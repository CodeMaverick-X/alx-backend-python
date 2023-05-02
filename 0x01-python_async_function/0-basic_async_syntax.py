#!/usr/bin/env python3
"""
an asynchronous coroutine that takes in an int
arg max_delay with default value 10, named
wait_random that waits for a random delay betwen 0
and max_delay(included float value) seconds and
eventually returns it.
uses `random` module
"""

import asyncio
import random
from typing import Union


async def wait_random(max_delay: int = 10) -> Union[int, float]:
    """wait with async function
    return the random number after
    waiting
    """
    r = random.uniform(0, max_delay)
    await asyncio.sleep(r)

    return r
