#!/usr/bin/env python3
"""
added function anotation to the below function
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """return list of tuple with sequence and len"""
    return [(i, len(i)) for i in lst]
