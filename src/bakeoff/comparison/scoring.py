from datetime import datetime, timezone
from statistics import mean

from bakeoff.models import CompanyRecord, ContactRecord, EntityScore, FieldComparison


WEIGHTS = {
    "accuracy": 0.40,
    "coverage": 0.25,
    "freshness": 0.20,
    "format": 0.15,
}


def calculate_coverage_score(record: CompanyRecord | ContactRecord, fields: list[str]) -> float:
    present = 0

    for field in fields:
        value = getattr(record, field)
        if value is not None and value != "":
            present += 1

    return present / len(fields)


def calculate_accuracy_score(comparisons: list[FieldComparison]) -> float:
    if not comparisons:
        return 0.0

    matches = [c for c in comparisons if c.winner == "tie"]
    return len(matches) / len(comparisons)


def calculate_freshness_score(record: CompanyRecord | ContactRecord) -> float:
    if record.last_updated_at is None:
        return 0.0

    now = datetime.now(timezone.utc)

    last_updated = record.last_updated_at
    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)

    age_days = (now - last_updated).days

    if age_days <= 30:
        return 1.0
    if age_days <= 90:
        return 0.7
    if age_days <= 180:
        return 0.4

    return 0.1


def calculate_format_score(record: CompanyRecord | ContactRecord) -> float:
    checks = []

    if hasattr(record, "domain"):
        checks.append("." in record.domain if record.domain else False)

    if hasattr(record, "email"):
        checks.append("@" in record.email if record.email else False)

    if record.linkedin_url:
        checks.append(record.linkedin_url.startswith("https://www.linkedin.com/"))

    if not checks:
        return 1.0

    return mean(checks)


def calculate_overall_score(
    accuracy_score: float,
    coverage_score: float,
    freshness_score: float,
    format_score: float,
) -> float:
    return (
        WEIGHTS["accuracy"] * accuracy_score
        + WEIGHTS["coverage"] * coverage_score
        + WEIGHTS["freshness"] * freshness_score
        + WEIGHTS["format"] * format_score
    )


def build_entity_score(
    run_id: str,
    entity_type: str,
    entity_id: str,
    source: str,
    record: CompanyRecord | ContactRecord,
    fields: list[str],
    comparisons: list[FieldComparison],
) -> EntityScore:
    coverage_score = calculate_coverage_score(record, fields)
    accuracy_score = calculate_accuracy_score(comparisons)
    freshness_score = calculate_freshness_score(record)
    format_score = calculate_format_score(record)

    overall_score = calculate_overall_score(
        accuracy_score=accuracy_score,
        coverage_score=coverage_score,
        freshness_score=freshness_score,
        format_score=format_score,
    )

    return EntityScore(
        run_id=run_id,
        entity_type=entity_type,
        entity_id=entity_id,
        source=source,
        accuracy_score=round(accuracy_score, 3),
        coverage_score=round(coverage_score, 3),
        freshness_score=round(freshness_score, 3),
        format_score=round(format_score, 3),
        overall_score=round(overall_score, 3),
    )