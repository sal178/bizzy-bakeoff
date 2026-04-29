from bakeoff.models import ContactRecord
from bakeoff.normalization.utils import normalize_string


def normalize_contact(record: ContactRecord) -> ContactRecord:
    return ContactRecord(
        source=record.source,
        external_id=record.external_id,
        full_name=normalize_string(record.full_name),
        email=normalize_string(record.email),
        linkedin_url=normalize_string(record.linkedin_url),
        job_title=normalize_string(record.job_title),
        seniority=normalize_string(record.seniority),
        department=normalize_string(record.department),
        last_updated_at=record.last_updated_at,
    )