import logging
from typing import Any, Dict

from hed_utils.selenium import FindBy

from scrape_jobs.base.data_collection import Page

__all__ = ["SeekPage"]

from scrape_jobs.seek import SeekJob

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class SeekPage(Page):
    PAGE_URL = "https://www.seek.com.au/"

    def __init__(self, search_params: Dict[str, Any], max_post_age_days: int, max_attempts: int):
        super().__init__(search_params, max_post_age_days, max_attempts, parser=SeekJob())
        self.search_results = FindBy.TAG_NAME("article", visible_only=False)
        self.search_button = FindBy.CSS_SELECTOR("button[data-automation='searchButton']")
        self.next_page_button = FindBy.CSS_SELECTOR("a[data-automation='page-next']")
        self.what_input = FindBy.ID("keywords-input")
        self.where_input = FindBy.CSS_SELECTOR("input#SearchBar__Where")
        self.where_autocomplete = FindBy.XPATH(
            "//input[contains(@id,'SearchBar__Where')]/../..//ul//li[contains(@id,'react-autowhatever')]")

    def perform_search(self):
        self.set_search_params()
        self.search_button.click()
        self.wait_for_results_to_load()
        self.sort_by_date()

    def sort_by_date(self):
        _log.info("sorting results by date...")
        sort_by = FindBy.XPATH("//label[contains(@id,'sortby-label')]")
        sort_by.click()
        date_option = FindBy.XPATH(f"//label[contains(@id,'sortby-label')]/../ul/li[contains(.,'Date')]")
        date_option.click()
        self.driver.wait_for_page_load()

    def set_search_params(self):
        _log.info("setting search params...")
        search_params = self.search_params

        what_value = search_params.get("what", "")
        _log.info("entering 'what': '%s'", what_value)
        self.what_input.click()
        self.what_input.send_keys(what_value)
        self.driver.wait_for_page_load()

        where_value = search_params.get("where", "")
        _log.info("entering 'where': '%s'", where_value)
        self.where_input.click()
        self.where_input.send_keys(where_value)
        self.where_autocomplete.click()
        self.driver.wait_for_page_load()

    def wait_for_results_to_load(self):
        self.driver.wait_for_page_load()
        return self.search_results.is_visible(timeout=15)

    def has_more_results(self) -> bool:
        return self.next_page_button.is_visible(timeout=5)

    def load_more_results(self):
        if self.search_results.is_visible():
            last_result = self.search_results[-1]
            last_result.scroll_into_view()

        self.next_page_button.click()
