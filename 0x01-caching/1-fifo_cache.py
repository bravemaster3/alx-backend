#!/usr/bin/env python3
"""
class FIFOCache that inherits from BaseCaching and is a caching system:
"""

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """Class definition here"""
    def put(self, key, item):
        """inserts a key: item into the cache"""
        max_items = BaseCaching.MAX_ITEMS
        if not key or not item:
            return
        elif len(self.cache_data) < max_items or key in self.cache_data:
            self.cache_data[key] = item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD:", first_key)
            self.cache_data[key] = item

    def get(self, key):
        """returns the value of a key"""
        if not key or key not in self.cache_data:
            return None
        return self.cache_data[key]
