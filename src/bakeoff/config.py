from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BakeoffConfig:
    companies_path: str | Path = Path("data/sample/sample_companies.csv")
    contacts_path: str | Path = Path("data/sample/sample_contacts.csv")

    selected_sources: list[str] = field(
        default_factory=lambda: ["competitor_a", "competitor_b"]
    )

    output_mode: str = "csv"  # overwritten in notebook
    output_dir: str | Path = Path("reports")

    catalog: str | None = None
    schema: str | None = None