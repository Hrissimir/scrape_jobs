from typing import Dict, Any
from urllib.parse import urljoin

from bs4 import Tag
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import TimedeltaParser, utc_moment

from scrape_jobs.base.data_collection import JobParser

__all__ = ["SeekJob"]


class SeekJob(JobParser):
    SELECTOR = ":scope article"

    KEYS = [
        "scraped_time",
        "posted_time",
        "location",
        "area",
        "classification",
        "sub_classification",
        "title",
        "salary",
        "company",
        "url"]

    @classmethod
    def get_posted_time(cls, tag):
        posted_tags = tag.select(":scope span[data-automation='jobListingDate']")
        if posted_tags:
            posted_text = normalize_spacing(posted_tags[0].get_text().strip())
            posted_timedelta = TimedeltaParser.parse(posted_text)
            return utc_moment() - posted_timedelta

        return None

    @classmethod
    def get_location(cls, tag):
        location_tags = tag.select(":scope a[data-automation='jobLocation']")
        return normalize_spacing(location_tags[0].get_text().strip()) if location_tags else None

    @classmethod
    def get_area(cls, tag):
        area_tags = tag.select(":scope a[data-automation='jobArea']")
        return normalize_spacing(area_tags[0].get_text().strip()) if area_tags else None

    @classmethod
    def get_classification(cls, tag):
        classification_tags = tag.select(":scope a[data-automation='jobClassification']")
        return normalize_spacing(classification_tags[0].get_text().strip()) if classification_tags else None

    @classmethod
    def get_sub_classification(cls, tag):
        sub_classification_tags = tag.select(":scope a[data-automation='jobSubClassification']")
        return normalize_spacing(sub_classification_tags[0].get_text().strip()) if sub_classification_tags else None

    @classmethod
    def get_title(cls, tag):
        title_tags = tag.select(":scope h1 > a")
        return normalize_spacing(title_tags[0].get_text().strip()) if title_tags else None

    @classmethod
    def get_salary(cls, tag):
        salary_tags = tag.select(":scope span[data-automation='jobSalary']")
        return normalize_spacing(salary_tags[0].get_text().strip()) if salary_tags else None

    @classmethod
    def get_company(cls, tag):
        company_tags = tag.select(":scope a[data-automation='jobCompany']")
        return normalize_spacing(company_tags[0].get_text().strip()) if company_tags else None

    @classmethod
    def get_url(cls, tag):
        title_tags = tag.select(":scope h1 > a")
        if title_tags:
            url = urljoin("https://seek.com.au/", title_tags[0]["href"].strip())
            return url[:url.index("?")] if ("?" in url) else url
        return None

    def parse(self, tag: Tag) -> Dict[str, Any]:
        job = super().parse(tag)

        job["scraped_time"] = self.creation_time_utc
        job["posted_time"] = self.get_posted_time(tag)
        job["location"] = self.get_location(tag)
        job["area"] = self.get_area(tag)
        job["classification"] = self.get_classification(tag)
        job["sub_classification"] = self.get_sub_classification(tag)
        job["title"] = self.get_title(tag)
        job["salary"] = self.get_salary(tag)
        job["company"] = self.get_company(tag)
        job["url"] = self.get_url(tag)

        return job
