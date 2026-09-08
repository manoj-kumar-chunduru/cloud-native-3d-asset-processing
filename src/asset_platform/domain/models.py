from enum import Enum
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class AssetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    format: str = Field(min_length=1, max_length=20)

class Asset(BaseModel):
    asset_id: str
    name: str
    format: str
    size_bytes: int
    content_hash: str
    metadata: dict = Field(default_factory=dict)

class Job(BaseModel):
    job_id: str
    asset_id: str
    status: JobStatus
    attempts: int = 0
    error: str | None = None
    result: dict | None = None
