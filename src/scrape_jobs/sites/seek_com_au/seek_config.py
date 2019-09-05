from configparser import ConfigParser
from typing import List

from scrape_jobs.common.scrape_config import ScrapeConfig


class SeekConfig(ScrapeConfig):
    def __init__(self, cfg: ConfigParser):
        super().__init__(cfg)

    @classmethod
    def section_name(cls) -> str:
        return "seek.com.au"

    @classmethod
    def section_keys(cls) -> List[str]:
        return super().section_keys() + ["what", "where"]

    @property
    def what(self) -> str:
        return self.config_section.get("what")

    @property
    def where(self) -> str:
        return self.config_section.get("where")

    def get_search_params(self) -> dict:
        return dict(what=self.what,
                    where=self.where)
