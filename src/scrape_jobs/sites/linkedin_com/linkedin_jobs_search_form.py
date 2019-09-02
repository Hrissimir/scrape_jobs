from typing import Tuple

from selenium.webdriver.common.by import By

from scrape_jobs.sites.linkedin_com.linkedin_search_section import LinkedinSearchSection


class LinkedinJobsSearchForm(LinkedinSearchSection):
    @property
    def keywords_input_locator(self) -> Tuple[str, str]:
        return self.KEYWORDS_INPUT

    @property
    def location_input_locator(self) -> Tuple[str, str]:
        return self.LOCATION_INPUT

    @property
    def search_button_locator(self) -> Tuple[str, str]:
        return self.SEARCH_BUTTON

    LOCATOR = By.XPATH, "//main//section//form[contains(@action,'/jobs/search')]"
    KEYWORDS_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'keywords')]"
    LOCATION_INPUT = By.XPATH, LOCATOR[-1] + "//input[contains(@name,'location')]"
    SEARCH_BUTTON = By.XPATH, "//button[contains(@form,'JOBS')]"

    def __init__(self):
        super().__init__(self.LOCATOR)
