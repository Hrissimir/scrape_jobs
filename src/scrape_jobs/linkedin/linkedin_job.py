from typing import List

from scrape_jobs.base.job import Job

__all__ = [
    "LinkedinJob"
]


class LinkedinJob(Job):
    _KEYS = ["scraped_time",
             "posted_time",
             "location",
             "title",
             "company",
             "url"]

    def __init__(self, *,
                 scraped_time,
                 posted_time,
                 location,
                 title,
                 company,
                 url):
        self.scraped_time = scraped_time
        self.posted_time = posted_time
        self.location = location
        self.title = title
        self.company = company
        self.url = url

    @classmethod
    def keys(cls) -> List[str]:
        return cls._KEYS.copy()
