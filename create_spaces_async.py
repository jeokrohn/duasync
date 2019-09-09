# -*- coding: utf-8 -*-
"""
Creating some random test spaces with random members; using asyncio
"""
import webexteamssdk
import asyncio
import aiohttp
import random
import uuid
import testusers

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()

SPACES_TO_CREATE = 5  # Number of spaces to create
RANDOM_PEOPLE_IN_SPACE = 10  # number of random people in each space


async def create_membership(room_id, title, user):
    url = 'https://api.ciscospark.com/v1/memberships'
    params = {'roomId': room_id,
              'personEmail': user.email}
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params, headers=headers) as r:
            try:
                r.raise_for_status()
            except Exception as e:
                print(f'Adding {user} to space "{title}" failed: {e}')
                raise
            else:
                print(f'{user} added to space {title}')


async def create_space(api, title, users):
    url = 'https://api.ciscospark.com/v1/rooms'
    params = {'title': title}
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params, headers=headers) as r:
            r.raise_for_status()
            space_json = await r.json()
            print(f'Space "{title}" created')

            space = webexteamssdk.Room(space_json)
            tasks = [create_membership(space.id, title, user) for user in users]
            r = await asyncio.gather(*tasks)


async def create_spaces():
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)

    me = api.people.me()

    people = list(testusers.testusers())

    tasks = []
    for space in range(SPACES_TO_CREATE):
        space_title = f'Test space {uuid.uuid4()}'

        random.shuffle(people)
        people_to_add_to_space = people[:RANDOM_PEOPLE_IN_SPACE]
        people_to_add_to_space.insert(0, testusers.TestUser('Johannes', 'Krohn', 'jkrohn@cisco.com'))

        tasks.append(create_space(api, space_title, people_to_add_to_space))
    r = await asyncio.gather(*tasks, return_exceptions=False)


if __name__ == '__main__':
    asyncio.run(create_spaces())
