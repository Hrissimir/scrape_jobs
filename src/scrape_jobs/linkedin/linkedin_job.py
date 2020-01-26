from datetime import datetime
from typing import Dict, Any
from urllib.parse import urljoin

from bs4 import Tag
from hed_utils.support.text_tool import normalize_spacing
from hed_utils.support.time_tool import localize

from scrape_jobs.base.data_collection import JobParser

__all__ = ["LinkedinJob"]


class LinkedinJob(JobParser):
    KEYS = ["scraped_time", "posted_time", "location", "title", "company", "url"]
    SELECTOR = ":scope section.results__list > ul > li.result-card"

    @classmethod
    def get_posted_time(cls, tag):
        posted_tags = tag.select(":scope time.job-result-card__listdate")
        if posted_tags:
            posted_date_text = posted_tags[0]["datetime"]
            if posted_date_text:
                return localize(datetime.strptime(posted_date_text, "%Y-%m-%d"), "UTC")

        return None

    @classmethod
    def get_location(cls, tag):
        location_tags = tag.select(":scope span.job-result-card__location")
        return normalize_spacing(location_tags[0].get_text().strip()) if location_tags else None

    @classmethod
    def get_title(cls, tag):
        title_tags = tag.select(":scope h3.job-result-card__title")
        return normalize_spacing(title_tags[0].get_text().strip()) if title_tags else None

    @classmethod
    def get_company(cls, tag):
        company_tags = tag.select(":scope h4.result-card__subtitle")
        return normalize_spacing(company_tags[0].get_text().strip()) if company_tags else None

    @classmethod
    def get_url(cls, tag):
        title_tags = tag.select(":scope a.result-card__full-card-link")
        if title_tags:
            url = urljoin("https://seek.com.au/", title_tags[0]["href"].strip())
            return url[:url.index("?")] if ("?" in url) else url
        return None

    def parse(self, tag: Tag) -> Dict[str, Any]:
        job = super().parse(tag)
        job["scraped_time"] = self.creation_time_utc
        job["posted_time"] = self.get_posted_time(tag)
        job["location"] = self.get_location(tag)
        job["title"] = self.get_title(tag)
        job["company"] = self.get_company(tag)
        job["url"] = self.get_url(tag)
        return job
