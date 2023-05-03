#!/usr/bin/env python3
"""
contains a coroutine called `async_generator`
that will loop 10 times async.. wait 1 sec
and then yield a random number between 0 and 10
"""
import random
from typing import Generator
import asyncio


async def async_generator() -> Generator[float, None, None]:
    """yields an int"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
