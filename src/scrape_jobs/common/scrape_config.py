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
    DATE_POSTED = "date_posted"
    DAYS = "days"
    TIMEZONE = "timezone"
    UPLOAD_WORKSHEET_INDEX = "upload_worksheet_index"


def assert_valid_config(config):
    assert isinstance(config, ConfigParser), \
        f"The provided config was not a ConfigParser instance! ({type(config).__name__})"

    try:
        assert Default.KEY in config, f"No '[{Default.KEY}]' section in config file"
        default = config[Default.KEY]

        assert Default.UPLOAD_SPREADSHEET_NAME in default, \
            f"No value for '{Default.UPLOAD_SPREADSHEET_NAME}=' in '[{Default.KEY}]' section"
        assert Default.UPLOAD_SPREADSHEET_JSON in default, \
            f"No value for '{Default.UPLOAD_SPREADSHEET_JSON}=' in '[{Default.KEY}]' section"
        assert Default.UPLOAD_WORKSHEET_INDEX in default, \
            f"No value for '{Default.UPLOAD_WORKSHEET_INDEX}=' in '[{Default.KEY}]' section"

        assert SeekComAu.KEY in config, f"No '[{SeekComAu.KEY}]' section in config file"
        seek = config[SeekComAu.KEY]

        assert SeekComAu.WHAT in seek, \
            f"No value for '{SeekComAu.WHAT}=' in '[{SeekComAu.KEY}]' section!"
        assert SeekComAu.WHERE in seek, \
            f"No value for '{SeekComAu.WHERE}=' in '[{SeekComAu.KEY}]' section!"
        assert SeekComAu.DAYS in seek, \
            f"No value for '{SeekComAu.DAYS}=' in '[{SeekComAu.KEY}]' section!"

        assert SeekComAu.TIMEZONE in seek, \
            f"No value for '{SeekComAu.TIMEZONE}=' in '[{SeekComAu.KEY}]' section!"

        assert SeekComAu.UPLOAD_WORKSHEET_INDEX in seek, \
            f"No value for '{SeekComAu.UPLOAD_WORKSHEET_INDEX}=' in '[{SeekComAu.KEY}]' section!"

        assert LinkedinCom.KEY in config, f"No '[{LinkedinCom.KEY}]' section in config file"
        linkedin = config[LinkedinCom.KEY]

        assert LinkedinCom.KEYWORDS in linkedin, \
            f"No value for '{LinkedinCom.KEYWORDS}=' in '[{LinkedinCom.KEY}]' section!"

        assert LinkedinCom.LOCATION in linkedin, \
            f"No value for '{LinkedinCom.LOCATION}=' in '[{LinkedinCom.KEY}]' section!"

        assert LinkedinCom.DATE_POSTED in linkedin, \
            f"No value for '{LinkedinCom.DATE_POSTED}=' in '[{LinkedinCom.KEY}]' section!"

        assert LinkedinCom.DAYS in linkedin, \
            f"No value for '{LinkedinCom.DAYS}=' in '[{LinkedinCom.KEY}]' section!"

        assert LinkedinCom.TIMEZONE in linkedin, \
            f"No value for '{LinkedinCom.TIMEZONE}=' in '[{LinkedinCom.KEY}]' section!"

        assert LinkedinCom.UPLOAD_WORKSHEET_INDEX in linkedin, \
            f"No value for '{LinkedinCom.KEYWORDS}=' in '[{LinkedinCom.KEY}]' section!"

    except AssertionError as err:
        lines = [f"Bad config ({err}, {err.args})! Ensure your file matches the following sample:",
                 "\n-----------SAMPLE START-----------\n",
                 format_config(get_sample_config()),
                 "\n-----------SAMPLE END-----------\n"]
        msg = "\n".join(lines)
        new_err = AssertionError(msg)
        raise new_err from err


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
    linkedin[LinkedinCom.DATE_POSTED] = "Past Month"
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
