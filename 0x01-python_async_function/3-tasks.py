#!/usr/bin/env python3
"""
contains function task_wait_random
that returns AN async task
"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """returns a task in async"""
    task = asyncio.create_task(wait_random(max_delay))

    return task
