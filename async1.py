# -*- coding: utf-8 -*-
"""
Trivial asyncio example
from: https://asyncio.readthedocs.io/en/latest/hello_world.html
"""
import asyncio

async def say(what, when):
    await asyncio.sleep(when)
    print(what)


loop = asyncio.get_event_loop()

# creating a few tasks and then run the loop
# the code never terminates; the loop runs forever
loop.create_task(say('first hello', 4))
loop.create_task(say('second hello', 3))
loop.create_task(say('third hello', 2))
loop.create_task(say('fourth hello', 1))

loop.run_forever()
loop.close()