from unittest import TestCase

from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs.sites.seek_com_au.seek_page import SeekPage
from scrape_jobs.sites.seek_com_au.seek_result import SeekResult


class TestSeekPage(TestCase):
    KEYWORDS = "manager"
    LOCATION = "All Sydney NSW"
    SORT_BY = "Date"

    @classmethod
    def setUpClass(cls) -> None:
        log.init()

    def setUp(self):
        driver.start_chrome()
        self.addCleanup(driver.quit)
        self.page = SeekPage()
        self.page.go_to()

    def test_can_get_set_search_keywords(self):
        self.page.set_search_keywords(self.KEYWORDS)
        self.assertEqual(self.page.get_search_keywords(), self.KEYWORDS)

    def test_can_get_set_search_location(self):
        self.page.set_search_location(self.LOCATION)
        self.assertEqual(self.page.get_search_location(), self.LOCATION)

    def test_can_trigger_search_and_wait_for_results(self):
        self.test_can_get_set_search_keywords()
        self.test_can_get_set_search_location()
        self.page.trigger_search()
        self.assertTrue(self.page.wait_for_search_results())

    def test_can_sort_by_date(self):
        self.test_can_trigger_search_and_wait_for_results()
        self.page.set_sort_by(self.SORT_BY)
        self.assertTrue(self.page.wait_for_search_results())
        self.assertEqual(self.page.get_sort_by(), self.SORT_BY)

    def test_can_get_visible_results(self):
        self.test_can_sort_by_date()
        results = self.page.get_visible_results()
        self.assertTrue(len(results) > 1)
        for r in results:
            self.assertIsInstance(r, SeekResult)

    def test_can_get_visible_results_data(self):
        self.test_can_sort_by_date()
        results_data = self.page.get_visible_results_data()
        self.assertTrue(len(results_data) > 1)
        for r in results_data:
            self.assertIsInstance(r, dict)

        # Bonus: log them pretty
        from tabulate import tabulate
        table_headers = [key.upper() for key in results_data[0].keys()]
        table_data = [d.values() for d in results_data]
        table = tabulate(tabular_data=table_data, headers=table_headers, tablefmt="fancy_grid")
        log.debug(f"Results:\n{table}")

    def test_can_go_to_next_page(self):
        self.test_can_trigger_search_and_wait_for_results()
        current_page = self.page.get_current_page_number()
        self.assertEqual(current_page, "1")

        self.page.go_to_next_page()
        self.page.wait_for_search_results()
        current_page = self.page.get_current_page_number()
        self.assertEqual(current_page, "2")

        self.page.go_to_next_page()
        self.page.wait_for_search_results()
        current_page = self.page.get_current_page_number()
        self.assertEqual(current_page, "3")
