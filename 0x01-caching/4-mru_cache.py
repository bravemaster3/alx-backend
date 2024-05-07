#!/usr/bin/env python3
"""
class MRUCache that inherits from BaseCaching and is a caching system:
"""

BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """Class definition here"""

    def put(self, key, item):
        """inserts a key: item into the cache"""
        max_items = BaseCaching.MAX_ITEMS
        if not key or not item:
            return
        elif key in self.cache_data:
            value = self.cache_data.pop(key)
            self.cache_data[key] = item
        elif len(self.cache_data) < max_items:
            self.cache_data[key] = item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_key]
            print("DISCARD:", last_key)
            self.cache_data[key] = item

    def get(self, key):
        """returns the value of a key"""
        if not key or key not in self.cache_data:
            return None
        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        return value
