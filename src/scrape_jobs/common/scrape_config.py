import pkgutil
from configparser import ConfigParser
from pathlib import Path
from typing import Optional, List, NoReturn

from hed_utils.support import log
from hed_utils.support.config_tool import ConfigSection

DEFAULT_FILENAME = "scrape-jobs.ini"
DEFAULT_CONTENTS = pkgutil.get_data("scrape_jobs.common", "scrape-jobs.ini").decode()


class ScrapeConfig(ConfigSection):
    KEYS = ["max_post_age_days",
            "timezone",
            "scraped_timestamp_format",
            "posted_timestamp_format",
            "driver_headless"]

    def __init__(self,
                 section_name: str,
                 section_keys: List[str],
                 config: ConfigParser):
        for key in self.KEYS:
            assert key in section_keys, f"Missing mandatory key '{key}', {self.KEYS}"

        super().__init__(section_name, section_keys, config)

    def get_search_params(self) -> dict:
        raise NotImplementedError()

    @property
    def max_post_age_days(self) -> int:
        return self.get_section().getint("max_post_age_days")

    @property
    def timezone(self) -> str:
        return self.get_section().get("timezone")

    @property
    def scraped_timestamp_format(self) -> str:
        return self.get_section().get("scraped_timestamp_format")

    @property
    def posted_timestamp_format(self) -> str:
        return self.get_section().get("posted_timestamp_format")

    @property
    def driver_headless(self) -> bool:
        return self.get_section().getboolean("driver_headless")


def get_sample_config() -> ConfigParser:
    log.debug("sample config file contents:\n%s", DEFAULT_CONTENTS)
    config = ConfigParser(interpolation=None)
    config.read_string(DEFAULT_CONTENTS)
    return config


def write_sample_config(file_path: Optional[str] = None) -> NoReturn:
    log.debug("writing sample config file at: '%s'", file_path)
    if not file_path:
        file_path = str(Path.cwd().joinpath(DEFAULT_FILENAME))
        log.debug("deduced file path '%s'", file_path)

    with open(file_path, "wb") as configfile:
        configfile.write(DEFAULT_CONTENTS.encode("utf-8"))
