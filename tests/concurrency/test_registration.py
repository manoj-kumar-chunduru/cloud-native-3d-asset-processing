from concurrent.futures import ThreadPoolExecutor
from asset_platform.domain.services import content_hash

def test_hash_is_thread_safe():
    with ThreadPoolExecutor(max_workers=8) as pool:
        values = list(pool.map(content_hash, ["scene"] * 100))
    assert len(set(values)) == 1
