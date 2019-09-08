from configparser import ConfigParser
from unittest import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.common.scrape_config import ScrapeConfig


class TestScrapeConfig(TestCase):

    def setUp(self) -> None:
        self.config = ScrapeConfig("DEFAULT", ScrapeConfig.KEYS, sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        with self.assertRaises(AssertionError):
            ScrapeConfig("DEFAULT", ScrapeConfig.KEYS, ConfigParser()).assert_valid()

    def test_scrape_config(self):
        self.assertEqual(1, self.config.max_post_age_days)
        self.assertEqual("Australia/Sydney", self.config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M:%S:%f", self.config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d %H:%M:%S:%f", self.config.posted_timestamp_format)
        self.assertFalse(self.config.driver_headless)

    def test_get_search_params(self):
        with self.assertRaises(NotImplementedError):
            self.config.get_search_params()
