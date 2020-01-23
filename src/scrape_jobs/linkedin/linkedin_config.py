import logging
from configparser import ConfigParser

from scrape_jobs.base.config import Config, SearchConfig

__all__ = [
    "LinkedinConfig"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class LinkedinConfig(Config):
    SECTION = "linkedin.com"

    def __init__(self):
        super().__init__()
        self.search_config = None
        self.sheets_config = None
        self.time_config = None

    @classmethod
    def parse_search_config(cls, parser: ConfigParser) -> SearchConfig:
        search_config = super().parse_search_config(parser)

        # update the search_params dict with parsed values
        search_params = search_config.search_params
        search_params["keywords"] = parser.get(cls.SECTION, "search_keywords")
        search_params["location"] = parser.get(cls.SECTION, "search_location")
        search_params["date_posted"] = parser.get(cls.SECTION, "date_posted")

        return search_config
