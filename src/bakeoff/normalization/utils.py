def normalize_string(value: str | None) -> str | None:
    if not value:
        return None
    return value.strip().lower()


def normalize_country(value: str | None) -> str | None:
    if not value:
        return None

    mapping = {
        "be": "BE",
        "belgium": "BE",
        "nl": "NL",
        "netherlands": "NL",
        "fr": "FR",
        "france": "FR",
        "de": "DE",
        "germany": "DE",
    }

    return mapping.get(value.lower(), value.upper())


def normalize_city(value: str | None) -> str | None:
    if not value:
        return None

    mapping = {
        "bruxelles": "brussels",
        "gent": "ghent",
    }

    value = value.strip().lower()
    return mapping.get(value, value)