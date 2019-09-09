from unittest import TestCase, mock

from bs4 import BeautifulSoup
from hed_utils.support import time_tool

from scrape_jobs.common.job_result import JobResult


class JobResultTest(TestCase):

    def test_keys(self):
        expected_keys = ["utc_datetime", "location", "title", "company", "url"]
        self.assertListEqual(expected_keys, JobResult.keys())

    def test_constructor_param(self):
        JobResult(BeautifulSoup(features="lxml"))
        with self.assertRaises(TypeError):
            JobResult(None)
        with self.assertRaises(TypeError):
            JobResult("")

    def test_as_dict(self):
        utc_datetime = time_tool.utc_moment()
        location = "Bulgaria"
        title = "QA Automation Specialist"
        company = "Home Projects Ltd."
        url = "my.missing.page.com"
        expected_dict = dict(utc_datetime=utc_datetime,
                             location=location,
                             title=title,
                             company=company,
                             url=url)

        result = JobResult(BeautifulSoup(features="lxml"))
        with mock.patch("scrape_jobs.common.job_result.JobResult.values") as mock_values:
            mock_values.side_effect = [list(expected_dict.keys())]
            result.as_dict()
            mock_values.assert_called_once()

        with mock.patch("scrape_jobs.common.job_result.JobResult.get_utc_datetime") as mock_get_utc_datetime:
            mock_get_utc_datetime.side_effect = [utc_datetime]
            with mock.patch("scrape_jobs.common.job_result.JobResult.get_location") as mock_get_location:
                mock_get_location.side_effect = [location]
                with mock.patch("scrape_jobs.common.job_result.JobResult.get_title") as mock_get_title:
                    mock_get_title.side_effect = [title]
                    with mock.patch("scrape_jobs.common.job_result.JobResult.get_company") as mock_get_company:
                        mock_get_company.side_effect = [company]
                        with mock.patch("scrape_jobs.common.job_result.JobResult.get_url") as mock_get_url:
                            mock_get_url.side_effect = [url]

                            data = result.as_dict()
                            mock_get_utc_datetime.assert_called_once()
                            mock_get_location.assert_called_once()
                            mock_get_title.assert_called_once()
                            mock_get_company.assert_called_once()
                            mock_get_url.assert_called_once()
                            self.assertDictEqual(expected_dict, data)
