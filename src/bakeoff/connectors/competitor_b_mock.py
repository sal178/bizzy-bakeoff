from datetime import datetime

from bakeoff.connectors.base import SourceConnector
from bakeoff.models import CompanyRecord, ContactRecord


class CompetitorBMockConnector(SourceConnector):
    source_name = "competitor_b"

    def fetch_company(self, domain: str) -> CompanyRecord | None:
        data = {
            "acmeanalytics.com": CompanyRecord(
                source=self.source_name,
                external_id="comp-b-c001",
                name="Acme Analytics",
                domain="acmeanalytics.com",
                linkedin_url="https://www.linkedin.com/company/acme-analytics",
                country="BE",
                city="Brussels",
                industry="Analytics Software",
                employee_count=None,
                revenue_range="1M-10M",
                last_updated_at=datetime(2026, 4, 1),
            ),
            "greengrid.energy": CompanyRecord(
                source=self.source_name,
                external_id="comp-b-c003",
                name="GreenGrid Energy",
                domain="greengrid.energy",
                linkedin_url=None,
                country="BE",
                city="Gent",
                industry="Energy",
                employee_count=40,
                revenue_range=None,
                last_updated_at=datetime(2025, 10, 10),
            ),
            "medcore-systems.com": CompanyRecord(
                source=self.source_name,
                external_id="comp-b-c005",
                name="MedCore Systems",
                domain="medcore-systems.com",
                linkedin_url="https://www.linkedin.com/company/medcore-systems",
                country="FR",
                city="Lyon",
                industry="Healthcare Software",
                employee_count=500,
                revenue_range="50M-100M",
                last_updated_at=datetime(2026, 3, 25),
            ),
        }

        return data.get(domain)

    def fetch_contact(self, email: str) -> ContactRecord | None:
        data = {
            "emma.peeters@acmeanalytics.com": ContactRecord(
                source=self.source_name,
                external_id="comp-b-p001",
                full_name="Emma Peeters",
                email="emma.peeters@acmeanalytics.com",
                linkedin_url="https://www.linkedin.com/in/emma-peeters",
                job_title="Head of Sales",
                seniority="Head",
                department="Sales",
                last_updated_at=datetime(2026, 4, 9),
            ),
            "sophie.janssens@greengrid.energy": ContactRecord(
                source=self.source_name,
                external_id="comp-b-p003",
                full_name="Sophie Janssens",
                email="sophie@greengrid.energy",
                linkedin_url="https://www.linkedin.com/in/sophie-janssens",
                job_title="CEO",
                seniority="C-Level",
                department="Executive",
                last_updated_at=datetime(2026, 4, 3),
            ),
            "claire.martin@medcore-systems.com": ContactRecord(
                source=self.source_name,
                external_id="comp-b-p005",
                full_name="Claire Martin",
                email="claire.martin@medcore-systems.com",
                linkedin_url="https://www.linkedin.com/in/claire-martin",
                job_title="Chief Technology Officer",
                seniority="C-Level",
                department="Technology",
                last_updated_at=datetime(2026, 3, 30),
            ),
        }

        return data.get(email)