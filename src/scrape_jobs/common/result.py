from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from bs4 import BeautifulSoup
from hed_utils.support import time_tool


class Result(ABC):

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @abstractmethod
    def get_utc_datetime(self) -> Optional[datetime]:
        pass

    @abstractmethod
    def get_location(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_title(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_company(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_url(self) -> Optional[str]:
        pass

    def as_dict(self):
        return dict(utc_datetime=self.get_utc_datetime(),
                    location=self.get_location(),
                    title=self.get_title(),
                    company=self.get_company(),
                    url=self.get_url())
