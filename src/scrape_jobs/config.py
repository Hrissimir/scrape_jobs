import logging
import pkgutil
from collections import namedtuple
from configparser import ConfigParser

from hed_utils.support.config_tool import parse_file, format_parser

__all__ = [
    "LOG_FORMAT",
    "CONFIG_FILENAME",
    "SearchConfig",
    "SheetsConfig",
    "TimeConfig",
    "Config",
    "get_sample_contents"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

LOG_FORMAT = "%(asctime)s | %(levelname)8s | %(message)s"
CONFIG_FILENAME = "scrape-jobs.ini"
SAMPLE_FILENAME = "sample_config.ini"

SearchConfig = namedtuple("SearchConfig", "driver_headless search_params max_post_age_days max_attempts")
SheetsConfig = namedtuple("SheetsConfig", "spreadsheet_title worksheet_title json_filepath")
TimeConfig = namedtuple("TimeConfig", "tz_name posted_fmt scraped_fmt")


def get_sample_contents():
    _log.debug("getting sample config contents...")
    return pkgutil.get_data(__package__, SAMPLE_FILENAME)


class Config:
    DEFAULT_MAX_ATTEMPTS = 3
    SECTION: str
    search_config: SearchConfig
    sheets_config: SheetsConfig
    time_config: TimeConfig

    def __init__(self):
        self.search_config = None
        self.sheets_config = None
        self.time_config = None

    def __repr__(self):
        return f"{type(self).__name__}({self.search_config}, {self.sheets_config}, {self.time_config})"

    @classmethod
    def parse_search_config(cls, parser: ConfigParser) -> SearchConfig:
        _log.debug("parsing search config...")
        return SearchConfig(driver_headless=parser.getboolean(cls.SECTION, "driver_headless"),
                            search_params=dict(),
                            max_post_age_days=parser.getint(cls.SECTION, "max_post_age_days"),
                            max_attempts=parser.getint(cls.SECTION, "max_attempts", fallback=cls.DEFAULT_MAX_ATTEMPTS))

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
        _log.debug("parsing %s ...", cls.__name__)
        config = cls()
        config.search_config = cls.parse_search_config(parser)
        config.sheets_config = cls.parse_sheets_config(parser)
        config.time_config = cls.parse_time_config(parser)
        return config

    @classmethod
    def parse_file(cls, src_file: str):
        _log.debug("reading '%s' config from file: '%s'", cls.__name__, src_file)
        parser = parse_file(src_file)
        _log.debug("got config contents:\n\n", format_parser(parser))
        return cls.parse(parser)
