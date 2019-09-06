from datetime import datetime
from typing import Optional, List
from urllib.parse import urljoin

from hed_utils.support import time_tool

from scrape_jobs.common.job_result import JobResult


class SeekJobResult(JobResult):

    @classmethod
    def keys(cls) -> List[str]:
        return ["utc_datetime", "location", "title", "company", "classification", "url", "salary"]

    def get_utc_datetime(self) -> Optional[datetime]:
        try:
            posted = self.soup.select_one("span[data-automation='jobListingDate']").get_text().strip()
            delta = time_tool.TimedeltaParser.parse(posted)
            return time_tool.utc_moment() - delta
        except:
            return None

    def get_location(self) -> Optional[str]:
        try:
            city = self.soup.select_one("a[data-automation='jobLocation']").get_text().strip()
        except:
            city = ""
        try:
            area = self.soup.select_one("a[data-automation='jobArea']").get_text().strip()
        except:
            area = ""

        components = [c.strip() for c in [city, area] if c.strip()]
        if components:
            return ", ".join(components)
        else:
            return None

    def get_title(self) -> Optional[str]:
        try:
            return self.soup.select_one("a[data-automation='jobTitle']").get_text().strip()
        except:
            return None

    def get_company(self) -> Optional[str]:
        try:
            return self.soup.select_one("a[data-automation='jobCompany']").get_text().strip()
        except:
            return None

    def get_url(self) -> Optional[str]:
        try:
            a = self.soup.select_one("a[data-automation='jobTitle']")
            domain = "https://www.seek.com.au/"
            link = urljoin(domain, a["href"])
            return link[:link.index("?")]
        except:
            return None

    def get_classification(self) -> Optional[str]:
        try:
            main_classification = self.soup.select_one("a[data-automation='jobClassification']").get_text().strip()
        except:
            main_classification = ""

        try:
            sub_classification = self.soup.select_one("a[data-automation='jobSubClassification']").get_text().strip()
        except:
            sub_classification = ""

        components = [c.strip() for c in [main_classification, sub_classification] if c.strip()]
        if components:
            return ", ".join(components)
        else:
            return None

    def get_salary(self) -> Optional[str]:
        try:
            return self.soup.select_one("span[data-automation='jobSalary']").get_text().strip()
        except:
            return None
