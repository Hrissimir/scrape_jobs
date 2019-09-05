import logging
from pathlib import Path
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs.common.jobs_scraper import JobsScraper
from scrape_jobs.common.scrape_config import read_config
from scrape_jobs.sites.linkedin_com.linkedin_config import LinkedinConfig
from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult
from scrape_jobs.sites.linkedin_com.linkedin_jobs_page import LinkedinJobsPage


class LinkedinJobsScraper(JobsScraper):

    def __init__(self, config: LinkedinConfig, page: LinkedinJobsPage):
        super().__init__(config, page)

    def get_results_keys(self) -> List[str]:
        return LinkedinJobResult.get_dict_keys()


def start(config_file: str):
    config = LinkedinConfig(read_config(config_file))
    page = LinkedinJobsPage()
    scraper = LinkedinJobsScraper(config, page)
    scraper.start()


def main():
    # left for testing
    from pprint import pprint

    config_path = Path("/home/re/CODE/PycharmProjects/scrape-jobs.ini")

    config = LinkedinConfig(read_config(str(config_path)))
    page = LinkedinJobsPage()

    scraper = LinkedinJobsScraper(config, page)
    scraper.check_for_upload_errors()

    # pprint(scraper.get_known_jobs_urls())
    # start(str(config_path))

    results = scraper.scrape_raw_results_data()
    scraper.set_posted_timestamps(results)

    rows = scraper.convert_to_rows(results)
    scraper.set_scraped_timestamps(rows)

    pprint(rows, width=1000)


if __name__ == '__main__':
    log.init(logging.INFO)
    driver.start_chrome()
    try:
        main()
    except:
        log.exception("error in main!")
    finally:
        driver.quit()
