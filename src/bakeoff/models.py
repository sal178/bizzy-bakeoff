from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


EntityType = Literal["company", "contact"]


class CompanyRecord(BaseModel):
    source: str
    external_id: str

    name: str | None = None
    domain: str
    linkedin_url: str | None = None

    country: str | None = None
    city: str | None = None
    industry: str | None = None
    employee_count: int | None = None
    revenue_range: str | None = None

    last_updated_at: datetime | None = None


class ContactRecord(BaseModel):
    source: str
    external_id: str

    full_name: str | None = None
    email: str | None = None
    linkedin_url: str | None = None

    job_title: str | None = None
    seniority: str | None = None
    department: str | None = None

    last_updated_at: datetime | None = None


class FieldComparison(BaseModel):
    run_id: str
    entity_type: EntityType
    entity_id: str
    compared_source: str
    field_name: str

    bizzy_value: object | None = None
    source_value: object | None = None

    truth_value: object | None = None
    winner: str | None = None
    confidence: float | None = None
    notes: str | None = None


class EntityScore(BaseModel):
    run_id: str
    entity_type: EntityType
    entity_id: str
    source: str

    coverage_score: float
    accuracy_score: float
    freshness_score: float
    format_score: float
    overall_score: float