from configparser import ConfigParser

from scrape_jobs.common.scrape_config import ScrapeConfig
from scrape_jobs.common.upload_config import UploadConfig


class LinkedinUploadConfig(UploadConfig):

    def __init__(self, config: ConfigParser):
        super().__init__("linkedin.com", config)


class LinkedinScrapeConfig(ScrapeConfig):
    KEYS = ScrapeConfig.KEYS + ["keywords", "location", "date_posted"]

    def __init__(self, config: ConfigParser):
        super().__init__("linkedin.com", self.KEYS, config)

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
