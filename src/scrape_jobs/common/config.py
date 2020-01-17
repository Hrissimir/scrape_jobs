import logging

from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

DEFAULT_FILENAME = "scrape-jobs.ini"

SAMPLE_FILEPATH = Path(__file__).parent.joinpath(DEFAULT_FILENAME)

SheetsConfig = namedtuple("SheetsConfig", "json_filepath spreadsheet_name worksheet_index urls_column_index")
TimeConfig = namedtuple("TimeConfig", "timezone max_post_age_days scraped_timestamp_fmt posted_timestamp_fmt")
ScrapeConfig = namedtuple("ScrapeConfig", "sheets_config time_config driver_headless search_params")


def parse_sheets_config(cfg: ConfigParser, section: str) -> SheetsConfig:
    """Extracts a SheetsConfig from a ConfigParser section by name"""

    _log.debug("parsing sheets config for section: '%s'", section)
    json_filepath = cfg.get(section, "upload_spreadsheet_json")
    spreadsheet_name = cfg.get(section, "upload_spreadsheet_name")
    worksheet_index = cfg.getint(section, "upload_worksheet_index")
    urls_column_index = cfg.getint(section, "upload_worksheet_urls_column_index")
    sheets_config = SheetsConfig(json_filepath, spreadsheet_name, worksheet_index, urls_column_index)
    _log.info("got sheets config: %s", sheets_config)
    return sheets_config


def parse_time_config(cfg: ConfigParser, section: str) -> TimeConfig:
    """Extracts a TimeConfig from a ConfigParser section by name"""

    _log.debug("parsing time config for section: '%s'", section)
    timezone = cfg.get(section, "timezone")
    max_post_age_days = cfg.getint(section, "max_post_age_days")
    scraped_timestamp_fmt = cfg.get(section, "scraped_timestamp_format")
    posted_timestamp_fmt = cfg.get(section, "posted_timestamp_format")
    time_config = TimeConfig(timezone, max_post_age_days, scraped_timestamp_fmt, posted_timestamp_fmt)
    _log.info("got time config: %s", time_config)
    return time_config


def write_sample(parent_dir):
    """Creates a sample config file in the given dir."""

    target_filepath = Path(parent_dir).joinpath(DEFAULT_FILENAME)
    sample_contents = SAMPLE_FILEPATH.read_text(encoding="utf-8")
    target_filepath.write_text(sample_contents, encoding="utf-8")
    _log.info("created sample config file at: '%s'", str(target_filepath))
