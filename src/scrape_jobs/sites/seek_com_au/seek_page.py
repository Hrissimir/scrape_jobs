from typing import List
from urllib.parse import urljoin

from hed_utils.selenium import driver
from hed_utils.selenium.page_objects.base.web_page import WebPage
from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper
from hed_utils.support import log
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class JobResult(ElementWrapper):
    KEYS = ["date", "title", "company", "classification", "salary", "suburb", "url"]

    def __init__(self, element):
        super().__init__(element)
        self._soup = self.soup
        self._dict = None

    def is_featured(self) -> bool:
        try:
            return self._soup.select_one("span[data-automation='jobPremium']") is not None
        except:
            return False

    def job_title(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobTitle']").get_text().strip()
        except:
            return "NO_TITLE"

    def job_url(self) -> str:
        try:
            a = self._soup.select_one("a[data-automation='jobTitle']")
            domain = "https://www.seek.com.au/"
            link = urljoin(domain, a["href"])
            return link[:link.index("?")]
        except:
            return "NO_URL"

    def job_date(self, tz="Australia/Sydney") -> str:
        from hed_utils.support import time_tool
        try:

            date = self._soup.select_one("span[data-automation='jobListingDate']").get_text().strip()
        except:
            if self.is_featured:
                return "Featured"
            else:
                return "NO_DATE"

        if date:
            date = time_tool.PastTimeParser.parse(date)
            tz_date = str(time_tool.convert_to_tz(date, tz).date())
            return str(tz_date)

        return ""

    def _job_classification(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobClassification']").get_text().strip()
        except:
            return ""

    def _job_sub_classification(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobSubClassification']").get_text().strip()
        except:
            return ""

    def job_classification(self) -> str:
        components = [c for c in [self._job_classification(), self._job_sub_classification()] if c]
        return ", ".join(components)

    def job_company(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobCompany']").get_text().strip()
        except:
            return "NO_COMPANY"

    def job_salary(self) -> str:
        try:
            return self._soup.select_one("span[data-automation='jobSalary']").get_text().strip()
        except:
            return "NO_SALARY"

    def job_suburb(self) -> str:
        try:
            city = self._soup.select_one("a[data-automation='jobLocation']").get_text().strip()
        except:
            city = ""
        try:
            area = self._soup.select_one("a[data-automation='jobArea']").get_text().strip()
        except:
            area = ""

        components = [c for c in [city, area] if c]
        return ", ".join(components)

    def as_dict(self, tz="Australia/Sydney") -> dict:
        if not self._dict:
            self._dict = dict(date=self.job_date(tz),
                              title=self.job_title(),
                              company=self.job_company(),
                              classification=self.job_classification(),
                              salary=self.job_salary(),
                              suburb=self.job_suburb(),
                              url=self.job_url())
        return self._dict

    def __repr__(self):
        return f"{type(self).__name__}({self._dict})"


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
        log.info("setting the search 'WHAT' input to: '%s'", keywords)
        search_input = driver.wait_until_visible_element(self.KEYWORDS_INPUT)
        search_input.clear()
        search_input.send_keys(keywords)

    def get_search_keywords(self) -> str:
        return driver.wait_until_visible_element(self.KEYWORDS_INPUT).text

    def set_search_location(self, location: str):
        log.info("setting the search 'WHERE' input to: '%s'", location)
        location_input = driver.wait_until_visible_element(self.LOCATION_INPUT)
        location_input.clear()
        location_input.send_keys(location)
        driver.click_element(self.AUTOCOMPLETE_FIRST_OPTION)

    def get_search_location(self) -> str:
        return driver.wait_until_visible_element(self.LOCATION_INPUT).text

    def trigger_search(self):
        log.info("triggering search...")
        driver.click_element(self.SEARCH_BUTTON)
        import time
        time.sleep(5)

    def wait_for_search_results(self) -> bool:
        log.info("waiting for search results...")
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

    def get_visible_results(self) -> List[JobResult]:
        return [JobResult(el) for el in driver.wait_until_elements(self.RESULT_ITEM)]

    def get_visible_results_data(self, tz="Australia/Sydney") -> List[dict]:
        return [job.as_dict(tz) for job in self.get_visible_results()]

    def get_current_page_number(self) -> str:
        pagination_container = driver.wait_until_visible_element(self.PAGINATION_NEXT).parent_element
        active_buttons = [child
                          for child
                          in pagination_container.child_elements
                          if ((child.tag_name == "span") and (not child.has_child_elements))]
        return active_buttons[0].text.strip()

    def go_to_next_page(self):
        log.info("navigating to next results page...")
        driver.scroll_into_view(self.PAGINATION_NEXT)
        driver.click_element(self.PAGINATION_NEXT)
