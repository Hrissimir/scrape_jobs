from typing import List

from scrape_jobs.base.job import Job

__all__ = [
    "SeekJob"
]


class SeekJob(Job):
    _KEYS = ["scraped_time",
             "posted_time",
             "location",
             "area",
             "classification",
             "sub_classification",
             "title",
             "salary",
             "company",
             "url"]

    def __init__(self, *,
                 scraped_time, posted_time,
                 location, area,
                 classification, sub_classification,
                 title, salary, company, url):

        self.scraped_time = scraped_time
        self.posted_time = posted_time
        self.location = location
        self.area = area
        self.classification = classification
        self.sub_classification = sub_classification
        self.title = title
        self.salary = salary
        self.company = company
        self.url = url

    @classmethod
    def keys(cls) -> List[str]:
        return cls._KEYS.copy()
