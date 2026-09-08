# Architecture

The service separates request handling from processing work.

## Data flow

1. Client registers an asset.
2. SHA-256 generates a deterministic content identifier.
3. Metadata is stored through the repository abstraction.
4. A processing job is created.
5. A worker performs validation and metadata extraction.
6. Job state transitions to succeeded or failed.
7. Hot assets can be served from the TTL cache.

## Production evolution

Replace the reference repository with PostgreSQL, the content store with S3/GCS/Azure Blob, and the local executor with a distributed queue and worker fleet.
