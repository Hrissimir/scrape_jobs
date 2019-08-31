from urllib.parse import urljoin

from bs4 import BeautifulSoup
from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper

from scrape_jobs.common import jobpost

KEYS = jobpost.KEYS + ["salary"]


def _get_posted(soup: BeautifulSoup):
    try:
        return soup.select_one("span[data-automation='jobListingDate']").get_text().strip()
    except:
        return "NO_POSTED"


def _get_location(soup: BeautifulSoup):
    try:
        city = soup.select_one("a[data-automation='jobLocation']").get_text().strip()
    except:
        city = ""
    try:
        area = soup.select_one("a[data-automation='jobArea']").get_text().strip()
    except:
        area = ""

    components = [c for c in [city, area] if c]
    return ", ".join(components)


def _get_title(soup: BeautifulSoup):
    try:
        return soup.select_one("a[data-automation='jobTitle']").get_text().strip()
    except:
        return "NO_TITLE"


def _get_company(soup: BeautifulSoup):
    try:
        return soup.select_one("a[data-automation='jobCompany']").get_text().strip()
    except:
        return "NO_COMPANY"


def _get_classification(soup: BeautifulSoup):
    try:
        main_classification = soup.select_one("a[data-automation='jobClassification']").get_text().strip()
    except:
        main_classification = ""

    try:
        sub_classification = soup.select_one("a[data-automation='jobSubClassification']").get_text().strip()
    except:
        sub_classification = ""

    components = [c.strip() for c in [main_classification, sub_classification] if c.strip()]
    return ", ".join(components)


def _get_url(soup: BeautifulSoup):
    try:
        a = soup.select_one("a[data-automation='jobTitle']")
        domain = "https://www.seek.com.au/"
        link = urljoin(domain, a["href"])
        return link[:link.index("?")]
    except:
        return "NO_URL"


def _get_salary(soup: BeautifulSoup):
    try:
        return soup.select_one("span[data-automation='jobSalary']").get_text().strip()
    except:
        return "NO_SALARY"


def parse_result_element(element: ElementWrapper) -> dict:
    soup = element.soup
    post = jobpost.new_post()

    jobpost.set_date(post, _get_posted(soup))
    jobpost.set_location(post, _get_location(soup))
    jobpost.set_title(post, _get_title(soup))
    jobpost.set_company(post, _get_company(soup))
    jobpost.set_classification(post, _get_classification(soup))
    jobpost.set_url(post, _get_url(soup))
    jobpost.set_salary(post, _get_salary(soup))
    return post
