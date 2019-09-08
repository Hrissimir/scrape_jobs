from typing import List

from scrape_jobs.common.scrape_config import ScrapeConfig
from scrape_jobs.common.upload_config import UploadConfig


class LinkedinUploadConfig(UploadConfig):

    @classmethod
    def get_section_name(cls) -> str:
        return "linkedin.com"


class LinkedinScrapeConfig(ScrapeConfig):

    @classmethod
    def get_section_name(cls) -> str:
        return "linkedin.com"

    @classmethod
    def get_section_keys(cls) -> List[str]:
        return super().get_section_keys() + ["keywords", "location", "date_posted"]

    @property
    def keywords(self) -> str:
        return self.get_section().get("keywords")

    @property
    def location(self) -> str:
        return self.get_section().get("location")

    @property
    def date_posted(self) -> str:
        return self.get_section().get("date_posted")

    def get_search_params(self) -> dict:
        return dict(keywords=self.keywords,
                    location=self.location,
                    date_posted=self.date_posted)
