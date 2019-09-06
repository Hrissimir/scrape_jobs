from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log
from selenium.webdriver.common.by import By

from scrape_jobs.common.results_context import ResultsContext
from scrape_jobs.sites.seek_com_au.seek_result import SeekJobResult


class SeekResultsContext(ResultsContext):
    NEXT_PAGE_BUTTON = By.CSS_SELECTOR, "a[data-automation='page-next']"

    RESULT_ITEM = By.CSS_SELECTOR, "div[data-automation='searchResults'] article"

    def has_results(self) -> bool:
        return driver.is_visible(self.RESULT_ITEM)

    def has_next_page(self) -> bool:
        return driver.is_visible(self.NEXT_PAGE_BUTTON)

    def get_visible_results(self) -> List[SeekJobResult]:
        return [SeekJobResult(e.soup)
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
