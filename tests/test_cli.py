from unittest import mock

from scrape_jobs import cli


def test_main_processes_args():
    site = "seek.au.com"
    config_file = "scrape.ini"
    with mock.patch("scrape_jobs.cli.scrape") as mock_method:
        cli.main([site, config_file])
        mock_method.assert_called_once_with(site, config_file)
