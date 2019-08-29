import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from scrape_jobs import scrape_config


class TestScrapeConfig(TestCase):
    def test_get_sample_config(self):
        config = scrape_config.get_sample_config()
        scrape_config.assert_valid(config)

    def test_write_read_sample_config(self):
        cwd = str(Path.cwd())
        self.addCleanup(lambda: os.chdir(cwd))

        with TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            file = Path.cwd().joinpath("scrape_config.ini")
            scrape_config.write_config(str(file))
            assert file.exists()
            scrape_config.assert_valid(scrape_config.read_config(str(file)))
