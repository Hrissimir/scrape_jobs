from configparser import ConfigParser
from unittest import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.common.upload_config import UploadConfig


class TestUploadConfig(TestCase):

    def setUp(self) -> None:
        self.config = UploadConfig("DEFAULT", sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        with self.assertRaises(AssertionError):
            UploadConfig("DEFAULT", ConfigParser()).assert_valid()

    def test_upload_config(self):
        config = self.config
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(-1, config.upload_worksheet_index)
        self.assertEqual(-1, config.upload_worksheet_expected_columns_count)
        self.assertEqual(-1, config.upload_worksheet_urls_column_index)
