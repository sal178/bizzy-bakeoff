from abc import ABC, abstractmethod

from bakeoff.models import CompanyRecord, ContactRecord


class SourceConnector(ABC):
    source_name: str

    @abstractmethod
    def fetch_company(self, domain: str) -> CompanyRecord | None:
        pass

    @abstractmethod
    def fetch_contact(self, email: str) -> ContactRecord | None:
        pass