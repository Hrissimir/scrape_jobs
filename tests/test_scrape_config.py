import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from scrape_jobs.common import scrape_config


class TestScrapeConfig(TestCase):
    def test_get_sample_config(self):
        config = scrape_config.get_sample_config()
        scrape_config.assert_valid_config(config)

    def test_write_read_sample_config(self):
        cwd = str(Path.cwd())
        self.addCleanup(lambda: os.chdir(cwd))

        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            file = Path.cwd().joinpath("scrape_config.ini")
            scrape_config.write_config(str(file))
            assert file.exists()
            scrape_config.assert_valid_config(scrape_config.read_config(str(file)))

    def test_format_config(self):
        config = scrape_config.get_sample_config()
        expected = """[DEFAULT]
upload_spreadsheet_name = jobs_stats_data
upload_spreadsheet_json = Replace with path to secrets.json file.
upload_worksheet_index = 0

[seek.com.au]
what = Replace with search query
where = All Sydney NSW
days = 3
timezone = Australia/Sydney
upload_worksheet_index = 0""".strip()
        actual = scrape_config.format_config(config)
        self.assertEqual(expected, actual)
