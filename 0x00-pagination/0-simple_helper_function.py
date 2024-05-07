#!/usr/bin/env python3
"""
Helper function for pagination
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Function definition here"""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
