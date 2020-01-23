import logging
from datetime import datetime
from typing import List
from urllib.parse import urljoin

from bs4 import Tag, BeautifulSoup
from hed_utils.selenium import FindBy, DriverWrapper
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import utc_moment, localize
from selenium.webdriver.common.keys import Keys

from scrape_jobs.base.job import Job
from scrape_jobs.base.page import Page
from scrape_jobs.linkedin.linkedin_job import LinkedinJob

__all__ = [
    "LinkedinPage"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def parse_tag(tag: Tag) -> Job:
    def get_posted_time():
        posted_tags = tag.select(":scope time.job-result-card__listdate")
        if posted_tags:
            posted_date_text = posted_tags[0]["datetime"]
            if posted_date_text:
                return localize(datetime.strptime(posted_date_text, "%Y-%m-%d"), "UTC")

        return None

    def get_location():
        location_tags = tag.select(":scope span.job-result-card__location")
        return normalize_spacing(location_tags[0].get_text().strip()) if location_tags else None

    def get_title():
        title_tags = tag.select(":scope h3.job-result-card__title")
        return normalize_spacing(title_tags[0].get_text().strip()) if title_tags else None

    def get_company():
        company_tags = tag.select(":scope h4.result-card__subtitle")
        return normalize_spacing(company_tags[0].get_text().strip()) if company_tags else None

    def get_url():
        title_tags = tag.select(":scope a.result-card__full-card-link")
        if title_tags:
            url = urljoin("https://seek.com.au/", title_tags[0]["href"].strip())
            return url[:url.index("?")] if ("?" in url) else url
        return None

    job = LinkedinJob(
        scraped_time=utc_moment().replace(minute=0, second=0, microsecond=0),
        posted_time=get_posted_time(),
        location=get_location(),
        title=get_title(),
        company=get_company(),
        url=get_url()
    )

    return job


class DatePostedFilter:
    OPEN_BUTTON = FindBy.XPATH("//div[@id='TIME_POSTED-dropdown']/../button")
    DROPDOWN_BODY = FindBy.CSS_SELECTOR("div#TIME_POSTED-dropdown")
    FILTER_LABELS = FindBy.XPATH("//div[@id='TIME_POSTED-dropdown']//div[contains(@class, 'filter-list')]/ul/li/label")
    APPLY_BUTTON = FindBy.XPATH(
        "//div[@id='TIME_POSTED-dropdown']//div[contains(@class, 'dropdown-actions')]/button[contains(@class,'apply')]")

    def __init__(self, driver: DriverWrapper):
        self.driver = driver

    def open_filter(self):
        _log.debug("opening date-posted filter")
        self.OPEN_BUTTON.click()

        if self.FILTER_LABELS.is_visible(timeout=5):
            raise RuntimeError("Could not open 'Date-Posted' filter!")

    def select_value(self, value: str):
        _log.debug("selecting date-posted value: '%s'", value)
        visible_labels = []
        for label in self.FILTER_LABELS:
            label_text = normalize_spacing(label.text.strip())
            if value.lower() in label_text.lower():
                label.click()
                return
            else:
                visible_labels.append(label_text)

        _log.warning("visible date-posted filter values: %s", visible_labels)
        raise RuntimeError("Could not click Date-Posted filter value!", value, visible_labels)

    def apply_value(self, value: str):
        self.open_filter()
        self.select_value(value)
        body_element = self.DROPDOWN_BODY.wrapped_element
        self.APPLY_BUTTON.click()
        self.driver.wait_for_staleness_of(body_element, timeout=5)


class LinkedinPage(Page):
    URL = "https://www.linkedin.com/jobs"

    SEARCH_RESULTS = FindBy.CSS_SELECTOR(value="section.results__list > ul > li.result-card",
                                         visible_only=True,
                                         desc="search results")

    KEYWORDS_INPUT = FindBy.NAME(value="keywords",
                                 visible_only=True,
                                 desc="'Keywords' input")

    LOCATION_INPUT = FindBy.NAME(value="location",
                                 visible_only=True,
                                 desc="'Where' input")

    SEARCH_BUTTON = FindBy.CSS_SELECTOR(value="button[type='submit'][aria-label='Search']",
                                        visible_only=True,
                                        desc="'Search' button")

    SEE_MORE_JOBS_BUTTON = FindBy.CSS_SELECTOR(value="button.see-more-jobs",
                                               visible_only=True,
                                               desc="'Next Page' button")

    DATE_POSTED_FILTER = DatePostedFilter(driver=Page.driver)

    @classmethod
    def get_visible_job_tags(cls, page_source: str) -> List[Tag]:
        super().get_visible_job_tags(page_source)
        page_soup = BeautifulSoup(page_source, "lxml")
        job_tags = page_soup.select(":scope section.results__list > ul > li.result-card") or []
        _log.debug("got %s visible job tags", len(job_tags))
        return job_tags

    @classmethod
    def parse_job_tag(cls, tag: Tag) -> Job:
        return parse_tag(tag)

    def go_to(self):
        super().go_to()
        self.driver.get(self.URL)

    def set_search_params(self, search_params: dict):
        super().set_search_params(search_params)

        keywords = search_params.get("keywords", "")
        _log.info("entering 'keywords': '%s'", keywords)
        self.KEYWORDS_INPUT.click()
        self.KEYWORDS_INPUT.send_keys(keywords + Keys.ENTER)
        self.driver.wait_for_page_load()

        location = search_params.get("location", "")
        _log.info("entering 'location': '%s'", location)
        self.LOCATION_INPUT.click()
        self.LOCATION_INPUT.send_keys(location + Keys.ENTER)
        self.driver.wait_for_page_load()

        date_posted = search_params.get("date_posted", "")
        _log.info("applying 'date-posted' filter: '%s'", date_posted)
        self.DATE_POSTED_FILTER.apply_value(date_posted)

    def trigger_search(self):
        super().trigger_search()
        self.SEARCH_BUTTON.click()

    def wait_for_results_to_load(self):
        super().wait_for_results_to_load()
        self.driver.wait_for_page_load()
        return self.SEARCH_RESULTS.is_visible(timeout=20)

    def scroll_to_bottom(self):
        search_results = self.SEARCH_RESULTS.elements
        if search_results:
            search_results[-1].scroll_into_view()
        self.driver.wait_for_page_load()

    def has_more_results(self) -> bool:
        super().has_more_results()
        self.scroll_to_bottom()

        has_more = self.SEE_MORE_JOBS_BUTTON.is_visible(timeout=2)
        if has_more:
            _log.info("more results are available!")
        else:
            _log.warning("no more results are available!")
        return has_more

    def load_more_results(self):
        super().load_more_results()
        load_more_button = self.SEE_MORE_JOBS_BUTTON.wrapped_element
        load_more_button.click()
        self.driver.wait_for_staleness_of(load_more_button, timeout=5)
        self.driver.wait_for_page_load()
