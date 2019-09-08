from datetime import datetime
from typing import Optional

from hed_utils.support import time_tool

from scrape_jobs.common.job_result import JobResult


class LinkedinJobResult(JobResult):

    def get_utc_datetime(self) -> Optional[datetime]:
        try:
            date_text_local = self.tag.select_one("time")["datetime"].strip()
            datetime_local = datetime.strptime(date_text_local, "%Y-%m-%d")
            return time_tool.localize(datetime_local, "UTC")
        except:
            return None

    def get_location(self) -> Optional[str]:
        try:
            return self.tag.select_one("span.job-result-card__location").get_text().strip()
        except:
            return None

    def get_title(self) -> Optional[str]:
        try:
            return self.tag.select_one("h3.job-result-card__title").get_text().strip()
        except:
            return None

    def get_company(self) -> Optional[str]:
        try:
            return self.tag.select_one("h4.result-card__subtitle").get_text().strip()
        except:
            return None

    def get_url(self) -> Optional[str]:
        try:
            a = self.tag.select_one("a.result-card__full-card-link")
            url = a["href"]
            return url[:url.index("?")]
        except:
            return None
