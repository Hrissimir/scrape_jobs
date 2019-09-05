import pkgutil
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Optional, List
from unittest import mock

from hed_utils.support import log

DEFAULT_FILENAME = "scrape-jobs.ini"
DEFAULT_CONTENTS = pkgutil.get_data("scrape_jobs.common", "scrape-jobs.ini").decode()


class ScrapeConfig:

    def __init__(self, cfg: ConfigParser):
        assert isinstance(cfg, ConfigParser), f"Expected ConfigParser , Got: {type(cfg).__name__}"
        self.cfg = cfg

    def __repr__(self):
        return f"{type(self).__name__}(section_name='{self.section_name()}', section_keys={self.section_keys()})"

    @classmethod
    def section_name(cls) -> str:
        return "DEFAULT"

    @classmethod
    def section_keys(cls) -> List[str]:
        return ["upload_spreadsheet_name",
                "upload_spreadsheet_json",
                "upload_worksheet_index",
                "max_post_age_days",
                "timezone",
                "scraped_timestamp_format",
                "posted_timestamp_format"]

    @property
    def config_section(self):
        return self.cfg[self.section_name()]

    @property
    def upload_spreadsheet_name(self) -> str:
        return self.config_section.get("upload_spreadsheet_name")

    @property
    def upload_spreadsheet_json(self) -> str:
        return self.config_section.get("upload_spreadsheet_json")

    @property
    def upload_worksheet_index(self) -> int:
        return self.config_section.getint("upload_worksheet_index")

    @property
    def max_post_age_days(self) -> int:
        return self.config_section.getint("max_post_age_days")

    @property
    def timezone(self) -> str:
        return self.config_section.get("timezone")

    @property
    def scraped_timestamp_format(self) -> str:
        return self.config_section.get("scraped_timestamp_format")

    @property
    def posted_timestamp_format(self) -> str:
        return self.config_section.get("posted_timestamp_format")

    def is_present(self) -> bool:
        try:
            return self.config_section is not None
        except:
            return False

    def is_properly_filled(self) -> bool:
        log.debug("checking if '%s' section is properly filled...", self)
        try:
            section = self.config_section
        except KeyError as kerr:
            raise AssertionError(
                f"No [{self.section_name()}] section present! {list(self.cfg.keys())}"
            ) from kerr
        actual_keys = list(section.keys())
        for expected_key in self.section_keys():
            if expected_key not in actual_keys:
                log.warning("expected key '%s' not present in actual keys: %s", expected_key, actual_keys)

        all_ok = True
        for expected_key in self.section_keys():
            actual_value = section.get(expected_key, fallback=None)

            if actual_value is None:
                log.warning("could not deduce section value for key: '%s'", expected_key)
                all_ok = False

        return all_ok

    def assert_is_valid(self):
        if not self.is_properly_filled():
            raise AssertionError((f"Invalid config: {self}! "
                                  f"Ensure your config file matches the following template:\n%s"),
                                 DEFAULT_CONTENTS)


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


def get_sample_config() -> ConfigParser:
    log.debug("sample config file contents:\n%s", DEFAULT_CONTENTS)
    config = ConfigParser(interpolation=None)
    config.read_string(DEFAULT_CONTENTS)
    return config


def print_config(config: ConfigParser):
    log.debug("printing config details...")
    for section_name in config.keys():
        print()
        print(f"[{section_name}]")
        section_config = config[section_name]
        for key in section_config.keys():
            print(f"{key} = {section_config[key]}")


def format_config(config: ConfigParser) -> str:
    log.debug("formatting config...")
    with mock.patch("sys.stdout", new=StringIO()) as fake_out:
        print_config(config)
        return fake_out.getvalue()


def write_sample_config(file_path: Optional[str] = None):
    log.debug("writing sample config file at: '%s'", file_path)
    if not file_path:
        file_path = str(Path.cwd().joinpath(DEFAULT_FILENAME))
        log.debug("deduced file path '%s'", file_path)

    with open(file_path, "wb") as configfile:
        configfile.write(DEFAULT_CONTENTS.encode("utf-8"))


def read_config(file_path: Optional[str] = None):
    log.debug("reading config from file: '%s'", file_path)
    if not file_path:
        file_path = str(Path.cwd().joinpath(DEFAULT_FILENAME))
        log.debug("deduced file path: '%s'", file_path)

    config = ConfigParser(interpolation=None)
    with open(file_path, "r") as configfile:
        config.read_file(configfile)

    log.debug("done reading config from '%s' got:\n%s", file_path, format_config(config))
    return config


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
