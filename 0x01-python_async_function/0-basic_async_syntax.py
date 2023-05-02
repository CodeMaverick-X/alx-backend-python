#!/usr/bin/env python3
"""
an asynchronous coroutine that takes in an int
and returns teh val and waits.
"""

import asyncio
import random
from typing import Union


async def wait_random(max_delay: int = 10) -> Union[int, float]:
    """wait with async function
    return the random num aftr waiting
    """
    r = random.uniform(0, max_delay)
    await asyncio.sleep(1)

    return r
