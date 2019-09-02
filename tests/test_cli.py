from unittest import mock

from scrape_jobs import scrape_jobs_cli


def test_main_processes_args():
    site = "seek.com.au"
    config_file = "scrape.ini"
    with mock.patch("scrape_jobs.scrape_jobs_cli.scrape") as mock_method:
        scrape_jobs_cli.main([site, config_file])
        mock_method.assert_called_once_with(site, config_file)


def test_scrape_seek():
    site = "seek.com.au"
    config_file = "scrape.ini"
    with mock.patch("scrape_jobs.sites.seek_com_au.seek_scraper.start") as mock_method:
        scrape_jobs_cli.main([site, config_file])
        mock_method.assert_called_once_with(config_file)


def test_scrape_linkedin():
    site = "linkedin.com"
    config_file = "scrape.ini"
    with mock.patch("scrape_jobs.sites.linkedin_com.linkedin_scraper.start") as mock_method:
        scrape_jobs_cli.main([site, config_file])
        mock_method.assert_called_once_with(config_file)
