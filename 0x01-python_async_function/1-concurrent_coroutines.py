#!/usr/bin/env python3
"""
contains a routine wait_ n that
takes in 2 in arg n and max_delay
and spawns wait_random n times
"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """returns list of floats"""
    res = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))

    return sorted(res)
