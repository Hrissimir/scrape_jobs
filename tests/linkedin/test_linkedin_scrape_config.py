from configparser import ConfigParser
from unittest.case import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.sites.linkedin_com.linkedin_config import LinkedinScrapeConfig


class TestLinkedinScrapeConfig(TestCase):
    def setUp(self) -> None:
        self.config = LinkedinScrapeConfig(sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        config = LinkedinScrapeConfig(ConfigParser())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_linkedin_scrape_config(self):
        config = self.config

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
