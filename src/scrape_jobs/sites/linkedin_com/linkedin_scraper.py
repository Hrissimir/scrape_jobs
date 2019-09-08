import logging
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log
from hed_utils.support.config_base import ConfigBase

from scrape_jobs.common.jobs_scraper import JobsScraper
from scrape_jobs.common.jobs_uploader import JobsUploader
from scrape_jobs.common.scrape_config import read_config
from scrape_jobs.sites.linkedin_com.linkedin_config import LinkedinScrapeConfig, LinkedinUploadConfig
from scrape_jobs.sites.linkedin_com.linkedin_job_result import LinkedinJobResult
from scrape_jobs.sites.linkedin_com.linkedin_jobs_page import LinkedinJobsPage


class LinkedinJobsScraper(JobsScraper):

    def __init__(self, config: LinkedinScrapeConfig, page: LinkedinJobsPage):
        super().__init__(config, page)

    def get_results_keys(self) -> List[str]:
        return LinkedinJobResult.keys()


def scrape_and_upload(config_file: str):
    cfg = read_config(config_file)
    log.info("loaded config from '%s' :\n%s", config_file, ConfigBase.format_config(cfg))

    upload_config = LinkedinUploadConfig(cfg)
    uploader = JobsUploader(upload_config)
    uploader.check_for_upload_errors()

    scrape_config = LinkedinScrapeConfig(cfg)
    page = LinkedinJobsPage()
    scraper = LinkedinJobsScraper(scrape_config, page)

    jobs = scraper.scrape_jobs()
    uploader.upload_jobs(jobs)


def main():
    # left for testing
    from pathlib import Path
    config_path = Path("/home/re/PycharmProjects/scrape-jobs.ini")
    config_file = str(config_path)
    scrape_and_upload(config_file)


if __name__ == '__main__':
    log.init(logging.INFO)
    try:
        main()
    except:
        log.exception("error in main!")
    finally:
        driver.quit()
