from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from scrape_jobs.base.job_result import JobResult
from scrape_jobs.base.jobs_page import JobsPage
from scrape_jobs.sites.seek_com_au.seek_job_result import SeekJobResult


class SeekJobsPage(JobsPage):
    AUTOCOMPLETE_FIRST_OPTION = By.CSS_SELECTOR, "div[id='react-autowhatever-1'] ul > li"
    KEYWORDS_INPUT = By.ID, "SearchBar__Keywords"
    LOCATION_INPUT = By.ID, "SearchBar__Where"
    SEARCH_BUTTON = By.CSS_SELECTOR, "button[data-automation='searchButton']"
    SEARCH_RESULTS = By.CSS_SELECTOR, "div[data-automation='searchResults']"
    SORT_BY_LABEL = By.CSS_SELECTOR, "label[id='SortedByLabel']"
    SORT_BY_DROPDOWN_ITEM_XPATH_TEMPLATE = "//ul[@role='navigation'][@aria-label='Sort By']/li[contains(.,'{order}')]"
    SORT_BY_EFFECTIVE_VALUE = By.CSS_SELECTOR, "label[id='SortedByLabel'] > strong"
    RESULT_ITEM = By.CSS_SELECTOR, "div[data-automation='searchResults'] article"
    PAGINATION_NEXT = By.CSS_SELECTOR, "a[data-automation='page-next']"
    TOTAL_JOBS_FOUND = By.CSS_SELECTOR, "strong[data-automation='totalJobsCount']"

    def __init__(self):
        super().__init__(url_domain="https://www.seek.com.au/", url_path="/")

    def set_search_keywords(self, keywords: str):
        log.info("setting the search 'WHAT' input to: '%s'", keywords)
        search_input = driver.wait_until_visible_element(self.KEYWORDS_INPUT)
        search_input.clear()
        search_input.send_keys(keywords)

    def set_search_location(self, location: str):
        log.info("setting the search 'WHERE' input to: '%s'", location)
        location_input = driver.wait_until_visible_element(self.LOCATION_INPUT)
        location_input.clear()
        location_input.send_keys(location)
        driver.click_element(self.AUTOCOMPLETE_FIRST_OPTION)

    def enter_search_details(self, query: str, location: str):
        self.set_search_keywords(query)
        self.set_search_location(location)

    def get_sort_by(self) -> str:
        try:
            return driver.wait_until_visible_element(self.SORT_BY_EFFECTIVE_VALUE).text.capitalize()
        except:
            return ""

    def set_sort_by(self, order: str):
        order = order.capitalize()
        log.info("sorting results by: [%s]", order)
        if order == self.get_sort_by():
            return
        driver.click_element(self.SORT_BY_LABEL)
        dropdown_item = By.XPATH, self.SORT_BY_DROPDOWN_ITEM_XPATH_TEMPLATE.format(order=order)
        driver.click_element(dropdown_item)

    def get_total_jobs_found(self) -> int:
        try:
            text = driver.wait_until_visible_element(self.TOTAL_JOBS_FOUND).text.strip()
            text = text.replace(",", "").replace(".", "")
            return int(text)
        except:
            return 0

    def trigger_search(self):
        log.info("pressing Seek search button...")
        driver.click_element(self.SEARCH_BUTTON)
        self.wait_for_results()
        log.info("got [ %s ] total search results")
        self.set_sort_by("Date")

    def wait_for_results(self) -> bool:
        log.info("waiting for search results...")
        try:
            return driver.wait_until_visible_element(self.SEARCH_RESULTS) is not None
        except TimeoutException:
            return False

    def get_visible_jobs(self) -> List[JobResult]:
        try:
            visible_results = [SeekJobResult(el) for el in driver.wait_until_elements(self.RESULT_ITEM)]
        except:
            visible_results = []

        log.info("got (%s) visible results on current page", len(visible_results))
        return visible_results

    def view_next_results_page(self):
        log.info("navigating to next results page...")
        driver.scroll_into_view(self.PAGINATION_NEXT)
        driver.click_element(self.PAGINATION_NEXT)
