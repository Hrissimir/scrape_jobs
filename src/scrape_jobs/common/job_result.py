from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from bs4 import BeautifulSoup
from hed_utils.selenium.page_objects.base.element_soup import ElementSoup


class JobResult(ElementSoup, ABC):

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)

    @classmethod
    def keys(cls) -> List[str]:
        return ["utc_datetime", "location", "title", "company", "url"]

    @abstractmethod
    def get_utc_datetime(self) -> Optional[datetime]:  # pragma: no cover
        pass

    @abstractmethod
    def get_location(self) -> Optional[str]:  # pragma: no cover
        pass

    @abstractmethod
    def get_title(self) -> Optional[str]:  # pragma: no cover
        pass

    @abstractmethod
    def get_company(self) -> Optional[str]:  # pragma: no cover
        pass

    @abstractmethod
    def get_url(self) -> Optional[str]:  # pragma: no cover
        pass
