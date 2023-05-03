#!/usr/bin/env python3
"""contains func task_wait_n that
calls task creattion"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ create task that
    returns list of float
    """
    res = await asyncio.gather(*(task_wait_random(max_delay)
                                     for _ in range(n)))
    return res
