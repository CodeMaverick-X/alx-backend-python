#!/usr/bin/env python3
"""
module that contains  a type-annotated
function sum_mixed_list which takes a list
mxd_lst of integers and floats and returns
their sum as a float.
"""


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """return sum of list as float"""
    sum_list: float = 0

    for val in mxd_lst:
        sum_list += val
    return sum_list
