from threading import Lock

class Metrics:
    def __init__(self):
        self._lock = Lock()
        self.assets_registered = 0
        self.jobs_submitted = 0
        self.jobs_succeeded = 0
        self.jobs_failed = 0

    def inc(self, field: str) -> None:
        with self._lock:
            setattr(self, field, getattr(self, field) + 1)

    def prometheus(self) -> str:
        return "\n".join([
            "# HELP asset_platform_assets_registered Total registered assets",
            "# TYPE asset_platform_assets_registered counter",
            f"asset_platform_assets_registered {self.assets_registered}",
            "# HELP asset_platform_jobs_submitted Total submitted jobs",
            "# TYPE asset_platform_jobs_submitted counter",
            f"asset_platform_jobs_submitted {self.jobs_submitted}",
            "# HELP asset_platform_jobs_succeeded Total successful jobs",
            "# TYPE asset_platform_jobs_succeeded counter",
            f"asset_platform_jobs_succeeded {self.jobs_succeeded}",
            "# HELP asset_platform_jobs_failed Total failed jobs",
            "# TYPE asset_platform_jobs_failed counter",
            f"asset_platform_jobs_failed {self.jobs_failed}",
        ])
