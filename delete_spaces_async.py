# -*- coding: utf-8 -*-

"""
Delete test spaces created by create_spaces.py or create_spaces_async.py; using asyncio

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!Caution!!!
This script deletes all spaces with titles starting wtih "Test space "
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""

import webexteamssdk
import asyncio
import aiohttp

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()


async def delete_space(id, title):
    url = f'https://api.ciscospark.com/v1/rooms/{id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as r:
            r.raise_for_status()
            print(f'space "{title}" deleted')


async def delete_spaces(loop):
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)

    # get all existing test spaces
    spaces = [s for s in api.rooms.list() if s.title.startswith('Test space ')]

    print('Start deleting spaces...')
    tasks = [delete_space(space.id, space.title) for space in spaces]

    r = await asyncio.gather(*tasks, loop=loop, return_exceptions=True)
    failed_spaces = [(s, r) for s, r in zip(spaces, r) if isinstance(r, Exception)]
    for s, r in failed_spaces:
        print(f'Deleting space "{s.title}" failed: {r}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_spaces(loop))
