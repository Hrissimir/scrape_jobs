import logging

from scrape_jobs.base import (
    Datastore,
    init_driver,
    TimeConfig
)
from scrape_jobs.base.datastore import SheetsDatastore
from scrape_jobs.base.scraper import Scraper
from scrape_jobs.seek import SeekConfig, SeekJob, SeekPage

__all__ = [
    "Program"
]
CONFIG_CLASSES = {
    "seek.com.au": SeekConfig
}

JOB_CLASSES = {
    "seek.com.au": SeekJob
}

PAGES = {
    "seek.com.au": SeekPage()
}

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class Program:
    time_config: TimeConfig
    datastore: Datastore
    scraper: Scraper

    def __init__(self):
        self.time_config = None
        self.datastore = None
        self.scraper = None

    @classmethod
    def init(cls, site: str, configfile: str):
        _log.info("initializing program: site='%s', configfile='%s'", site, configfile)

        cfg = CONFIG_CLASSES[site].from_file(configfile)
        _log.info("got config: %s", cfg)

        time_cfg = cfg.time_config
        sheets_cfg = cfg.sheets_config
        search_cfg = cfg.search_config

        init_driver(search_cfg.driver_headless)

        program = cls()
        program.time_config = time_cfg
        program.datastore = SheetsDatastore(config=sheets_cfg, job_cls=JOB_CLASSES[site])
        program.scraper = Scraper(page=PAGES[site],
                                  search_params=search_cfg.search_params,
                                  utc_posted_after=search_cfg.utc_posted_after,
                                  known_jobs_urls=program.datastore.get_known_jobs_urls())

        return program

    def start(self):
        _log.info("scraping jobs...")

        jobs = self.scraper.scrape()

        if not jobs:
            _log.warning("no new jobs were collected!")
        else:
            _log.info("preparing [ %s ] jobs for upload...", len(jobs))
            for job in jobs:
                job.prepare_for_upload(time_config=self.time_config)

            _log.info("uploading jobs...")
            self.datastore.add_jobs(jobs)

        _log.info("all done!")
