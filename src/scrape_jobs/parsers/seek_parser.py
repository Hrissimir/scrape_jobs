from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import TimedeltaParser, utc_moment
from tabulate import tabulate


def get_tags(source: str) -> List[Tag]:
    soup = BeautifulSoup(source, "lxml")
    return soup.select(":scope article")


def get_posted_time(tag: Tag):
    posted_tags = tag.select(":scope span[data-automation='jobListingDate']")
    if posted_tags:
        posted_text = normalize_spacing(posted_tags[0].get_text().strip())
        posted_timedelta = TimedeltaParser.parse(posted_text)
        return utc_moment() - posted_timedelta

    return None


def get_location(tag: Tag):
    location_tags = tag.select(":scope a[data-automation='jobLocation']")
    return normalize_spacing(location_tags[0].get_text().strip()) if location_tags else None


def get_area(tag: Tag):
    area_tags = tag.select(":scope a[data-automation='jobArea']")
    return normalize_spacing(area_tags[0].get_text().strip()) if area_tags else None


def get_classification(tag: Tag):
    classification_tags = tag.select(":scope a[data-automation='jobClassification']")
    return normalize_spacing(classification_tags[0].get_text().strip()) if classification_tags else None


def get_sub_classification(tag: Tag):
    sub_classification_tags = tag.select(":scope a[data-automation='jobSubClassification']")
    return normalize_spacing(sub_classification_tags[0].get_text().strip()) if sub_classification_tags else None


def get_title(tag: Tag):
    title_tags = tag.select(":scope h1 > a")
    return normalize_spacing(title_tags[0].get_text().strip()) if title_tags else None


def get_salary(tag: Tag):
    salary_tags = tag.select(":scope span[data-automation='jobSalary']")
    return normalize_spacing(salary_tags[0].get_text().strip()) if salary_tags else None


def get_company(tag: Tag):
    company_tags = tag.select(":scope a[data-automation='jobCompany']")
    return normalize_spacing(company_tags[0].get_text().strip()) if company_tags else None


def get_url(tag: Tag):
    title_tags = tag.select(":scope h1 > a")
    if title_tags:
        url = urljoin("https://seek.com.au/", title_tags[0]["href"].strip())
        return url[:url.index("?")] if ("?" in url) else url
    return None


PARSE_MAP = {
    "posted_time": get_posted_time,
    "location": get_location,
    "area": get_area,
    "classification": get_classification,
    "sub_classification": get_sub_classification,
    "title": get_title,
    "salary": get_salary,
    "company": get_company,
    "url": get_url
}

KEYS = list(PARSE_MAP.keys())


def parse_jobs(page_source: str):
    return [{key: parse_func(tag) for key, parse_func in PARSE_MAP.items()}
            for tag
            in get_tags(page_source)]


def format_jobs(jobs):
    return tabulate(jobs, headers={key: key.upper() for key in KEYS})
