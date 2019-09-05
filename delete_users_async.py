# -*- coding: utf-8 -*-
"""
Delete test users; using asyncio
"""

import webexteamssdk
import asyncio
import aiohttp
import testusers

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()


async def delete_user(id, user):
    url = f'https://api.ciscospark.com/v1/people/{id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as r:
            r.raise_for_status()
            print(f'{user} deleted')


async def delete_users(loop):
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)
    me = api.people.me()
    people = [p for p in api.people.list() if p.emails[0] != me.emails[0]]

    # need a mapping from user email to Webex id
    email_to_id = {u.emails[0]: u.id for u in people}

    print('Start deleting users...')
    tasks = []
    users = list(testusers.testusers())
    for user in users:
        # we need the user's Webex id to delete the user
        id = email_to_id.get(user.email)
        if id is None:
            print(f'Failed to determine Webex id for {user}')
            continue
        tasks.append(delete_user(id, user))
    r = await asyncio.gather(*tasks, loop=loop, return_exceptions=True)
    failed_users = [(u, r) for u, r in zip(users, r) if isinstance(r, Exception)]

    for u, r in failed_users:
        print(f'Deleting {u} failed: {r}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_users(loop))
