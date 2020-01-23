import logging
import pkgutil
from collections import namedtuple
from configparser import ConfigParser
from datetime import timedelta

from hed_utils.support import config_tool, time_tool

__all__ = [
    "CONFIG_FILENAME",
    "SearchConfig",
    "SheetsConfig",
    "TimeConfig",
    "Config",
    "get_sample_contents"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

CONFIG_FILENAME = "scrape-jobs.ini"
SAMPLE_FILENAME = "config_sample.ini"

SearchConfig = namedtuple("SearchConfig", "driver_headless search_params utc_posted_after")
SheetsConfig = namedtuple("SheetsConfig", "spreadsheet_title worksheet_title json_filepath")
TimeConfig = namedtuple("TimeConfig", "tz_name posted_fmt scraped_fmt")


def get_sample_contents():
    return pkgutil.get_data(__package__, SAMPLE_FILENAME)


class Config:
    SECTION: str
    search_config: SearchConfig
    sheets_config: SheetsConfig
    time_config: TimeConfig

    def __repr__(self):
        return f"{type(self).__name__}({self.search_config}, {self.sheets_config}, {self.time_config})"

    @classmethod
    def parse_search_config(cls, parser: ConfigParser) -> SearchConfig:
        _log.debug("parsing search config...")
        max_post_age_days = parser.getint(cls.SECTION, "max_post_age_days")
        max_post_age = timedelta(days=max_post_age_days)
        utc_now = time_tool.utc_moment().replace(minute=0, second=0, microsecond=0)
        utc_posted_after = utc_now - max_post_age
        return SearchConfig(driver_headless=parser.getboolean(cls.SECTION, "driver_headless"),
                            search_params=dict(),
                            utc_posted_after=utc_posted_after)

    @classmethod
    def parse_time_config(cls, parser: ConfigParser) -> TimeConfig:
        _log.debug("parsing time config...")
        return TimeConfig(tz_name=parser.get(cls.SECTION, "tz_name"),
                          posted_fmt=parser.get(cls.SECTION, "posted_fmt"),
                          scraped_fmt=parser.get(cls.SECTION, "scraped_fmt"))

    @classmethod
    def parse_sheets_config(cls, parser: ConfigParser) -> SheetsConfig:
        _log.debug("parsing sheets config...")
        return SheetsConfig(spreadsheet_title=parser.get(cls.SECTION, "spreadsheet_title"),
                            worksheet_title=parser.get(cls.SECTION, "worksheet_title"),
                            json_filepath=parser.get(cls.SECTION, "json_filepath"))

    @classmethod
    def parse(cls, parser: ConfigParser):
        config = cls()
        config.search_config = cls.parse_search_config(parser)
        config.sheets_config = cls.parse_sheets_config(parser)
        config.time_config = cls.parse_time_config(parser)
        return config

    @classmethod
    def from_file(cls, src_file: str):
        _log.info("reading '%s' config from file: '%s'", cls.__name__, src_file)
        parser = config_tool.parse_file(src_file)
        return cls.parse(parser)
