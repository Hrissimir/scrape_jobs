from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from unittest import TestCase

from bs4 import BeautifulSoup
from hed_utils.support import time_tool

from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult


def get_source() -> str:
    file_path = Path(__file__).parent.joinpath("static").joinpath("linkedin_job_result.html")
    return file_path.read_text(encoding="utf-8")


class TestLinkedinJobResult(TestCase):
    def setUp(self) -> None:
        self.job = LinkedinJobResult(BeautifulSoup(get_source(), "lxml"))

    def tearDown(self) -> None:
        self.job = None

    def test_get_utc_datetime(self):
        expected = time_tool.localize(datetime(2019, 9, 6, 0, 0), "UTC")
        actual = self.job.get_utc_datetime()
        self.assertEqual(expected, actual)

    def test_get_location(self):
        expected = "Sofia, BG"
        actual = self.job.get_location()
        self.assertEqual(expected, actual)

    def test_get_title(self):
        expected = "Automation QA Engineer (Virtualization Backup)"
        actual = self.job.get_title()
        self.assertEqual(expected, actual)

    def test_get_company(self):
        expected = "Acronis"
        actual = self.job.get_company()
        self.assertEqual(expected, actual)

    def test_get_url(self):
        expected = \
            "https://bg.linkedin.com/jobs/view/automation-qa-engineer-virtualization-backup-at-acronis-1452801029"
        actual = self.job.get_url()
        self.assertEqual(expected, actual)

    def test_as_dict(self):
        expected = OrderedDict(
            utc_datetime=time_tool.localize(datetime(2019, 9, 6, 0, 0), "UTC"),
            location="Sofia, BG",
            title="Automation QA Engineer (Virtualization Backup)",
            company="Acronis",
            url="https://bg.linkedin.com/jobs/view/automation-qa-engineer-virtualization-backup-at-acronis-1452801029",
        )
        actual = self.job.as_dict()
        self.assertDictEqual(expected, actual)

    def test_empty_soup(self):
        soup = BeautifulSoup(features="lxml")
        job = LinkedinJobResult(soup)
        expected = OrderedDict(
            utc_datetime=None,
            location=None,
            title=None,
            company=None,
            url=None)
        actual = job.as_dict()
        self.assertDictEqual(expected, actual)
