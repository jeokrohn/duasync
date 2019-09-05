# -*- coding: utf-8 -*-
"""
Create some testusers. This requires sufficient scopes of the access token; serial
"""

import webexteamssdk
import testusers

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()

def provision_users():
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)

    messaging_license = next((l for l in api.licenses.list() if l.name == 'Messaging'), None)
    assert messaging_license is not None

    print('Start adding users...')
    for user in testusers.testusers():
        try:
            api.people.create(emails=[user.email], displayName=user.display_name, firstName=user.first, lastName=user.last,
                              licenses=[messaging_license.id])
        except Exception as e:
            print(f'Provsisioning of {user} failed: {e}')
        else:
            print(f'Provsisioning of {user} done')


if __name__ == '__main__':
    provision_users()
