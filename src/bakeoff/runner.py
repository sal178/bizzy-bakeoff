from pathlib import Path

import pandas as pd

from bakeoff.config import BakeoffConfig
from bakeoff.connectors.base import SourceConnector
from bakeoff.connectors.competitor_a_mock import CompetitorAMockConnector
from bakeoff.connectors.competitor_b_mock import CompetitorBMockConnector
from bakeoff.models import CompanyRecord, ContactRecord

from bakeoff.normalization.companies import normalize_company
from bakeoff.normalization.contacts import normalize_contact

from datetime import datetime

from bakeoff.comparison.compare import (
    compare_company_records,
    compare_contact_records,
)
from bakeoff.normalization.companies import normalize_company
from bakeoff.normalization.contacts import normalize_contact

from bakeoff.comparison.field_rules import COMPANY_FIELDS, CONTACT_FIELDS
from bakeoff.comparison.scoring import build_entity_score

from bakeoff.storage.output_writer import write_outputs

def load_bizzy_companies(path: str | Path) -> list[CompanyRecord]:
    """Load Bizzy company sample from CSV."""
    df = pd.read_csv(path)

    return [
        CompanyRecord(
            source="bizzy",
            external_id=row["external_id"],
            name=row.get("name"),
            domain=row["domain"],
            linkedin_url=row.get("linkedin_url"),
            country=row.get("country"),
            city=row.get("city"),
            industry=row.get("industry"),
            employee_count=row.get("employee_count"),
            revenue_range=row.get("revenue_range"),
            last_updated_at=None,
        )
        for row in df.to_dict(orient="records")
    ]


def load_bizzy_contacts(path: str | Path) -> list[ContactRecord]:
    """Load Bizzy contact sample from CSV."""
    df = pd.read_csv(path)

    return [
        ContactRecord(
            source="bizzy",
            external_id=row["external_id"],
            full_name=row.get("full_name"),
            email=row.get("email"),
            linkedin_url=row.get("linkedin_url"),
            job_title=row.get("job_title"),
            seniority=row.get("seniority"),
            department=row.get("department"),
            last_updated_at=None,
        )
        for row in df.to_dict(orient="records")
    ]


def fetch_company_records(
    bizzy_companies: list[CompanyRecord],
    connectors: list[SourceConnector],
) -> list[CompanyRecord]:
    """Fetch matching company records from selected competitor connectors."""
    records = []

    for company in bizzy_companies:
        for connector in connectors:
            record = connector.fetch_company(company.domain)
            if record:
                records.append(record)

    return records


def fetch_contact_records(
    bizzy_contacts: list[ContactRecord],
    connectors: list[SourceConnector],
) -> list[ContactRecord]:
    """Fetch matching contact records from selected competitor connectors."""
    records = []

    for contact in bizzy_contacts:
        if not contact.email:
            continue

        for connector in connectors:
            record = connector.fetch_contact(contact.email)
            if record:
                records.append(record)

    return records


def get_competitor_connectors(
    selected_sources: list[str],
) -> list[SourceConnector]:
    """Create connector instances for selected competitor sources."""
    available_connectors = {
        "competitor_a": CompetitorAMockConnector,
        "competitor_b": CompetitorBMockConnector,
    }

    unknown_sources = set(selected_sources) - set(available_connectors)
    if unknown_sources:
        raise ValueError(f"Unknown competitor sources: {sorted(unknown_sources)}")

    return [available_connectors[source]() for source in selected_sources]


def group_competitor_companies_by_domain(records):
    grouped = {}
    for r in records:
        grouped.setdefault(r.domain, []).append(r)
    return grouped


def group_competitor_contacts_by_email(records):
    grouped = {}
    for r in records:
        if r.email:
            grouped.setdefault(r.email, []).append(r)
    return grouped


def run_bakeoff(config: BakeoffConfig | None = None) -> None:
    config = config or BakeoffConfig()
    
    run_id = datetime.utcnow().isoformat()

    companies_path = Path(config.companies_path)
    contacts_path = Path(config.contacts_path)

    connectors = get_competitor_connectors(config.selected_sources)

    # Load Bizzy sample
    bizzy_companies = load_bizzy_companies(companies_path)
    bizzy_contacts = load_bizzy_contacts(contacts_path)

    # Normalize Bizzy
    bizzy_companies = [normalize_company(c) for c in bizzy_companies]
    bizzy_contacts = [normalize_contact(c) for c in bizzy_contacts]

    # Fetch competitors
    competitor_companies = fetch_company_records(bizzy_companies, connectors)
    competitor_contacts = fetch_contact_records(bizzy_contacts, connectors)

    # Normalize competitors
    competitor_companies = [normalize_company(c) for c in competitor_companies]
    competitor_contacts = [normalize_contact(c) for c in competitor_contacts]

    # Group competitors
    comp_companies_by_domain = group_competitor_companies_by_domain(competitor_companies)
    comp_contacts_by_email = group_competitor_contacts_by_email(competitor_contacts)

    # Run comparisons
    all_comparisons = []

    # Company comparisons
    for bizzy_company in bizzy_companies:
        competitors = comp_companies_by_domain.get(bizzy_company.domain, [])

        for comp in competitors:
            comparisons = compare_company_records(run_id, bizzy_company, comp)
            all_comparisons.extend(comparisons)

    # Contact comparisons
    for bizzy_contact in bizzy_contacts:
        if not bizzy_contact.email:
            continue

        competitors = comp_contacts_by_email.get(bizzy_contact.email, [])

        for comp in competitors:
            comparisons = compare_contact_records(run_id, bizzy_contact, comp)
            all_comparisons.extend(comparisons)

    print(f"Total comparisons generated: {len(all_comparisons)}")

    # Preview some results
    for c in all_comparisons[:10]:
        print(
            f"{c.entity_type} | {c.entity_id} | {c.compared_source} | "
            f"{c.field_name} | {c.bizzy_value} vs {c.source_value} → {c.winner}"
        )

    entity_scores = []

    for bizzy_company in bizzy_companies:
        company_comparisons = [
            c for c in all_comparisons
            if c.entity_type == "company" and c.entity_id == bizzy_company.external_id
        ]

        entity_scores.append(
            build_entity_score(
                run_id=run_id,
                entity_type="company",
                entity_id=bizzy_company.external_id,
                source="bizzy",
                record=bizzy_company,
                fields=COMPANY_FIELDS,
                comparisons=company_comparisons,
            )
        )

    for bizzy_contact in bizzy_contacts:
        contact_comparisons = [
            c for c in all_comparisons
            if c.entity_type == "contact" and c.entity_id == bizzy_contact.external_id
        ]

        entity_scores.append(
            build_entity_score(
                run_id=run_id,
                entity_type="contact",
                entity_id=bizzy_contact.external_id,
                source="bizzy",
                record=bizzy_contact,
                fields=CONTACT_FIELDS,
                comparisons=contact_comparisons,
            )
        )

    print("\nEntity scores:")
    for score in entity_scores:
        print(
            f"{score.entity_type} | {score.entity_id} | "
            f"accuracy={score.accuracy_score} | "
            f"coverage={score.coverage_score} | "
            f"freshness={score.freshness_score} | "
            f"overall={score.overall_score}"
        )
        
    write_outputs(
        config=config,
        field_comparisons=all_comparisons,
        entity_scores=entity_scores,
    )

    print("\nReports written.")

if __name__ == "__main__":
    run_bakeoff()