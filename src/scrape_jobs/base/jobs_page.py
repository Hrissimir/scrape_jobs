import datetime
from typing import List, Dict, Optional

import pytz
from hed_utils.selenium.page_objects.base.web_page import WebPage
from hed_utils.support import log
from hed_utils.support.time_tool import get_local_tz_name, get_local_datetime, convert_to_tz

from scrape_jobs.base.job_result import JobResult

JobsData = List[Dict[str, str]]


class JobsPage(WebPage):

    @classmethod
    def get_stop_datetime(cls, past_n_days: int, *, tz_name: Optional[str] = None) -> datetime.datetime:
        tz_name = tz_name or get_local_tz_name()
        local_datetime = get_local_datetime()
        local_stop_datetime = local_datetime - datetime.timedelta(days=past_n_days)
        return convert_to_tz(local_stop_datetime, tz_name)

    @classmethod
    def parse_datetime_string(cls,
                              value: str, *,
                              fmt="%Y-%m-%d",
                              tz_name: Optional[str] = None) -> Optional[datetime.datetime]:
        try:
            tz_name = tz_name or get_local_tz_name()
            tz = pytz.timezone(tz_name)
            dt = datetime.datetime.strptime(value, fmt)
            return tz.localize(dt)
        except:
            return None

    def get_visible_jobs(self) -> List[JobResult]:
        raise NotImplementedError()

    def enter_search_details(self, query: str, location: str):
        raise NotImplementedError()

    def trigger_search(self):
        raise NotImplementedError()

    def wait_for_results(self) -> bool:
        raise NotImplementedError()

    def view_next_results_page(self):
        raise NotImplementedError()

    def collect_most_recent_jobs(self,
                                 query: str,
                                 location: str,
                                 past_n_days: int,
                                 tz_name: Optional[str]) -> JobsData:
        tz_name = tz_name or get_local_tz_name()
        stop_datetime = self.get_stop_datetime(past_n_days, tz_name=tz_name)
        log.info("collecting most recent jobs "
                 "(query='%s', location='%s', past_n_days='%s', tz_name='%s', stop_datetime='%s')",
                 query, location, past_n_days, tz_name, stop_datetime)

        most_recent_jobs: JobsData = []

        def is_new_job(job_data: Dict[str, str]):
            same_jobs = [j for j in most_recent_jobs if j["url"] == job_data["url"]]
            return not bool(same_jobs)

        self.enter_search_details(query, location)
        self.trigger_search()

        current_pageno = 1
        is_first_bad_page = True

        while True:
            log.info("processing jobs results on page #:%s", current_pageno)

            if not self.wait_for_results():
                log.warning("there weren't any results on page #:%s", current_pageno)
                if is_first_bad_page:
                    is_first_bad_page = False
                    self.view_next_results_page()
                    current_pageno += 1
                    continue
                else:
                    log.warning("page #:%s was the second page with no results in a row - stopping results iteration!")
                    break

            current_page_new_jobs = []

            visible_jobs = self.get_visible_jobs()

            for current_job in visible_jobs:
                current_job_data = current_job.as_dict(tz_name)

                # skip jobs that were already collected
                if not is_new_job(current_job_data):
                    continue

                # skip older jobs and jobs with no date
                job_post_datetime = self.parse_datetime_string(current_job_data["date"], tz_name=tz_name)
                if (not job_post_datetime) or (job_post_datetime.date() < stop_datetime.date()):
                    continue

                current_page_new_jobs.append(current_job_data)

            is_bad_page = not (bool(current_page_new_jobs))

            if is_bad_page:
                log.info("page #:%s was a bad page - it had no unseen jobs", current_pageno)
                if is_first_bad_page:
                    log.warning("this was first bad page, will stop results iteration on next occasion")
                    is_first_bad_page = False
                    self.view_next_results_page()
                    current_pageno += 1
                    continue
                else:
                    log.warning("page #%s was second bad page in a row - done with results iteration!", current_pageno)
                    break
            else:
                is_first_bad_page = True
                log.info("found %s unseen jobs on page #:%s", len(current_page_new_jobs), current_pageno)
                most_recent_jobs.extend(current_page_new_jobs)
                self.view_next_results_page()
                current_pageno += 1

        log.info("collected total of %s matching jobs for the pas %s days", len(most_recent_jobs), past_n_days)
        most_recent_jobs.sort(key=lambda j: self.parse_datetime_string(j["date"], tz_name=tz_name))
        return most_recent_jobs
