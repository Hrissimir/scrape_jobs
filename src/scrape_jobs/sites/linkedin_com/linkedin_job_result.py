from datetime import datetime
from typing import Optional, List

from bs4 import BeautifulSoup
from hed_utils.support import time_tool

from scrape_jobs.common.result import Result


class LinkedinJobResult(Result):
    @classmethod
    def get_dict_keys(cls) -> List[str]:
        return ["utc_datetime", "location", "title", "company", "url"]

    def get_utc_datetime(self) -> Optional[datetime]:
        try:
            date_text_local = self.soup.select_one("time")["datetime"].strip()
            datetime_local = datetime.strptime(date_text_local, "%Y-%m-%d")
            return time_tool.localize(datetime_local, "UTC")
        except:
            return None

    def get_location(self) -> Optional[str]:
        try:
            return self.soup.select_one("span.job-result-card__location").get_text().strip()
        except:
            return None

    def get_title(self) -> Optional[str]:
        try:
            return self.soup.select_one("span.job-result-card__location").get_text().strip()
        except:
            return None

    def get_company(self) -> Optional[str]:
        try:
            return self.soup.select_one("h4.result-card__subtitle").get_text().strip()
        except:
            return None

    def get_url(self) -> Optional[str]:
        try:
            a = self.soup.select_one("a.result-card__full-card-link")
            url = a["href"]
            return url[:url.index("?")]
        except:
            return None

    def as_dict(self):
        return dict(utc_datetime=self.get_utc_datetime(),
                    location=self.get_location(),
                    title=self.get_title(),
                    company=self.get_company(),
                    url=self.get_url())
