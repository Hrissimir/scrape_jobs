import logging

from hed_utils.selenium import FindBy

from scrape_jobs.pages.base_page import BasePage
from scrape_jobs.parsers import seek_parser

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class SeekPage(BasePage):
    URL = "https://www.seek.com.au/"

    def __init__(self, search_params: dict):
        super().__init__(self.URL, search_params)
        self.what_input = FindBy.CSS_SELECTOR("input#keywords-input")
        self.where_input = FindBy.CSS_SELECTOR("input#SearchBar__Where")
        self.where_autocomplete = FindBy.XPATH(
            "//input[contains(@id,'SearchBar__Where')]/../..//ul//li[contains(@id,'react-autowhatever')]")
        self.search_button = FindBy.CSS_SELECTOR("button[data-automation='searchButton']")
        self.search_results = FindBy.TAG_NAME("article", visible_only=False)
        self.next_page_button = FindBy.CSS_SELECTOR("a[data-automation='page-next']")

    def enter_search_params(self):
        super().enter_search_params()

        what_value = self.search_params.get("what", "")
        _log.info("entering 'what': '%s'", what_value)
        self.what_input.click()
        self.what_input.send_keys(what_value)
        self.driver.wait_for_page_load()

        where_value = self.search_params.get("where", "")
        _log.info("entering 'where': '%s'", where_value)
        self.where_input.click()
        self.where_input.send_keys(where_value)
        self.where_autocomplete.click()
        self.driver.wait_for_page_load()

    def trigger_search(self):
        super().trigger_search()
        self.search_button.click()

    def wait_for_results(self):
        super().wait_for_results()
        return self.search_results.is_present(timeout=20)

    def has_more_results(self) -> bool:
        super().has_more_results()
        return self.next_page_button.is_visible()

    def load_more_results(self):
        super().load_more_results()
        self.next_page_button.click()

    def get_visible_jobs(self) -> list:
        super().get_visible_jobs()
        return seek_parser.parse_jobs(self.driver.page_source)
