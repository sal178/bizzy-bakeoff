from bakeoff.models import CompanyRecord
from bakeoff.normalization.utils import (
    normalize_city,
    normalize_country,
    normalize_string,
)


def normalize_company(record: CompanyRecord) -> CompanyRecord:
    return CompanyRecord(
        source=record.source,
        external_id=record.external_id,
        name=normalize_string(record.name),
        domain=normalize_string(record.domain),
        linkedin_url=normalize_string(record.linkedin_url),
        country=normalize_country(record.country),
        city=normalize_city(record.city),
        industry=normalize_string(record.industry),
        employee_count=record.employee_count,
        revenue_range=normalize_string(record.revenue_range),
        last_updated_at=record.last_updated_at,
    )