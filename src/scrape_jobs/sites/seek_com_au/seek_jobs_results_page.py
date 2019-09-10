from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from scrape_jobs.common.jobs_results_page import JobsResultsPage
from scrape_jobs.sites.seek_com_au.seek_job_result import SeekJobResult


class SeekJobsResultsPage(JobsResultsPage):
    NEXT_PAGE_BUTTON = By.CSS_SELECTOR, "a[data-automation='page-next']"

    RESULT_ITEM = By.CSS_SELECTOR, "div[data-automation='searchResults'] article"
    RESULTS_LOADER = By.CSS_SELECTOR, "div[data-automation='searchResultsLoader']"

    def has_results(self) -> bool:
        return driver.is_visible(self.RESULT_ITEM)

    def has_next_page(self) -> bool:
        return driver.is_visible(self.NEXT_PAGE_BUTTON)

    def get_visible_results(self) -> List[SeekJobResult]:
        page_soup = driver.page_soup()

        return [SeekJobResult(e)
                for e
                in page_soup.select(self.RESULT_ITEM[-1])]

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
        try:
            loader = driver.wait_until_visible_element(self.RESULTS_LOADER, timeout=1)
            log.info("found results loader element!")  # pragma: no cover
        except TimeoutException:  # pragma: no cover
            log.info("no results loader was found")
            loader = None

        if loader:  # pragma: no cover
            try:
                log.info("waiting for results loader to disappear...")
                driver.wait_until_staleness_of(loader, timeout=10)
            except TimeoutException:  # pragma: no cover
                log.info("the result loader is not going away - deleting it from page..")
                loader.hide_element()

        log.info("clicking NEXT page button...")
        driver.click_locator(self.NEXT_PAGE_BUTTON)

    def scroll_to_last_result(self):
        if self.has_results():
            results = driver.wait_until_visible_elements(self.RESULT_ITEM, timeout=2)
            results[-1].scroll_into_view()
