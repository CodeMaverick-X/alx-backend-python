#!/usr/bin/env python3
"""
contains a function `async_comprehension`
recieve 10 random numbers from a async_gen..
"""
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """returns list of float"""

    return [val async for val in async_generator()]
