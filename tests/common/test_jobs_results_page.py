from unittest import TestCase

from scrape_jobs.common.jobs_results_page import JobsResultsPage


class JobsResultsPageTest(TestCase):
    def setUp(self) -> None:
        self.page = JobsResultsPage()

    def tearDown(self) -> None:
        self.page = None

    def test_has_results(self):
        with self.assertRaises(NotImplementedError):
            self.page.has_results()

    def test_has_next_page(self):
        with self.assertRaises(NotImplementedError):
            self.page.has_next_page()

    def test_get_visible_results(self):
        with self.assertRaises(NotImplementedError):
            self.page.get_visible_results()

    def test_go_to_next_page(self):
        with self.assertRaises(NotImplementedError):
            self.page.go_to_next_page()
