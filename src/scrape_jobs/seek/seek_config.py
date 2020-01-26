from configparser import ConfigParser

from scrape_jobs.config import Config, SearchConfig

__all__ = ["SeekConfig"]


class SeekConfig(Config):
    SECTION = "seek.com.au"

    @classmethod
    def parse_search_config(cls, parser: ConfigParser) -> SearchConfig:
        search_config = super().parse_search_config(parser)

        # update the search_params dict with parsed values
        search_params = search_config.search_params
        search_params["what"] = parser.get(cls.SECTION, "search_what")
        search_params["where"] = parser.get(cls.SECTION, "search_where")

        return search_config
