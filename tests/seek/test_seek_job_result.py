from datetime import timedelta
from pathlib import Path
from unittest import TestCase

from bs4 import BeautifulSoup
from hed_utils.support import time_tool

from scrape_jobs.sites.seek_com_au.seek_job_result import SeekJobResult


def get_source() -> str:
    file_path = Path(__file__).parent.joinpath("static").joinpath("seek_job_result.html")
    return file_path.read_text(encoding="utf-8")


class TestSeekJobResult(TestCase):
    def setUp(self) -> None:
        self.job = SeekJobResult(BeautifulSoup(get_source(), "lxml"))

    def tearDown(self) -> None:
        self.job = None

    def test_get_utc_datetime(self):
        expected = time_tool.utc_moment() - timedelta(hours=8)
        actual = self.job.get_utc_datetime()
        allowed_delta_seconds = 1
        actual_delta_seconds = (abs((expected - actual).total_seconds()))
        self.assertTrue(actual_delta_seconds < allowed_delta_seconds)

    def test_get_location(self):
        expected = "Sydney, CBD, Inner West & Eastern Suburbs"
        actual = self.job.get_location()
        self.assertEqual(expected, actual)

    def test_get_title(self):
        expected = "Technical Lead - Android / Kotlin / iOS / Swift"
        actual = self.job.get_title()
        self.assertEqual(expected, actual)

    def test_get_company(self):
        expected = "Finite IT Recruitment Solutions"
        actual = self.job.get_company()
        self.assertEqual(expected, actual)

    def test_get_url(self):
        expected = "https://www.seek.com.au/job/39900475"
        actual = self.job.get_url()
        self.assertEqual(expected, actual)

    def test_get_classification(self):
        expected = "Information & Communication Technology, Developers/Programmers"
        actual = self.job.get_classification()
        self.assertEqual(expected, actual)

    def test_get_salary(self):
        expected = None
        actual = self.job.get_salary()
        self.assertEqual(expected, actual)
