from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log, waiter
from selenium.webdriver.common.by import By

from scrape_jobs.common.jobs_page import JobsPage, ISearchContext, IResultsContext
from scrape_jobs.sites.seek_com_au import seek_job


class SeekSearch(ISearchContext):
    INPUT_WHAT = By.ID, "SearchBar__Keywords"

    INPUT_WHERE = By.ID, "SearchBar__Where"

    INPUT_WHERE_AUTOCOMPLETE_ITEM = By.CSS_SELECTOR, "div[id='react-autowhatever-1'] ul > li"

    RESULTS_CONTAINER = By.CSS_SELECTOR, "div[data-automation='searchResults']"

    SEARCH_BUTTON = By.CSS_SELECTOR, "button[data-automation='searchButton']"

    SORT_BY_COMBO = By.CSS_SELECTOR, "label#SortedByLabel"

    SORT_BY_COMBO_DATE_ITEM = By.XPATH, "//ul[@role='navigation'][@aria-label='Sort By']/li[contains(.,'Date')]"

    SORT_ORDER = By.CSS_SELECTOR, "label#SortedByLabel > strong"

    TOTAL_RESULTS_COUNT_LABEL = By.CSS_SELECTOR, "strong[data-automation='totalJobsCount']"

    def set_what(self, what: str):
        log.info("setting search 'WHAT' to: '%s'", what)
        search_input = driver.wait_until_visible_element(self.INPUT_WHAT)
        search_input.clear()
        search_input.send_keys(what)

    def get_what(self) -> str:
        return driver.wait_until_visible_element(self.INPUT_WHAT).text

    def set_where(self, where: str):
        log.info("setting search 'WHERE' to: '%s'", where)
        location_input = driver.wait_until_visible_element(self.INPUT_WHERE)
        location_input.clear()
        location_input.send_keys(where)
        driver.click_element(self.INPUT_WHERE_AUTOCOMPLETE_ITEM)

    def get_where(self) -> str:
        return driver.wait_until_visible_element(self.INPUT_WHERE).text

    def set_search_params(self, **params):
        what = params.pop("what", "")
        self.set_what(what)

        where = params.pop("where", "")
        self.set_where(where)

    def sort_by_date(self):
        log.info("sorting results by 'Date'")
        driver.click_element(self.SORT_BY_COMBO)
        driver.click_element(self.SORT_BY_COMBO_DATE_ITEM)

    def get_sort_order(self) -> str:
        if driver.is_visible(self.SORT_ORDER):
            return driver.wait_until_visible_element(self.SORT_ORDER).text.strip().capitalize()
        return ""

    def trigger_search(self):
        log.info("triggering search...")
        driver.click_element(self.SEARCH_BUTTON)
        self.wait_for_search_complete()
        log.info("total results count: [%s]", self.get_total_results_count())
        self.sort_by_date()

    def get_total_results_count(self) -> int:
        try:
            count = driver.wait_until_visible_element(self.TOTAL_RESULTS_COUNT_LABEL).text.strip()
            return int(count.replace(",", "").replace(".", "").strip())
        except:
            return 0

    def wait_for_search_complete(self):
        """Just waits for the results container to appear, without caring for actual result items"""

        log.info("waiting for search to complete...")

        def search_complete() -> bool:
            return driver.is_visible(self.RESULTS_CONTAINER)

        waiter.poll_for_result(search_complete, timeout_seconds=30, default=TimeoutError)


class SeekResults(IResultsContext):
    NEXT_PAGE_BUTTON = By.CSS_SELECTOR, "a[data-automation='page-next']"

    RESULT_ITEM = By.CSS_SELECTOR, "div[data-automation='searchResults'] article"

    def has_results(self) -> bool:
        return driver.is_visible(self.RESULT_ITEM)

    def has_next_page(self) -> bool:
        return driver.is_visible(self.NEXT_PAGE_BUTTON)

    def get_visible_results(self) -> List[dict]:
        return [seek_job.parse_result_element(e)
                for e
                in driver.wait_until_visible_elements(self.RESULT_ITEM)]

    def get_current_page_number(self) -> str:
        try:
            pagination_container = driver.wait_until_visible_element(self.NEXT_PAGE_BUTTON).parent_element
            active_buttons = [child
                              for child
                              in pagination_container.child_elements
                              if ((child.tag_name == "span") and (not child.has_child_elements))]
            return active_buttons[0].text.strip()
        except:
            return ""

    def go_to_next_page(self):
        log.info("moving to next results page...")
        driver.click_element(self.NEXT_PAGE_BUTTON)


class SeekPage(SeekSearch, SeekResults, JobsPage):
    def __init__(self):
        super().__init__(url_domain="https://www.seek.com.au/", url_path="/")
