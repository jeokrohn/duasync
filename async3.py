# -*- coding: utf-8 -*-
"""
3rd asyncio example
"""
import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


async def test():
    # schedule parallel execution of three tasks in parallel and wait until all are done
    await asyncio.gather(say('first hello', 2),
                         say('second hello', 1),
                         say('third hello', 4))


# create a single task, schedule execution of that task in an event loop, and then close the loop after task termination
asyncio.run(test())
