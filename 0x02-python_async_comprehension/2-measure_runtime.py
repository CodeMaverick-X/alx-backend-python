#!/usr/bin/env python3
"""
contains a `measure_runtime` coroutine
that will execute the `async_comprehension`
four times in parrallel using asyncio.gather
"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure time of execution"""
    start = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end = time.perf_counter() - start
    return end
