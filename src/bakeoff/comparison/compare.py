from bakeoff.comparison.field_rules import COMPANY_FIELDS, CONTACT_FIELDS
from bakeoff.models import CompanyRecord, ContactRecord, FieldComparison


def values_match(bizzy_value: object | None, source_value: object | None) -> bool:
    if bizzy_value is None or source_value is None:
        return False

    return bizzy_value == source_value


def compare_records(
    run_id: str,
    entity_type: str,
    entity_id: str,
    bizzy_record: CompanyRecord | ContactRecord,
    source_record: CompanyRecord | ContactRecord,
    fields: list[str],
) -> list[FieldComparison]:
    comparisons = []

    for field in fields:
        bizzy_value = getattr(bizzy_record, field)
        source_value = getattr(source_record, field)
        is_match = values_match(bizzy_value, source_value)

        comparisons.append(
            FieldComparison(
                run_id=run_id,
                entity_type=entity_type,
                entity_id=entity_id,
                compared_source=source_record.source,
                field_name=field,
                bizzy_value=bizzy_value,
                source_value=source_value,
                truth_value=bizzy_value,
                winner="tie" if is_match else "bizzy",
                confidence=0.7,
                notes="Values match" if is_match else "Values differ",
            )
        )

    return comparisons


def compare_company_records(
    run_id: str,
    bizzy_record: CompanyRecord,
    source_record: CompanyRecord,
) -> list[FieldComparison]:
    return compare_records(
        run_id=run_id,
        entity_type="company",
        entity_id=bizzy_record.external_id,
        bizzy_record=bizzy_record,
        source_record=source_record,
        fields=COMPANY_FIELDS,
    )


def compare_contact_records(
    run_id: str,
    bizzy_record: ContactRecord,
    source_record: ContactRecord,
) -> list[FieldComparison]:
    return compare_records(
        run_id=run_id,
        entity_type="contact",
        entity_id=bizzy_record.external_id,
        bizzy_record=bizzy_record,
        source_record=source_record,
        fields=CONTACT_FIELDS,
    )