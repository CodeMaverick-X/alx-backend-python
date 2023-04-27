#!/usr/bin/env python3
"""
module that contains a type-annotated
function make_multiplier that takes a
float multiplier as argument and returns
a function that multiplies a float by multiplier.
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """returns a function"""
    def fun(n: float) -> float:
        return n * multiplier

    return fun
