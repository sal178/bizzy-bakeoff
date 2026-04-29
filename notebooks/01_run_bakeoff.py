from bakeoff.config import BakeoffConfig
from bakeoff.runner import run_bakeoff

config = BakeoffConfig(
    companies_path="/Volumes/bizzy_bakeoff/input/sample_companies.csv",
    contacts_path="/Volumes/bizzy_bakeoff/input/sample_contacts.csv",
    output_mode="delta",
    catalog="bizzy_bakeoff",
    schema="gold",
)

run_bakeoff(config)