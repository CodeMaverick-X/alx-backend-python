#!/usr/bin/env python3
"""
contains a coroutine wait_ n that
takes in 2 in arg n and max_delay
and spawns wait_random n times
"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """returns list of floats"""
    res = await asyncio.gather(*(task_wait_random(max_delay)
                               for _ in range(n)))

    return sorted(res)
