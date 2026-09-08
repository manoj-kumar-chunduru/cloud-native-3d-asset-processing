import time
from asset_platform.domain.services import content_hash

def test_hash_throughput_smoke():
    start = time.perf_counter()
    for _ in range(1000):
        content_hash("benchmark-asset")
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0
