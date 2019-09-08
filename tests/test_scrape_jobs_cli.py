import logging
import sys
from pathlib import Path
from unittest import mock

from scrape_jobs import scrape_jobs_cli
from scrape_jobs.common import scrape_config


def test_main_processes_args():
    entry_file = str(Path(scrape_jobs_cli.__file__))
    site = "seek.com.au"
    config_file = "scrape.ini"
    argv = [entry_file, site, config_file]
    with mock.patch.object(sys, "argv", argv):
        with mock.patch("scrape_jobs.scrape_jobs_cli.scrape") as mock_method:
            scrape_jobs_cli.run()
            mock_method.assert_called_once_with(site, config_file)


def test_scrape_seek():
    entry_file = str(Path(scrape_jobs_cli.__file__))
    site = "seek.com.au"
    config_file = "scrape.ini"
    argv = [entry_file, site, config_file]
    with mock.patch.object(sys, "argv", argv):
        with mock.patch("scrape_jobs.sites.seek_com_au.seek_scraper.start") as mock_method:
            scrape_jobs_cli.run()
            mock_method.assert_called_once_with(config_file)


def test_scrape_linkedin():
    entry_file = str(Path(scrape_jobs_cli.__file__))
    site = "linkedin.com"
    config_file = "scrape.ini"
    argv = [entry_file, site, config_file]
    with mock.patch.object(sys, "argv", argv):
        with mock.patch("scrape_jobs.sites.linkedin_com.linkedin_scraper.start") as mock_method:
            scrape_jobs_cli.run()
            mock_method.assert_called_once_with(config_file)


def test_init_config():
    expected_path = str(Path.cwd().joinpath(scrape_config.DEFAULT_FILENAME))
    with mock.patch("scrape_jobs.common.scrape_config.write_sample_config") as mock_method:
        scrape_jobs_cli.init_config()
        mock_method.assert_called_once_with(expected_path)


def test_init_logging_deletes_pre_existing_log():
    initial_contents = "initial contents"
    log_file = Path.cwd().joinpath(scrape_jobs_cli.LOG_FILE)
    if log_file.exists():
        log_file.unlink()
    log_file.write_text(initial_contents)
    scrape_jobs_cli.init_logging(logging.INFO)
    assert initial_contents != log_file.read_text(), "pre-existing log was not overwritten!"