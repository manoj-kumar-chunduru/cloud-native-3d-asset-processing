# Cloud-Native 3D Asset Processing Pipeline

A production-oriented reference platform for asynchronous 3D asset processing, spatial metadata extraction, content-addressed deduplication, caching, observability, and cloud-native deployment.

## Overview

This project demonstrates backend engineering patterns commonly used in media, AR/VR, and cloud platforms:

- REST APIs for asset registration and processing jobs
- SHA-256 content addressing and duplicate detection
- Bounded asynchronous worker execution
- Idempotent job processing
- Retry and failure handling
- Metadata extraction from lightweight asset manifests
- Cache abstraction for hot metadata
- Structured logging and Prometheus-compatible metrics
- Health/readiness endpoints
- Docker and Kubernetes deployment artifacts
- Unit, integration, concurrency, and benchmark tests

The implementation is intentionally self-contained. It does not claim production benchmark numbers from a specific employer; benchmark results should be generated on the target hardware and workload.

## Architecture

```text
Client
  |
  v
FastAPI
  |
  +---- Asset Registry ----> Content Store
  |
  +---- Job Dispatcher ----> Worker Pool
  |                              |
  |                              +--> Metadata Processor
  |                              +--> Spatial Processor
  |                              +--> Validation
  |
  +---- Cache <------------------+
  |
  +---- Metrics / Health
```

## Tech Stack

- Python 3.11+
- FastAPI + Pydantic
- pytest
- Ruff
- ThreadPoolExecutor
- Docker / Docker Compose
- Kubernetes manifests
- Prometheus-compatible metrics format

## Key Design Decisions

### Content addressing

Assets are identified by SHA-256 digest. This makes duplicate detection deterministic and creates a stable identifier for storage and cache keys.

### Asynchronous processing

API requests register work and return a job identifier instead of performing expensive processing synchronously. A bounded worker pool limits resource consumption.

### Idempotency

A job can be retried safely using its stable job identifier. Terminal job state is persisted by the in-memory reference implementation.

### Cache abstraction

The cache interface is intentionally separated from business logic so Redis can be introduced without rewriting the asset-processing domain.

## API Examples

Register an asset:

```bash
curl -X POST http://localhost:8000/assets   -H "Content-Type: application/json"   -d '{"name":"chair.glb","content":"sample-3d-asset","format":"glb"}'
```

Start processing:

```bash
curl -X POST http://localhost:8000/assets/<asset_id>/process
```

Inspect job status:

```bash
curl http://localhost:8000/jobs/<job_id>
```

Health:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

Metrics:

```bash
curl http://localhost:8000/metrics
```

## Project Structure

```text
src/asset_platform/
├── api.py
├── config.py
├── domain/
│   ├── models.py
│   └── services.py
├── processing/
│   ├── engine.py
│   └── processors.py
├── storage/
│   └── repository.py
├── cache/
│   └── cache.py
└── observability/
    └── metrics.py
```

## Running Locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -e ".[dev]"
uvicorn asset_platform.api:app --reload
```

OpenAPI documentation is available at `/docs`.

## Testing

```bash
pytest
ruff check .
```

## Benchmarking

```bash
python benchmarks/run_benchmark.py
```

The benchmark reports throughput and latency for asset registration and job submission. Results depend on CPU, memory, Python version, concurrency, and workload.

## Docker

```bash
docker build -t cloud-native-3d-asset-processing .
docker run --rm -p 8000:8000 cloud-native-3d-asset-processing
```

Or:

```bash
docker compose up --build
```

## Kubernetes

The `k8s/` directory contains deployment and service examples.

```bash
kubectl apply -f k8s/
```

The reference implementation uses in-memory state, so Kubernetes manifests are intended as deployment-learning artifacts. A production deployment should use durable object storage, a shared database, and a distributed queue.

## Reliability Considerations

- bounded worker concurrency
- deterministic asset identifiers
- idempotent job identifiers
- explicit job states
- retry limits
- readiness checks
- structured metrics
- graceful worker shutdown

## Future Improvements

- S3/GCS/Azure Blob integration
- Redis-backed cache
- PostgreSQL metadata store
- Kafka or managed queue integration
- GPU worker pool for expensive transforms
- OpenTelemetry tracing
- real GLTF/GLB validation and geometry extraction
- CDN delivery for processed assets
- autoscaling based on queue depth

## Engineering Principles

- separate API, domain, processing, and infrastructure layers
- prefer deterministic identifiers
- keep expensive work off request threads
- make retries explicit and bounded
- measure before optimizing
- design interfaces for replaceable infrastructure

## Security

See `SECURITY.md`.

## Contributing

See `CONTRIBUTING.md`.

## Author

**Manoj Kumar Chunduru**  
Software Engineer
