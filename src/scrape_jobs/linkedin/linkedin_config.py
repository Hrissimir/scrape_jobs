from configparser import ConfigParser

from scrape_jobs.config import Config, SearchConfig

__all__ = ["LinkedinConfig"]


class LinkedinConfig(Config):
    SECTION = "linkedin.com"

    @classmethod
    def parse_search_config(cls, parser: ConfigParser) -> SearchConfig:
        search_config = super().parse_search_config(parser)

        # update the search_params dict with parsed values
        search_params = search_config.search_params
        search_params["keywords"] = parser.get(cls.SECTION, "search_keywords")
        search_params["location"] = parser.get(cls.SECTION, "search_location")
        search_params["date_posted"] = parser.get(cls.SECTION, "date_posted")

        return search_config
