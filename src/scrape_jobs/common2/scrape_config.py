from configparser import ConfigParser
from typing import List

from hed_utils.support.config_tool import ConfigSection


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


