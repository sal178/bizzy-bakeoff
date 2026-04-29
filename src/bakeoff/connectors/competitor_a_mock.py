from datetime import datetime

from bakeoff.connectors.base import SourceConnector
from bakeoff.models import CompanyRecord, ContactRecord


class CompetitorAMockConnector(SourceConnector):
    source_name = "competitor_a"

    def fetch_company(self, domain: str) -> CompanyRecord | None:
        data = {
            "acmeanalytics.com": CompanyRecord(
                source=self.source_name,
                external_id="comp-a-c001",
                name="Acme Analytics BV",
                domain="acmeanalytics.com",
                linkedin_url="https://www.linkedin.com/company/acme-analytics",
                country="BE",
                city="Bruxelles",
                industry="Business Intelligence",
                employee_count=90,
                revenue_range=None,
                last_updated_at=datetime(2025, 12, 15),
            ),
            "northstarlogistics.eu": CompanyRecord(
                source=self.source_name,
                external_id="comp-a-c002",
                name="Northstar Logistics",
                domain="northstarlogistics.eu",
                linkedin_url=None,
                country="NL",
                city="Amsterdam",
                industry="Transportation",
                employee_count=810,
                revenue_range="50M-100M",
                last_updated_at=datetime(2026, 2, 20),
            ),
            "finovo.io": CompanyRecord(
                source=self.source_name,
                external_id="comp-a-c004",
                name="Finovo",
                domain="finovo.io",
                linkedin_url="https://www.linkedin.com/company/finovo",
                country="DE",
                city="Berlin",
                industry="Financial Technology",
                employee_count=210,
                revenue_range="10M-50M",
                last_updated_at=datetime(2026, 3, 5),
            ),
        }

        return data.get(domain)

    def fetch_contact(self, email: str) -> ContactRecord | None:
        data = {
            "emma.peeters@acmeanalytics.com": ContactRecord(
                source=self.source_name,
                external_id="comp-a-p001",
                full_name="Emma Peeters",
                email="emma.peeters@acmeanalytics.com",
                linkedin_url="https://www.linkedin.com/in/emma-peeters",
                job_title="Sales Director",
                seniority="Director",
                department="Sales",
                last_updated_at=datetime(2025, 11, 30),
            ),
            "lucas.devries@northstarlogistics.eu": ContactRecord(
                source=self.source_name,
                external_id="comp-a-p002",
                full_name="Lucas Devries",
                email="lucas.devries@northstarlogistics.eu",
                linkedin_url=None,
                job_title="Operations Director",
                seniority="Director",
                department="Operations",
                last_updated_at=datetime(2026, 1, 12),
            ),
            "max.schneider@finovo.io": ContactRecord(
                source=self.source_name,
                external_id="comp-a-p004",
                full_name="Max Schneider",
                email="max.schneider@finovo.io",
                linkedin_url="https://www.linkedin.com/in/max-schneider",
                job_title="Data Engineering Manager",
                seniority="Manager",
                department="Engineering",
                last_updated_at=datetime(2026, 3, 15),
            ),
        }

        return data.get(email)