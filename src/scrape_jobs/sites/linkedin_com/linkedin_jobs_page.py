from hed_utils.selenium import driver
from selenium.webdriver.common.by import By

from scrape_jobs.common.jobs_page import JobsPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_results_page import LinkedinJobsResultsPage
from scrape_jobs.sites.linkedin_com.linkedin_jobs_search_page import LinkedinJobsSearchPage


class LinkedinJobsPage(LinkedinJobsSearchPage, LinkedinJobsResultsPage, JobsPage):
    COOKIES_ALERT = By.CSS_SELECTOR, "label[for=cookie-policy] > figure"

    def __init__(self):
        super().__init__(url_domain="https://www.linkedin.com/", url_path="/jobs")

    def go_to(self, *, wait_for_url_changes=True, wait_for_page_load=True, check_is_at=True):
        super().go_to(wait_for_url_changes=wait_for_url_changes,
                      wait_for_page_load=wait_for_page_load,
                      check_is_at=check_is_at)
        if driver.is_visible(self.COOKIES_ALERT):
            driver.click_locator(self.COOKIES_ALERT)
            driver.wait_until_page_loads()
