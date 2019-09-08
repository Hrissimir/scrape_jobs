from configparser import ConfigParser
from unittest import TestCase

from scrape_jobs.common.sample_config import get_config, write_to
from scrape_jobs.sites.linkedin_com.linkedin_config import LinkedinScrapeConfig, LinkedinUploadConfig
from scrape_jobs.sites.seek_com_au.seek_config import SeekScrapeConfig, SeekUploadConfig


class TestScrapeConfig(TestCase):

    def test_seek_config_is_present_and_properly_filled(self):
        config = SeekScrapeConfig(get_config())
        self.assertTrue(config.is_present())
        config.assert_valid()

    def test_seek_config_is_not_present_and_not_properly_filled(self):
        config = SeekScrapeConfig(ConfigParser())
        self.assertFalse(config.is_present())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_seek_scrape_config(self):
        scrape_config = SeekScrapeConfig(get_config())

        self.assertTrue(scrape_config.driver_headless)
        self.assertEqual(2, scrape_config.max_post_age_days)

        self.assertEqual("Australia/Sydney", scrape_config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M", scrape_config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d %H:00", scrape_config.posted_timestamp_format)
        self.assertEqual("Replace with search query", scrape_config.what)
        self.assertEqual("All Sydney NSW", scrape_config.where)
        expected_params = dict(what="Replace with search query", where="All Sydney NSW")
        self.assertDictEqual(expected_params, scrape_config.get_search_params())

    def test_seek_upload_config(self):
        upload_config = SeekUploadConfig(get_config())
        self.assertEqual("jobs_stats_data", upload_config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", upload_config.upload_spreadsheet_json)
        self.assertEqual(0, upload_config.upload_worksheet_index)
        self.assertEqual(8, upload_config.upload_worksheet_expected_columns_count)
        self.assertEqual(7, upload_config.upload_worksheet_urls_column_index)

    def test_linkedin_scrape_config_is_present(self):
        config = LinkedinScrapeConfig(get_config())
        self.assertTrue(config.is_present())
        config.assert_valid()

    def test_linkedin_config_is_not_present_and_not_properly_filled(self):
        config = SeekScrapeConfig(ConfigParser())
        self.assertFalse(config.is_present())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_linkedin_scrape_config(self):
        config = LinkedinScrapeConfig(get_config())

        self.assertEqual(14, config.max_post_age_days)
        self.assertTrue(config.driver_headless)
        self.assertEqual("Australia/Sydney", config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M", config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d", config.posted_timestamp_format)
        self.assertEqual("Replace with exact search keywords as in the UI autocomplete", config.keywords)
        self.assertEqual("Sydney, New South Wales, Australia", config.location)
        self.assertEqual("Past Month", config.date_posted)
        expected_params = dict(keywords="Replace with exact search keywords as in the UI autocomplete",
                               location="Sydney, New South Wales, Australia",
                               date_posted="Past Month")
        self.assertDictEqual(expected_params, config.get_search_params())

    def test_linkedin_upload_config(self):
        config = LinkedinUploadConfig(get_config())
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(1, config.upload_worksheet_index)
        self.assertEqual(6, config.upload_worksheet_expected_columns_count)
        self.assertEqual(6, config.upload_worksheet_urls_column_index)
