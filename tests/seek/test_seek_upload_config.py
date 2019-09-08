from configparser import ConfigParser
from unittest.case import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.sites.seek_com_au.seek_config import SeekUploadConfig


class TestSeekUploadConfig(TestCase):

    def setUp(self) -> None:
        self.config = SeekUploadConfig(sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        config = SeekUploadConfig(ConfigParser())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_seek_upload_config(self):
        self.assertEqual("jobs_stats_data", self.config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", self.config.upload_spreadsheet_json)
        self.assertEqual(0, self.config.upload_worksheet_index)
        self.assertEqual(8, self.config.upload_worksheet_expected_columns_count)
        self.assertEqual(7, self.config.upload_worksheet_urls_column_index)
