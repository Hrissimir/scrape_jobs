from abc import ABC
from configparser import ConfigParser
from typing import List

from hed_utils.support.config_base import ConfigBase


class UploadConfig(ConfigBase, ABC):

    def __init__(self, cfg: ConfigParser):
        super().__init__(cfg)

    @classmethod
    def get_section_keys(cls) -> List[str]:
        return ["upload_spreadsheet_name",
                "upload_spreadsheet_json",
                "upload_worksheet_index",
                "upload_worksheet_expected_columns_count",
                "upload_worksheet_urls_column_index"]

    @property
    def upload_spreadsheet_name(self) -> str:
        return self.get_section().get("upload_spreadsheet_name")

    @property
    def upload_spreadsheet_json(self) -> str:
        return self.get_section().get("upload_spreadsheet_json")

    @property
    def upload_worksheet_index(self) -> int:
        return self.get_section().getint("upload_worksheet_index")

    @property
    def upload_worksheet_expected_columns_count(self) -> int:
        return self.get_section().getint("upload_worksheet_expected_columns_count")

    @property
    def upload_worksheet_urls_column_index(self) -> int:
        return self.get_section().getint("upload_worksheet_urls_column_index")
