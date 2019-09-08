from unittest import TestCase

from scrape_jobs.common.jobs_search_page import JobsSearchPage


class JobsSearchPageTest(TestCase):

    def setUp(self) -> None:
        self.page = JobsSearchPage()

    def tearDown(self) -> None:
        self.page = None

    def test_set_search_params(self):
        with self.assertRaises(NotImplementedError):
            self.page.set_search_params()

    def test_trigger_search(self):
        with self.assertRaises(NotImplementedError):
            self.page.trigger_search()

    def test_wait_for_search_complete(self):
        with self.assertRaises(NotImplementedError):
            self.page.wait_for_search_complete()
