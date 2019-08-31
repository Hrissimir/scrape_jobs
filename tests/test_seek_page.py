from unittest import TestCase, mock

from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs.sites.seek_com_au.seek_page import SeekPage


class TestSeekPage(TestCase):
    WHAT = "manager"
    WHERE = "All Sydney NSW"

    @classmethod
    def setUpClass(cls) -> None:
        log.init()

    def setUp(self):
        driver.start_chrome()
        self.addCleanup(driver.quit)
        self.page = SeekPage()
        self.page.go_to()

    def test_set_search_params_calls_relevant_methods(self):
        with mock.patch("scrape_jobs.sites.seek_com_au.seek_page.SeekSearch.set_what") as mock_set_what:
            with mock.patch("scrape_jobs.sites.seek_com_au.seek_page.SeekSearch.set_where") as mock_set_where:
                self.page.set_search_params(what=self.WHAT, where=self.WHERE)
                mock_set_what.assert_called_once_with(self.WHAT)
                mock_set_where.assert_called_once_with(self.WHERE)

    def test_can_set_what(self):
        self.page.set_what(self.WHAT)
        self.assertEqual(self.page.get_what(), self.WHAT)

    def test_can_set_where(self):
        self.page.set_where(self.WHERE)
        self.assertEqual(self.page.get_where(), self.WHERE)

    def test_trigger_search(self):
        # navigate to page - no results list & next page
        self.assertFalse(self.page.has_results())
        self.assertFalse(self.page.has_next_page())

        # trigger empty search & wait
        self.page.trigger_search()
        self.page.wait_for_search_complete()

        # results and next page had appeared
        self.assertTrue(self.page.has_results())
        self.assertTrue(self.page.has_next_page())

        # sort order was silently changed to Date
        self.assertEqual(self.page.get_sort_order(), "Date")

    def test_can_get_visible_results(self):
        self.page.set_search_params(what=self.WHAT, where=self.WHERE)
        self.page.trigger_search()

        results = self.page.get_visible_results()
        self.assertTrue(len(results) > 1)
        for r in results:
            self.assertIsInstance(r, dict)

    def test_can_go_to_next_page(self):
        self.page.set_search_params(what=self.WHAT, where=self.WHERE)
        self.page.trigger_search()

        first_page = self.page.get_current_page_number()
        self.assertEqual(first_page, "1")
        self.page.go_to_next_page()
        self.page.wait_for_search_complete()

        second_page = self.page.get_current_page_number()
        self.assertEqual(second_page, "2")
        self.page.go_to_next_page()
        self.page.wait_for_search_complete()

        third_page = self.page.get_current_page_number()
        self.assertEqual(third_page, "3")
