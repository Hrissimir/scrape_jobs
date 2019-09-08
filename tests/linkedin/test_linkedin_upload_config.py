from configparser import ConfigParser
from unittest.case import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.sites.linkedin_com.linkedin_config import LinkedinUploadConfig


class TestLinkedinUploadConfig(TestCase):
    def setUp(self) -> None:
        self.config = LinkedinUploadConfig(sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        config = LinkedinUploadConfig(ConfigParser())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_linkedin_upload_config(self):
        config = self.config
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(1, config.upload_worksheet_index)
        self.assertEqual(6, config.upload_worksheet_expected_columns_count)
        self.assertEqual(6, config.upload_worksheet_urls_column_index)
