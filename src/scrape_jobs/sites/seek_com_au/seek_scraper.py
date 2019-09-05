import logging
from collections import namedtuple
from typing import List

from hed_utils.selenium import driver
from hed_utils.support import log

from scrape_jobs.common.jobs_scraper import JobsScraper
from scrape_jobs.common.scrape_config import read_config
from scrape_jobs.sites.seek_com_au.seek_config import SeekConfig
from scrape_jobs.sites.seek_com_au.seek_page import SeekPage
from scrape_jobs.sites.seek_com_au.seek_result import SeekResult

ScrapeParams = namedtuple("ScrapeParams", "what where days tz")
UploadParams = namedtuple("UploadParams", "spreadsheet_name json_auth_file worksheet_index")


class SeekScraper(JobsScraper):
    def __init__(self, config: SeekConfig, page: SeekPage):
        super().__init__(config, page)

    def get_results_keys(self) -> List[str]:
        return SeekResult.get_dict_keys()


def start(config_file: str):
    config = SeekConfig(read_config(config_file))
    log.info("loaded config:\n%s", config)
    page = SeekPage()
    scraper = SeekScraper(config, page)
    scraper.start()


def main():
    # left for testing
    # config_path = Path("/home/re/CODE/PycharmProjects/scrape-jobs.ini")
    # start(str(config_path))
    pass


if __name__ == '__main__':
    log.init(logging.INFO)
    try:
        main()
    except:
        log.exception("error in main!")
    finally:
        driver.quit()
