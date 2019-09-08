from datetime import datetime
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from hed_utils.selenium.page_objects.base.element_soup import ElementSoup


class JobResult(ElementSoup):

    def __init__(self, soup: BeautifulSoup):
        super().__init__(soup)

    @classmethod
    def keys(cls) -> List[str]:
        return ["utc_datetime", "location", "title", "company", "url"]

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()

    def values(self) -> List[Any]:
        return super().values()

    def get_utc_datetime(self) -> Optional[datetime]:  # pragma: no cover
        raise NotImplementedError()

    def get_location(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_title(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_company(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    def get_url(self) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()