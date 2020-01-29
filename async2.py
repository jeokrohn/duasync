# -*- coding: utf-8 -*-
"""
2nd asyncio example
from: https://asyncio.readthedocs.io/en/latest/hello_world.html
"""
import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


async def stop_after(loop, when):
    await asyncio.sleep(when)
    loop.stop()


loop = asyncio.get_event_loop()

# creating four tasks. One tasks stops the loop after three seconds
# .. before all other tasks can finish
# --> a warning is created
# Task was destroyed but it is pending!
# task: <Task pending coro=<say() done, defined at /<..>/async2.py:8> wait_for=<Future pending cb=[
# <TaskWakeupMethWrapper object at 0x10b39c610>()]>>
loop.create_task(say('first hello', 2))
loop.create_task(say('second hello', 1))
loop.create_task(say('third hello', 4))
loop.create_task(stop_after(loop, 3))

loop.run_forever()
loop.close()
