from typing import Tuple

from hed_utils.selenium import driver
from hed_utils.selenium.page_objects.base.page_element import PageElement
from hed_utils.support import log
from selenium.webdriver.common.by import By


class LinkedinSearchSection(PageElement):

    def __init__(self,
                 locator: Tuple[str, str],
                 keywords_input_locator: Tuple[str, str],
                 location_input_locator: Tuple[str, str],
                 search_button_locator: Tuple[str, str]
                 ):
        super().__init__(locator)
        self.keywords_input_locator = keywords_input_locator
        self.location_input_locator = location_input_locator
        self.search_button_locator = search_button_locator

    def set_keywords(self, keywords):
        log.info("setting search keywords to: '%s'", keywords)
        driver.set_text(self.keywords_input_locator, keywords, press_enter=True)
        driver.wait_until_page_loads()

    def set_location(self, location):
        log.info("setting search location to: '%s'", location)
        driver.set_text(self.location_input_locator, location, press_enter=True)
        driver.wait_until_page_loads()

    def trigger_search(self):
        log.info("triggering search...")
        driver.click_locator(self.search_button_locator)
        driver.wait_until_page_loads()


class LinkedinJobsSearchForm(LinkedinSearchSection):
    LOCATOR = By.XPATH, "//main//section//form[contains(@action,'/jobs/search')]"

    KEYWORDS_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'keywords')]"

    LOCATION_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'location')]"

    SEARCH_BUTTON = By.XPATH, "//button[contains(@form,'JOBS')]"

    def __init__(self):
        super().__init__(self.LOCATOR, self.KEYWORDS_INPUT, self.LOCATION_INPUT, self.SEARCH_BUTTON)


class LinkedinJobsSearchBar(LinkedinSearchSection):
    LOCATOR = By.XPATH, "//header//nav/section[@class='search-bar']"

    KEYWORDS_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'keywords')]"

    LOCATION_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'location')]"

    SEARCH_BUTTON = By.CSS_SELECTOR, "section[data-searchbar-type='JOBS'] button[type='submit']"

    def __init__(self):
        super().__init__(self.LOCATOR, self.KEYWORDS_INPUT, self.LOCATION_INPUT, self.SEARCH_BUTTON)
