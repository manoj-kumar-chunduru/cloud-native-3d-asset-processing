# ADR 0001: Asynchronous Processing

## Status
Accepted

## Decision
Expensive asset processing is executed asynchronously through a worker pool.

## Rationale
Keeping processing off the API request path improves responsiveness and allows worker capacity to scale independently.

## Trade-off
The reference implementation needs durable queue infrastructure before it can safely support process crashes and multi-instance execution.
