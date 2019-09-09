from datetime import timedelta
from unittest import TestCase

from hed_utils.support import time_tool

from scrape_jobs.common.result_predicates import MaxDaysAge


class MaxDaysAgeTest(TestCase):

    def test_create_instance(self):
        predicate = MaxDaysAge(5)
        self.assertIsNotNone(predicate)

    def test_create_instance_bad_params(self):
        with self.assertRaises(ValueError):
            MaxDaysAge(-1)
        with self.assertRaises(ValueError):
            MaxDaysAge(0)

        with self.assertRaises(TypeError):
            MaxDaysAge("15")

        with self.assertRaises(TypeError):
            MaxDaysAge(None)

    def test_check_matching_job(self):
        job = dict(utc_datetime=(time_tool.utc_moment() - timedelta(days=2)))
        predicate = MaxDaysAge(3)
        self.assertTrue(predicate(job))

    def test_check_mismatching_job(self):
        job = dict(utc_datetime=(time_tool.utc_moment() - timedelta(days=2)))
        predicate = MaxDaysAge(1)
        self.assertFalse(predicate(job))

    def test_check_job_with_no_utc_datetime(self):
        job = dict()
        predicate = MaxDaysAge(2)
        self.assertFalse(predicate(job))
