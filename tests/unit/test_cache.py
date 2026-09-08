from asset_platform.cache.cache import TTLCache

def test_cache_round_trip():
    cache = TTLCache(ttl_seconds=60)
    cache.set("key", {"value": 1})
    assert cache.get("key") == {"value": 1}
