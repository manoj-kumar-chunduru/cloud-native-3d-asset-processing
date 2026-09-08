from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    worker_count: int = int(os.getenv("ASSET_WORKERS", "4"))
    max_retries: int = int(os.getenv("ASSET_MAX_RETRIES", "2"))
    cache_ttl_seconds: int = int(os.getenv("ASSET_CACHE_TTL", "300"))
