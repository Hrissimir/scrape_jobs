import logging
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
        return LinkedinJobResult.keys()


def start(config_file: str):
    config = LinkedinConfig(read_config(config_file))
    log.info("loaded config:\n%s", config)
    page = LinkedinJobsPage()
    scraper = LinkedinJobsScraper(config, page)
    scraper.start()


def main():
    # left for testing
    # config_path = Path("/home/re/CODE/PycharmProjects/scrape-jobs.ini")
    # config_file = str(config_path)
    # config = LinkedinConfig(read_config(config_file))
    # log.info("loaded config:\n%s", config)
    # page = LinkedinJobsPage()
    # scraper = LinkedinJobsScraper(config, page)
    # driver.start_chrome()
    # scraper.page.go_to()
    # scraper.page.set_search_params(**scraper.config.get_search_params())
    # driver.save_source("linkedin_search.html")
    # driver.quit()
    pass


if __name__ == '__main__':
    log.init(logging.INFO)
    try:
        main()
    except:
        log.exception("error in main!")
    finally:
        driver.quit()
