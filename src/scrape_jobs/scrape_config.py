from configparser import ConfigParser
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


def assert_valid(config):
    assert isinstance(config, ConfigParser)
    assert Default.KEY in config
    assert Default.UPLOAD_SPREADSHEET_NAME in config[Default.KEY]
    assert Default.UPLOAD_SPREADSHEET_JSON in config[Default.KEY]
    assert Default.UPLOAD_WORKSHEET_INDEX in config[Default.KEY]

    assert SeekComAu.KEY in config
    assert SeekComAu.WHAT in config[SeekComAu.KEY]
    assert SeekComAu.WHERE in config[SeekComAu.KEY]
    assert SeekComAu.DAYS in config[SeekComAu.KEY]
    assert SeekComAu.TIMEZONE in config[SeekComAu.KEY]
    assert SeekComAu.UPLOAD_WORKSHEET_INDEX in config[SeekComAu.KEY]


def get_sample_config() -> ConfigParser:
    config = ConfigParser()
    config[Default.KEY] = {}
    config[Default.KEY][Default.UPLOAD_SPREADSHEET_NAME] = "job_stats_data"
    config[Default.KEY][Default.UPLOAD_SPREADSHEET_JSON] = "Replace with path to secrets.json file."
    config[Default.KEY][Default.UPLOAD_WORKSHEET_INDEX] = "0"

    config[SeekComAu.KEY] = {}
    config[SeekComAu.KEY][SeekComAu.WHAT] = "Replace with search query"
    config[SeekComAu.KEY][SeekComAu.WHERE] = "All Sydney NSW"
    config[SeekComAu.KEY][SeekComAu.DAYS] = "3"
    config[SeekComAu.KEY][SeekComAu.TIMEZONE] = "Australia/Sydney"
    config[SeekComAu.KEY][SeekComAu.UPLOAD_WORKSHEET_INDEX] = "0"

    return config


def read_config(file_path: Optional[str] = None):
    if not file_path:
        file_path = str(Path.cwd().joinpath(CONFIG_FILENAME))

    config = ConfigParser()
    with open(file_path, "r") as configfile:
        config.read_file(configfile)

    return config


def write_config(file_path: Optional[str] = None):
    if not file_path:
        file_path = str(Path.cwd().joinpath(CONFIG_FILENAME))

    log.debug("writing sample scrape config to: '%s'", file_path)
    config = get_sample_config()
    with open(file_path, "w") as configfile:
        config.write(configfile)
