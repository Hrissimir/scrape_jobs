from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Optional

from hed_utils.support import log

CONFIG_FILENAME = "scrape-jobs.ini"


class Default:
    KEY = "DEFAULT"
    UPLOAD_SPREADSHEET_NAME = "upload_spreadsheet_name"
    UPLOAD_SPREADSHEET_JSON = "upload_spreadsheet_json"
    UPLOAD_WORKSHEET_INDEX = "upload_worksheet_index"


class SeekComAu:
    KEY = "seek.com.au"
    WHAT = "what"
    WHERE = "where"
    DAYS = "days"
    TIMEZONE = "timezone"
    UPLOAD_WORKSHEET_INDEX = "upload_worksheet_index"


class LinkedinCom:
    KEY = "linkedin.com"
    KEYWORDS = "keywords"
    LOCATION = "location"
    DAYS = "days"
    TIMEZONE = "timezone"
    UPLOAD_WORKSHEET_INDEX = "upload_worksheet_index"


def assert_valid_config(config):
    assert isinstance(config, ConfigParser)
    assert Default.KEY in config
    default = config[Default.KEY]
    assert Default.UPLOAD_SPREADSHEET_NAME in default
    assert Default.UPLOAD_SPREADSHEET_JSON in default
    assert Default.UPLOAD_WORKSHEET_INDEX in default

    assert SeekComAu.KEY in config
    seek = config[SeekComAu.KEY]

    assert SeekComAu.WHAT in seek
    assert SeekComAu.WHERE in seek
    assert SeekComAu.DAYS in seek
    assert SeekComAu.TIMEZONE in seek
    assert SeekComAu.UPLOAD_WORKSHEET_INDEX in seek

    assert LinkedinCom.KEY in config
    linkedin = config[LinkedinCom.KEY]

    assert LinkedinCom.KEYWORDS in linkedin
    assert LinkedinCom.LOCATION in linkedin
    assert LinkedinCom.DAYS in linkedin
    assert LinkedinCom.TIMEZONE in linkedin
    assert LinkedinCom.UPLOAD_WORKSHEET_INDEX in linkedin


def get_sample_config() -> ConfigParser:
    config = ConfigParser()
    config[Default.KEY] = {}
    default = config[Default.KEY]
    default[Default.UPLOAD_SPREADSHEET_NAME] = "jobs_stats_data"
    default[Default.UPLOAD_SPREADSHEET_JSON] = "Replace with path to secrets.json file."
    default[Default.UPLOAD_WORKSHEET_INDEX] = "0"

    config[SeekComAu.KEY] = {}
    seek = config[SeekComAu.KEY]
    seek[SeekComAu.WHAT] = "Replace with search query"
    seek[SeekComAu.WHERE] = "All Sydney NSW"
    seek[SeekComAu.DAYS] = "3"
    seek[SeekComAu.TIMEZONE] = "Australia/Sydney"
    seek[SeekComAu.UPLOAD_WORKSHEET_INDEX] = "0"

    config[LinkedinCom.KEY] = {}
    linkedin = config[LinkedinCom.KEY]
    linkedin[LinkedinCom.KEYWORDS] = "Replace with search query"
    linkedin[LinkedinCom.LOCATION] = "Sydney, New South Wales, Australia"
    linkedin[LinkedinCom.DAYS] = "2"
    linkedin[LinkedinCom.TIMEZONE] = "Australia/Sydney"
    linkedin[LinkedinCom.UPLOAD_WORKSHEET_INDEX] = "1"

    log.debug("got sample config:\n%s", format_config(config))
    return config


def format_config(config: ConfigParser) -> str:
    buffer = StringIO()
    config.write(buffer)
    return buffer.getvalue().strip()


def read_config(file_path: Optional[str] = None):
    if not file_path:
        file_path = str(Path.cwd().joinpath(CONFIG_FILENAME))

    config = ConfigParser()
    with open(file_path, "r") as configfile:
        config.read_file(configfile)

    log.debug("read config from '%s' got:\n%s", file_path, format_config(config))
    return config


def write_config(file_path: Optional[str] = None):
    if not file_path:
        file_path = str(Path.cwd().joinpath(CONFIG_FILENAME))

    log.debug("writing sample scrape config to: '%s'", file_path)
    config = get_sample_config()
    with open(file_path, "w") as configfile:
        config.write(configfile)
