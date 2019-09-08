import os
from configparser import ConfigParser
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.case import TestCase

from hed_utils.support import config_tool

from scrape_jobs.common import sample_config

SAMPLE_CONFIG_PRINT = """
[DEFAULT]
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.
upload_worksheet_index = -1
upload_worksheet_expected_columns_count = -1
upload_worksheet_urls_column_index = -1
max_post_age_days = 1
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M:%S:%f
posted_timestamp_format = %Y-%m-%d %H:%M:%S:%f
driver_headless = no

[seek.com.au]
upload_worksheet_index = 0
upload_worksheet_expected_columns_count = 8
upload_worksheet_urls_column_index = 7
max_post_age_days = 2
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d %H:00
what = Replace with search query
where = All Sydney NSW
driver_headless = yes
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.

[linkedin.com]
upload_worksheet_index = 1
upload_worksheet_expected_columns_count = 6
upload_worksheet_urls_column_index = 6
max_post_age_days = 14
timezone = Australia/Sydney
scraped_timestamp_format = %Y-%m-%d %H:%M
posted_timestamp_format = %Y-%m-%d
keywords = Replace with exact search keywords as in the UI autocomplete
location = Sydney, New South Wales, Australia
date_posted = Past Month
driver_headless = yes
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to default secrets.json file.
"""


class TestSampleConfig(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_get_sample_config(self):
        config = sample_config.get_config()
        assert isinstance(config, ConfigParser)

    def test_sample_config_contents(self):
        config = sample_config.get_config()
        contents = config_tool.format_config(config)
        self.assertEqual(SAMPLE_CONFIG_PRINT, contents)

    def test_write_sample_config_with_file_path_param(self):
        with TemporaryDirectory() as tempdir:
            file_path = Path(tempdir).joinpath(sample_config.FILENAME)
            sample_config.write_to(str(file_path))
            self.assertTrue(file_path.exists(), msg=f"No config was written to {str(file_path)} !")
            self.assertEqual(sample_config.CONTENTS.strip(), file_path.read_text(encoding="utf-8").strip())

    def test_write_sample_config_no_file_path_param_writes_in_cwd(self):
        cwd = str(Path.cwd())
        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            self.addCleanup(lambda: os.chdir(cwd))
            sample_config.write_to()
            expected_file_path = Path.cwd().joinpath(sample_config.FILENAME)
            self.assertTrue(expected_file_path.exists(), "No config file was written to cwd!")
            self.assertEqual(sample_config.CONTENTS, expected_file_path.read_text())

    def test_read_config_with_file_path_param(self):
        with TemporaryDirectory() as tempdir:
            cfg_path = Path(tempdir).joinpath(sample_config.FILENAME)
            sample_config.write_to(str(cfg_path))
            self.assertEqual(sample_config.get_config(), config_tool.read_config(str(cfg_path)))
