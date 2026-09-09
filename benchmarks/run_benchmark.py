import time

from asset_platform.domain.services import content_hash


def main():
    samples = []
    iterations = 5000
    for _ in range(iterations):
        start = time.perf_counter_ns()
        content_hash("benchmark-3d-asset-content")
        samples.append((time.perf_counter_ns() - start) / 1_000_000)

    samples.sort()
    p50 = samples[len(samples) // 2]
    p95 = samples[int(len(samples) * 0.95)]
    p99 = samples[int(len(samples) * 0.99)]
    total_seconds = sum(samples) / 1000
    throughput = iterations / total_seconds if total_seconds else 0

    print(f"iterations={iterations}")
    print(f"throughput_ops_per_sec={throughput:.2f}")
    print(f"latency_ms_p50={p50:.4f}")
    print(f"latency_ms_p95={p95:.4f}")
    print(f"latency_ms_p99={p99:.4f}")


if __name__ == "__main__":
    main()
