import logging

from scrape_jobs.base.data_collection import ACollector
from scrape_jobs.base.data_processing import AProcessor
from scrape_jobs.base.data_storage import AStorage

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class Program:
    def __init__(self, collector: ACollector, processor: AProcessor, storage: AStorage):
        self.collector = collector
        self.processor = processor
        self.storage = storage

    def execute(self):
        try:
            _log.info("Collecting jobs...")
            collected_jobs = self.collector.collect_jobs()
            _log.info("Done with jobs collection! (got %s jobs)", len(collected_jobs))
        except BaseException as err:
            _log.exception("Error while collecting data! (%s) %s", type(err).__name__, err)
            raise RuntimeError() from err

        try:
            _log.info("Filtering known jobs to avoid extra processing...")
            known_jobs_urls = self.storage.get_known_jobs_urls()
            previously_unknown_jobs = [job for job in collected_jobs if job["url"] not in known_jobs_urls]
            _log.info("Got %s new out of %s collected jobs!", len(previously_unknown_jobs), len(collected_jobs))
        except BaseException as err:
            _log.exception("Error while filtering collected jobs! (%s) %s", type(err).__name__, err)
            raise RuntimeError() from err

        if not previously_unknown_jobs:
            _log.warning("There were no previously unknown jobs - all done!")
            return

        try:
            _log.info("Processing new jobs...")
            processed_jobs = self.processor.process_jobs(previously_unknown_jobs)
            _log.info("Done with jobs processing!")
        except BaseException as err:
            _log.exception("Error while processing collected jobs! (%s) %s", type(err).__name__, err)
            raise RuntimeError() from err

        try:
            _log.info("Saving processed jobs...")
            self.storage.store_jobs(processed_jobs)
            _log.info("Saved %s jobs!", len(processed_jobs))
        except BaseException as err:
            _log.exception("Error while storing processed jobs! (%s) %s", type(err).__name__, err)
            raise RuntimeError() from err
