from fastapi import FastAPI, HTTPException

from asset_platform.cache.cache import TTLCache
from asset_platform.config import Settings
from asset_platform.domain.models import Asset, AssetCreate
from asset_platform.domain.services import content_hash
from asset_platform.observability.metrics import Metrics
from asset_platform.processing.engine import ProcessingEngine
from asset_platform.storage.repository import AssetRepository

settings = Settings()
repository = AssetRepository()
cache = TTLCache(settings.cache_ttl_seconds)
metrics = Metrics()
engine = ProcessingEngine(repository, settings.worker_count, settings.max_retries)

app = FastAPI(title="Cloud-Native 3D Asset Processing Platform", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/assets", response_model=Asset, status_code=201)
def register_asset(payload: AssetCreate):
    digest = content_hash(payload.content)
    asset_id = digest[:24]
    existing = repository.get_asset(asset_id)
    if existing:
        return existing

    asset = Asset(
        asset_id=asset_id,
        name=payload.name,
        format=payload.format,
        size_bytes=len(payload.content.encode("utf-8")),
        content_hash=digest,
    )
    repository.save_asset(asset)
    cache.set(f"asset:{asset_id}", asset)
    metrics.inc("assets_registered")
    return asset


@app.get("/assets/{asset_id}", response_model=Asset)
def get_asset(asset_id: str):
    cached = cache.get(f"asset:{asset_id}")
    if cached:
        return cached
    asset = repository.get_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="asset not found")
    cache.set(f"asset:{asset_id}", asset)
    return asset


@app.post("/assets/{asset_id}/process")
def process(asset_id: str):
    asset = repository.get_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="asset not found")
    job = engine.submit(asset)
    metrics.inc("jobs_submitted")
    return job


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = repository.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@app.get("/metrics")
def metrics_endpoint():
    return metrics.prometheus()


@app.on_event("shutdown")
def shutdown():
    engine.shutdown()
