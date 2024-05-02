#!/usr/bin/env python3
"""
Simple pagination
"""

import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """Function definition here"""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        dataset = self.dataset()
        total_pages = math.ceil(len(dataset) / page_size)

        if page > total_pages:
            return []

        idx_tuple = index_range(page, page_size)
        page_data = dataset[idx_tuple[0]: idx_tuple[1]]

        return page_data
