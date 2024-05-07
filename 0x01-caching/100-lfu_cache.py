#!/usr/bin/env python3
"""
class LFUCache that inherits from BaseCaching and is a caching system:
"""

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """Class definition here"""
    def __init__(self):
        """instanciation method"""
        super().__init__()
        self.freq_dict = {}

    def put(self, key, item):
        """inserts a key: item into the cache"""
        max_items = BaseCaching.MAX_ITEMS
        if not key or not item:
            return
        elif key in self.cache_data:
            # value = self.cache_data.pop(key)
            self.cache_data[key] = item
        elif len(self.cache_data) < max_items:
            self.cache_data[key] = item
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # last_key = list(self.cache_data.keys())[-1]
            min_key = min(self.freq_dict, key=lambda k: self.freq_dict[k])
            # print("**********", min_key)
            del self.cache_data[min_key]
            del self.freq_dict[min_key]
            print("DISCARD:", min_key)
            self.cache_data[key] = item

        if key not in self.freq_dict:
            self.freq_dict[key] = 1
        else:
            self.freq_dict[key] += 1

    def get(self, key):
        """returns the value of a key"""
        if not key or key not in self.cache_data:
            if key in self.freq_dict:
                del self.freq_dict[key]
            return None
        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        self.freq_dict[key] += 1
        return value
