#!/usr/bin/env python3
"""
Module: element of a sequence anotation
"""
from typing import Mapping, Any, Union, TypeVar
Tv = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[Tv, None] = None) -> Union[Any, Tv]:
    """
    return values safely
    """
    if key in dct:
        return dct[key]
    else:
        return default
