import os
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, mock

from hed_utils.support import log

from scrape_jobs.common import scrape_config

SAMPLE_CONFIG_PRINT = """
[DEFAULT]
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.
upload_worksheet_index = 0
max_post_age_days = 2
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M:%S:%f
posted_timestamp_format = %Y-%m-%d %H:%M:%S:%f

[seek.com.au]
upload_worksheet_index = 0
max_post_age_days = 3
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d %H:00
what = Replace with search query
where = All Sydney NSW
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.

[linkedin.com]
upload_worksheet_index = 1
max_post_age_days = 14
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d
keywords = Replace with exact search keywords as in the UI autocomplete
location = Sydney, New South Wales, Australia
date_posted = Past Month
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.
"""


class TestSampleConfig(TestCase):

    def test_get_sample_config(self):
        config = scrape_config.get_sample_config()
        assert isinstance(config, ConfigParser)

    def test_print_sample_config(self):
        config = scrape_config.get_sample_config()
        with mock.patch("sys.stdout", new=StringIO()) as fake_out:
            scrape_config.print_config(config)
            self.assertEqual(SAMPLE_CONFIG_PRINT, fake_out.getvalue())

    def test_format_config(self):
        config = scrape_config.get_sample_config()
        self.assertEqual(SAMPLE_CONFIG_PRINT, scrape_config.format_config(config))

    def test_write_sample_config_with_file_path_param(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir).joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
            scrape_config.write_sample_config(str(file_path))
            self.assertTrue(file_path.exists(), msg=f"No config was written to {str(file_path)} !")
            self.assertEqual(scrape_config.SAMPLE_CONFIG_CONTENTS, file_path.read_text())

    def test_write_sample_config_no_file_path_param_writes_in_cwd(self):
        cwd = str(Path.cwd())
        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            self.addCleanup(lambda: os.chdir(cwd))
            scrape_config.write_sample_config()
            expected_file_path = Path.cwd().joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
            self.assertTrue(expected_file_path.exists(), "No config file was written to cwd!")
            self.assertEqual(scrape_config.SAMPLE_CONFIG_CONTENTS, expected_file_path.read_text())

    def test_read_config_with_file_path_param(self):
        with TemporaryDirectory() as tempdir:
            cfg_path = Path(tempdir).joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
            scrape_config.write_sample_config(str(cfg_path))
            self.assertEqual(scrape_config.get_sample_config(),
                             scrape_config.read_config(str(cfg_path)))

    def test_read_config_with_no_file_path_param_reads_from_cwd(self):
        cwd = str(Path.cwd())
        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            self.addCleanup(lambda: os.chdir(cwd))
            scrape_config.write_sample_config()
            self.assertEqual(scrape_config.get_sample_config(),
                             scrape_config.read_config())


class TestScrapeConfig(TestCase):
    def setUp(self) -> None:
        log.init()
        self.sample_config = scrape_config.get_sample_config()

    def tearDown(self) -> None:
        self.sample_config = None

    def test_default_section_is_present_and_properly_filled(self):
        config = scrape_config.ScrapeConfig(self.sample_config)
        self.assertTrue(config.is_present())
        self.assertTrue(config.is_properly_filled())
        config.assert_is_valid()

    def test_default_config_is_present_but_not_properly_filled(self):
        config = scrape_config.ScrapeConfig(ConfigParser())
        self.assertTrue(config.is_present())
        self.assertFalse(config.is_properly_filled())
        with self.assertRaises(AssertionError):
            config.assert_is_valid()

    def test_default_config_properties(self):
        config = scrape_config.ScrapeConfig(self.sample_config)
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(0, config.upload_worksheet_index)
        self.assertEqual(2, config.max_post_age_days)
        self.assertEqual("Australia/Sydney", config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M:%S:%f", config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d %H:%M:%S:%f", config.posted_timestamp_format)

    def test_seek_config_is_present_and_properly_filled(self):
        config = scrape_config.SeekComAuConfig(self.sample_config)
        self.assertTrue(config.is_present())
        self.assertTrue(config.is_properly_filled())
        config.assert_is_valid()

    def test_seek_config_is_not_present_and_not_properly_filled(self):
        config = scrape_config.SeekComAuConfig(ConfigParser())
        self.assertFalse(config.is_present())
        with self.assertRaises(AssertionError):
            self.assertFalse(config.is_properly_filled())
        with self.assertRaises(AssertionError):
            config.assert_is_valid()

    def test_seek_config_properties(self):
        config = scrape_config.SeekComAuConfig(self.sample_config)
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(0, config.upload_worksheet_index)
        self.assertEqual(3, config.max_post_age_days)
        self.assertEqual("Australia/Sydney", config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M", config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d %H:00", config.posted_timestamp_format)
        self.assertEqual("Replace with search query", config.what)
        self.assertEqual("All Sydney NSW", config.where)

    def test_linkedin_config_is_present_and_properly_filled(self):
        config = scrape_config.LinkedinComConfig(self.sample_config)
        self.assertTrue(config.is_present())
        self.assertTrue(config.is_properly_filled())
        config.assert_is_valid()

    def test_linkedin_config_is_not_present_and_not_properly_filled(self):
        config = scrape_config.SeekComAuConfig(ConfigParser())
        self.assertFalse(config.is_present())
        with self.assertRaises(AssertionError):
            self.assertFalse(config.is_properly_filled())
        with self.assertRaises(AssertionError):
            config.assert_is_valid()

    def test_linkedin_config_properties(self):
        config = scrape_config.LinkedinComConfig(self.sample_config)
        self.assertEqual("jobs_stats_data", config.upload_spreadsheet_name)
        self.assertEqual("Replace with path to default secrets.json file.", config.upload_spreadsheet_json)
        self.assertEqual(1, config.upload_worksheet_index)
        self.assertEqual(14, config.max_post_age_days)
        self.assertEqual("Australia/Sydney", config.timezone)
        self.assertEqual("%Y-%m-%d %H:%M", config.scraped_timestamp_format)
        self.assertEqual("%Y-%m-%d", config.posted_timestamp_format)
        self.assertEqual("Replace with exact search keywords as in the UI autocomplete", config.keywords)
        self.assertEqual("Sydney, New South Wales, Australia", config.location)
        self.assertEqual("Past Month", config.date_posted)
