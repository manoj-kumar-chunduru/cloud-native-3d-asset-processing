from threading import RLock
import time

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._items: dict[str, tuple[float, object]] = {}
        self._lock = RLock()

    def get(self, key: str):
        with self._lock:
            item = self._items.get(key)
            if item is None:
                return None
            expires, value = item
            if time.monotonic() >= expires:
                self._items.pop(key, None)
                return None
            return value

    def set(self, key: str, value: object) -> None:
        with self._lock:
            self._items[key] = (time.monotonic() + self._ttl, value)
