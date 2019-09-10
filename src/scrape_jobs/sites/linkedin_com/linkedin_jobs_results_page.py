from typing import List

from hed_utils.selenium import driver
from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper
from hed_utils.support import log
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from scrape_jobs.common.jobs_results_page import JobsResultsPage
from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult


class LinkedinJobsResultsPage(JobsResultsPage):
    LOCATOR = By.XPATH, "//main/section[contains(@class,'results__container')]"
    RESULTS_LIST = By.XPATH, LOCATOR[-1] + "/ul"
    JOB_RESULT_ITEM = By.XPATH, RESULTS_LIST[-1] + "/li[contains(@class,'job-result-card')]"
    SEE_MORE_JOBS = By.XPATH, LOCATOR[-1] + "/button[contains(@class,'see-more-jobs')]"
    NO_MORE_JOBS = By.CSS_SELECTOR, "span.see-more-jobs__viewed-all-text"

    def is_visible(self) -> bool:
        return driver.is_visible(self.LOCATOR)

    def elements(self) -> List[ElementWrapper]:
        return driver.wait_until_visible_elements(self.JOB_RESULT_ITEM)

    def has_results(self) -> bool:
        return driver.is_visible(self.JOB_RESULT_ITEM)

    def has_next_page(self) -> bool:
        return (not driver.is_visible(self.NO_MORE_JOBS)) and driver.is_visible(self.SEE_MORE_JOBS)

    def get_visible_results(self) -> List[LinkedinJobResult]:
        page_soup = driver.page_soup()
        results = page_soup.select("ul > li[class~=job-result-card]")
        return [LinkedinJobResult(result) for result in results]

    def go_to_next_page(self):
        driver.click_locator(self.SEE_MORE_JOBS)
        driver.wait_until_page_loads()
        try:
            driver.wait_until_visible_element(self.SEE_MORE_JOBS, timeout=10)
        except TimeoutException:
            log.warning("the 'See more jobs' button did not appear...")
            has_ended = driver.is_visible(self.NO_MORE_JOBS)
            log.warning("'You've viewed all jobs' is present: %s", has_ended)

    def scroll_to_last_result(self):
        if self.has_results():
            self.elements()[-1].scroll_into_view()
