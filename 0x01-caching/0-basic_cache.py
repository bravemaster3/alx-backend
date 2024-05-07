#!/usr/bin/env python3
"""
class BasicCache that inherits from BaseCaching and is a caching system:
"""

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """Class definition here"""
    def put(self, key, item):
        """inserts a key: item into the cache"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """returns the value of a key"""
        if not key or key not in self.cache_data:
            return None
        return self.cache_data[key]
