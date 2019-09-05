# -*- coding: utf-8 -*-
"""
Create some testusers. This requires sufficient scopes of the access token; using asyncio
"""

import webexteamssdk
import asyncio
import aiohttp
import testusers

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()


async def add_user(emails, displayName, firstName, lastName, licenses):
    url = 'https://api.ciscospark.com/v1/people'
    params = {
        'emails': emails,
        'displayName': displayName,
        'firstName': firstName,
        'lastName': lastName,
        'licenses': licenses
    }
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params, headers=headers) as r:
            if r.status != 200:
                text = await r.text()
                print(f'Failed to provision {displayName}: {r.status}, {text}')
            r.raise_for_status()
            print(f'{displayName} provisioned')


async def provision_users(loop):
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)

    messaging_license = next((l for l in api.licenses.list() if l.name == 'Messaging'), None)
    assert messaging_license is not None

    tasks = []
    print('Start adding users...')
    users = list(testusers.testusers())
    for user in users:
        tasks.append(
            add_user(emails=[user.email], displayName=user.display_name, firstName=user.first, lastName=user.last,
                     licenses=[messaging_license.id]))
    r = await asyncio.gather(*tasks, loop=loop, return_exceptions=True)
    failed_users = [(u, r) for u, r in zip(users, r) if isinstance(r, Exception)]

    for u, r in failed_users:
        print(f'Adding {u} failed: {r}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(provision_users(loop))
