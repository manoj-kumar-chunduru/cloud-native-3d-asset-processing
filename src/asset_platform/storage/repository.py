from threading import RLock

from asset_platform.domain.models import Asset, Job


class AssetRepository:
    def __init__(self):
        self._assets: dict[str, Asset] = {}
        self._jobs: dict[str, Job] = {}
        self._lock = RLock()

    def save_asset(self, asset: Asset) -> Asset:
        with self._lock:
            self._assets[asset.asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> Asset | None:
        with self._lock:
            return self._assets.get(asset_id)

    def save_job(self, job: Job) -> Job:
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)
