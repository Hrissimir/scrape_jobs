from configparser import ConfigParser

from scrape_jobs.common.scrape_config import ScrapeConfig
from scrape_jobs.common.upload_config import UploadConfig


class SeekUploadConfig(UploadConfig):
    def __init__(self, config: ConfigParser):
        super().__init__("seek.com.au", config)


class SeekScrapeConfig(ScrapeConfig):
    KEYS = ScrapeConfig.KEYS + ["what", "where"]

    def __init__(self, config: ConfigParser):
        super().__init__("seek.com.au", self.KEYS, config)

    @property
    def what(self) -> str:
        return self.get_section().get("what")

    @property
    def where(self) -> str:
        return self.get_section().get("where")

    def get_search_params(self) -> dict:
        return dict(what=self.what,
                    where=self.where)
