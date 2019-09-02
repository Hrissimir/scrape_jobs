from abc import ABC, abstractmethod, abstractclassmethod
from datetime import datetime
from typing import Optional, List

from bs4 import BeautifulSoup


class Result(ABC):

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @abstractclassmethod
    def get_dict_keys(cls) -> List[str]:
        pass

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
