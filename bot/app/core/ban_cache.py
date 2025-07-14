from cachetools import TTLCache


ban_cache: TTLCache[str, bool] = TTLCache(maxsize=100_000, ttl=300)
