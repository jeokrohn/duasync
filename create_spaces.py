import webexteamssdk
import random
import uuid
import testusers

with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()

SPACES_TO_CREATE = 5
RANDOM_PEOPLE_IN_SPACE = 10


def create_spaces():
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)
    me = api.people.me()

    people = list(testusers.testusers())

    for space in range(SPACES_TO_CREATE):
        space_title = f'Test space {uuid.uuid4()}'

        random.shuffle(people)
        people_to_add_to_space = people[:RANDOM_PEOPLE_IN_SPACE]
        people_to_add_to_space.insert(0, testusers.TestUser('Johannes', 'Krohn', 'jkrohn@cisco.com'))

        space = api.rooms.create(title=space_title)
        print(f'Created space {space_title}')
        for user in people_to_add_to_space:
            api.memberships.create(roomId=space.id, personEmail=user.email)
            print(f'Added {user} to space {space_title}')


if __name__ == '__main__':
    create_spaces()
