import os
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, mock

from scrape_jobs.common import scrape_config

SAMPLE_CONFIG_PRINT = """
[DEFAULT]
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to secrets.json file.
upload_worksheet_index = 0
max_post_age_days = 2
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d %H:%M

[seek.com.au]
upload_worksheet_index = 0
max_post_age_days = 2
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d %H:00
what = Replace with search query
where = All Sydney NSW
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to secrets.json file.

[linkedin.com]
upload_worksheet_index = 1
max_post_age_days = 2
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d
keywords = Replace with search query
location = Sydney, New South Wales, Australia
date_posted = Past Month
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to secrets.json file.
"""


class TestScrapeConfig(TestCase):

    def test_get_sample_config(self):
        config = scrape_config.get_sample_config()
        assert isinstance(config, ConfigParser)

    def test_print_sample_config(self):
        config = scrape_config.get_sample_config()
        with mock.patch("sys.stdout", new=StringIO()) as fake_out:
            scrape_config.print_config(config)
            self.assertEqual(SAMPLE_CONFIG_PRINT, fake_out.getvalue())

    def test_write_config_with_param(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir).joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
            scrape_config.write_config(str(file_path))
            self.assertTrue(file_path.exists(), msg=f"No config was written to {str(file_path)} !")
            self.assertEqual(scrape_config.SAMPLE_CONFIG_CONTENTS, file_path.read_text())

    def test_write_config_no_param(self):
        cwd = str(Path.cwd())
        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            self.addCleanup(lambda: os.chdir(cwd))
            scrape_config.write_config()
            expected_file_path = Path.cwd().joinpath(scrape_config.SAMPLE_CONFIG_FILENAME)
            self.assertTrue(expected_file_path.exists(), "No config file was written to cwd!")
            self.assertEqual(scrape_config.SAMPLE_CONFIG_CONTENTS, expected_file_path.read_text())
