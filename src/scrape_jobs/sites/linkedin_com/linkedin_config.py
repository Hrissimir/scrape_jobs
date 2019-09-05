from typing import List

from scrape_jobs.common.scrape_config import ScrapeConfig


class LinkedinConfig(ScrapeConfig):
    @classmethod
    def section_name(cls) -> str:
        return "linkedin.com"

    @classmethod
    def section_keys(cls) -> List[str]:
        return super().section_keys() + ["keywords", "location", "date_posted"]

    @property
    def keywords(self) -> str:
        return self.config_section.get("keywords")

    @property
    def location(self) -> str:
        return self.config_section.get("location")

    @property
    def date_posted(self) -> str:
        return self.config_section.get("date_posted")