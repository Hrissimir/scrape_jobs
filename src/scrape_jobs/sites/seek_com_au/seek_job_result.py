from typing import List, Optional, Dict
from urllib.parse import urljoin

from hed_utils.selenium.wrappers.element_wrapper import ElementWrapper

from scrape_jobs.base.job_result import JobResult


class SeekJobResult(JobResult):
    def __init__(self, element: ElementWrapper):
        self._soup = element.soup

    @classmethod
    def get_dict_keys(cls) -> List[str]:
        return super().get_dict_keys() + ["is_featured", "salary"]

    def get_post_date_value(self) -> str:
        try:
            return self._soup.select_one("span[data-automation='jobListingDate']").get_text().strip()
        except:
            return ""

    def get_title(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobTitle']").get_text().strip()
        except:
            return "NO_TITLE"

    def get_location(self) -> str:
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

    def get_company(self) -> str:
        try:
            return self._soup.select_one("a[data-automation='jobCompany']").get_text().strip()
        except:
            return "NO_COMPANY"

    def get_classification(self) -> str:
        try:
            main_classification = self._soup.select_one("a[data-automation='jobClassification']").get_text().strip()
        except:
            main_classification = ""

        try:
            sub_classification = self._soup.select_one("a[data-automation='jobSubClassification']").get_text().strip()
        except:
            sub_classification = ""

        components = [c.strip() for c in [main_classification, sub_classification] if c.strip()]
        return ", ".join(components)

    def get_url(self) -> str:
        try:
            a = self._soup.select_one("a[data-automation='jobTitle']")
            domain = "https://www.seek.com.au/"
            link = urljoin(domain, a["href"])
            return link[:link.index("?")]
        except:
            return "NO_URL"

    def get_salary(self) -> str:
        try:
            return self._soup.select_one("span[data-automation='jobSalary']").get_text().strip()
        except:
            return "NO_SALARY"

    def is_featured(self) -> bool:
        try:
            return self._soup.select_one("span[data-automation='jobPremium']") is not None
        except:
            return False

    def as_dict(self, tz_name: Optional[str] = None) -> Dict[str, str]:
        base_dict = super().as_dict(tz_name)
        base_dict["is_featured"] = str(self.is_featured())
        base_dict["salary"] = str(self.get_salary())
        return base_dict
