import logging
from typing import List
from urllib.parse import urljoin

from bs4 import Tag, BeautifulSoup
from hed_utils.selenium import FindBy
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import TimedeltaParser, utc_moment

from scrape_jobs.base.job import Job
from scrape_jobs.base.page import Page
from scrape_jobs.seek.seek_job import SeekJob

__all__ = [
    "SeekPage"
]

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


def parse_tag(tag: Tag) -> Job:
    def get_posted_time():
        posted_tags = tag.select(":scope span[data-automation='jobListingDate']")
        if posted_tags:
            posted_text = normalize_spacing(posted_tags[0].get_text().strip())
            posted_timedelta = TimedeltaParser.parse(posted_text)
            return utc_moment() - posted_timedelta

        return None

    def get_location():
        location_tags = tag.select(":scope a[data-automation='jobLocation']")
        return normalize_spacing(location_tags[0].get_text().strip()) if location_tags else None

    def get_area():
        area_tags = tag.select(":scope a[data-automation='jobArea']")
        return normalize_spacing(area_tags[0].get_text().strip()) if area_tags else None

    def get_classification():
        classification_tags = tag.select(":scope a[data-automation='jobClassification']")
        return normalize_spacing(classification_tags[0].get_text().strip()) if classification_tags else None

    def get_sub_classification():
        sub_classification_tags = tag.select(":scope a[data-automation='jobSubClassification']")
        return normalize_spacing(sub_classification_tags[0].get_text().strip()) if sub_classification_tags else None

    def get_title():
        title_tags = tag.select(":scope h1 > a")
        return normalize_spacing(title_tags[0].get_text().strip()) if title_tags else None

    def get_salary():
        salary_tags = tag.select(":scope span[data-automation='jobSalary']")
        return normalize_spacing(salary_tags[0].get_text().strip()) if salary_tags else None

    def get_company():
        company_tags = tag.select(":scope a[data-automation='jobCompany']")
        return normalize_spacing(company_tags[0].get_text().strip()) if company_tags else None

    def get_url():
        title_tags = tag.select(":scope h1 > a")
        if title_tags:
            url = urljoin("https://seek.com.au/", title_tags[0]["href"].strip())
            return url[:url.index("?")] if ("?" in url) else url
        return None

    job = SeekJob(
        scraped_time=utc_moment().replace(minute=0, second=0, microsecond=0),
        posted_time=get_posted_time(),
        location=get_location(),
        area=get_area(),
        classification=get_classification(),
        sub_classification=get_sub_classification(),
        title=get_title(),
        salary=get_salary(),
        company=get_company(),
        url=get_url()
    )

    return job


class SeekPage(Page):
    URL = "https://www.seek.com.au/"

    WHAT_INPUT = FindBy.ID(value="keywords-input",
                           desc="'What' input")

    WHERE_INPUT = FindBy.CSS_SELECTOR(value="input#SearchBar__Where",
                                      desc="'Where' input")
    WHERE_AUTOCOMPLETE = FindBy.XPATH(
        value="//input[contains(@id,'SearchBar__Where')]/../..//ul//li[contains(@id,'react-autowhatever')]",
        desc="'Where' autocomplete")

    SEARCH_BUTTON = FindBy.CSS_SELECTOR(value="button[data-automation='searchButton']",
                                        desc="'Search' button")

    SEARCH_RESULTS = FindBy.TAG_NAME(value="article",
                                     visible_only=False,
                                     desc="search results")

    NEXT_PAGE_BUTTON = FindBy.CSS_SELECTOR(value="a[data-automation='page-next']",
                                           desc="'Next Page' button")

    @classmethod
    def get_visible_job_tags(cls, page_source: str) -> List[Tag]:
        super().get_visible_job_tags(page_source)
        page_soup = BeautifulSoup(page_source, "lxml")
        job_tags = page_soup.select(":scope article") or []
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

        what_value = search_params.get("what", "")
        _log.info("entering 'what': '%s'", what_value)
        self.WHAT_INPUT.click()
        self.WHAT_INPUT.send_keys(what_value)
        self.driver.wait_for_page_load()

        where_value = search_params.get("where", "")
        _log.info("entering 'where': '%s'", where_value)
        self.WHERE_INPUT.click()
        self.WHERE_INPUT.send_keys(where_value)
        self.WHERE_AUTOCOMPLETE.click()
        self.driver.wait_for_page_load()

    def trigger_search(self):
        super().trigger_search()
        self.SEARCH_BUTTON.click()

    def wait_for_results_to_load(self):
        super().wait_for_results_to_load()
        self.driver.wait_for_page_load()
        return self.SEARCH_RESULTS.is_visible(timeout=20)

    def has_more_results(self) -> bool:
        super().has_more_results()
        has_more = self.NEXT_PAGE_BUTTON.is_visible(timeout=2)
        if has_more:
            _log.info("more results are available!")
        else:
            _log.warning("no more results are available!")
        return has_more

    def load_more_results(self):
        super().load_more_results()
        last_result = self.SEARCH_RESULTS[-1]
        self.NEXT_PAGE_BUTTON.click()
        self.driver.wait_for_staleness_of(last_result, timeout=10)
