from configparser import ConfigParser
from unittest.case import TestCase

from scrape_jobs.common import sample_config
from scrape_jobs.sites.seek_com_au.seek_config import SeekScrapeConfig


class TestSeekScrapeConfig(TestCase):

    def setUp(self) -> None:
        self.config = SeekScrapeConfig(sample_config.get_config())

    def tearDown(self) -> None:
        self.config = None

    def test_valid(self):
        self.config.assert_valid()

    def test_invalid(self):
        config = SeekScrapeConfig(ConfigParser())
        with self.assertRaises(AssertionError):
            config.assert_valid()

    def test_seek_scrape_config(self):
        self.assertTrue(self.config.driver_headless)
        self.assertEqual(2, self.config.max_post_age_days)

        self.assertEqual("Australia/Sydney", self.config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M", self.config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d %H:00", self.config.posted_timestamp_format)
        self.assertEqual("Replace with search query", self.config.what)
        self.assertEqual("All Sydney NSW", self.config.where)
        expected_params = dict(what="Replace with search query", where="All Sydney NSW")
        self.assertDictEqual(expected_params, self.config.get_search_params())
