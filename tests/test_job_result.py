from unittest import TestCase

from scrape_jobs.common.job_result import JobResult


class JobResultTest(TestCase):

    def test_keys(self):
        expected_keys = ["utc_datetime", "location", "title", "company", "url"]
        self.assertListEqual(expected_keys, JobResult.keys())
