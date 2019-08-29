from typing import List

from hed_utils.selenium import driver
from hed_utils.selenium.page_objects.base.web_page import WebPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from scrape_jobs.sites.seek_com_au.seek_result import SeekResult


class SeekPage(WebPage):
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
        search_input = driver.wait_until_visible_element(self.KEYWORDS_INPUT)
        search_input.clear()
        search_input.send_keys(keywords)

    def get_search_keywords(self) -> str:
        return driver.wait_until_visible_element(self.KEYWORDS_INPUT).text

    def set_search_location(self, location: str):
        location_input = driver.wait_until_visible_element(self.LOCATION_INPUT)
        location_input.clear()
        location_input.send_keys(location)
        driver.click_element(self.AUTOCOMPLETE_FIRST_OPTION)

    def get_search_location(self) -> str:
        return driver.wait_until_visible_element(self.LOCATION_INPUT).text

    def trigger_search(self):
        driver.click_element(self.SEARCH_BUTTON)
        import time
        time.sleep(5)

    def wait_for_search_results(self) -> bool:
        try:
            return driver.wait_until_visible_element(self.SEARCH_RESULTS) is not None
        except TimeoutException:
            return False

    def get_total_jobs_found(self) -> int:
        try:
            text = driver.wait_until_visible_element(self.TOTAL_JOBS_FOUND).text.strip()
            text = text.replace(",", "").replace(".", "")
            return int(text)
        except:
            return 0

    def get_sort_by(self) -> str:
        return driver.wait_until_visible_element(self.SORT_BY_EFFECTIVE_VALUE).text.capitalize()

    def set_sort_by(self, order: str):
        order = order.capitalize()
        if order == self.get_sort_by():
            return
        driver.click_element(self.SORT_BY_LABEL)
        dropdown_item = By.XPATH, self.SORT_BY_DROPDOWN_ITEM_XPATH_TEMPLATE.format(order=order)
        driver.click_element(dropdown_item)

    def get_visible_results(self) -> List[SeekResult]:
        return [SeekResult(el) for el in driver.wait_until_elements(self.RESULT_ITEM)]

    def get_visible_results_data(self) -> List[dict]:
        return [result.as_dict() for result in self.get_visible_results()]

    def get_current_page_number(self) -> str:
        pagination_container = driver.wait_until_visible_element(self.PAGINATION_NEXT).parent_element
        active_buttons = [child
                          for child
                          in pagination_container.child_elements
                          if ((child.tag_name == "span") and (not child.has_child_elements))]
        return active_buttons[0].text.strip()

    def go_to_next_page(self):
        driver.scroll_into_view(self.PAGINATION_NEXT)
        driver.click_element(self.PAGINATION_NEXT)
