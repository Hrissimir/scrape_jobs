from typing import List

from hed_utils.selenium import driver
from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper
from selenium.webdriver.common.by import By

from scrape_jobs.common.results_context import ResultsContext
from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult


class LinkedinResultsContext(ResultsContext):
    LOCATOR = By.XPATH, "//main/section[contains(@class,'results__container')]"
    RESULTS_LIST = By.XPATH, LOCATOR[-1] + "/ul"
    JOB_RESULT_ITEM = By.XPATH, RESULTS_LIST[-1] + "/li[contains(@class,'job-result-card')]"
    SEE_MORE_JOBS = By.XPATH, LOCATOR[-1] + "/button[contains(@class,'see-more-jobs')]"

    def elements(self) -> List[ElementWrapper]:
        return driver.wait_until_visible_elements(self.JOB_RESULT_ITEM)

    def has_results(self) -> bool:
        return driver.is_visible(self.JOB_RESULT_ITEM)

    def has_next_page(self) -> bool:
        return driver.is_visible(self.SEE_MORE_JOBS)

    def get_visible_results(self) -> List[LinkedinJobResult]:
        return [LinkedinJobResult(e.soup) for e in self.elements()]

    def go_to_next_page(self):
        driver.click_element(self.SEE_MORE_JOBS)
