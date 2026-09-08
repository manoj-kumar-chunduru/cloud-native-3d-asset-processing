from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import time
import uuid

from asset_platform.domain.models import Asset, Job, JobStatus
from asset_platform.processing.processors import process_asset
from asset_platform.storage.repository import AssetRepository

class ProcessingEngine:
    def __init__(self, repository: AssetRepository, worker_count: int = 4, max_retries: int = 2):
        self.repository = repository
        self.max_retries = max_retries
        self.executor = ThreadPoolExecutor(max_workers=max(1, worker_count))
        self._active: set[str] = set()
        self._lock = RLock()

    def submit(self, asset: Asset) -> Job:
        job = Job(job_id=str(uuid.uuid4()), asset_id=asset.asset_id, status=JobStatus.QUEUED)
        self.repository.save_job(job)
        self.executor.submit(self._run, job.job_id, asset)
        return job

    def _run(self, job_id: str, asset: Asset) -> None:
        job = self.repository.get_job(job_id)
        if job is None:
            return
        with self._lock:
            if job_id in self._active:
                return
            self._active.add(job_id)
        try:
            for attempt in range(1, self.max_retries + 2):
                job.status = JobStatus.RUNNING
                job.attempts = attempt
                self.repository.save_job(job)
                try:
                    result = process_asset(asset)
                    job.status = JobStatus.SUCCEEDED
                    job.result = result
                    job.error = None
                    self.repository.save_job(job)
                    return
                except Exception as exc:
                    job.error = str(exc)
                    if attempt > self.max_retries:
                        job.status = JobStatus.FAILED
                        self.repository.save_job(job)
                        return
                    time.sleep(0.01 * attempt)
        finally:
            with self._lock:
                self._active.discard(job_id)

    def shutdown(self) -> None:
        self.executor.shutdown(wait=True)
