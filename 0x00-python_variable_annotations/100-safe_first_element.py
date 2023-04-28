#!/usr/bin/env python3
"""Augmented the following code
with the correct duck-typed annotations"""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Safe first element: types of the element not known
    """
    if lst:
        return lst[0]
    else:
        return None
