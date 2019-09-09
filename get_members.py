import webexteamssdk
import itertools
import datetime
import concurrent.futures
import tqdm
import asyncio
import aiohttp

SPACES = 200 # number of spaces to work on
MAX_WORKER = 10

# the file 'access token' should contain an access token (for example obtained from developer.webex.com)
with open('access_token', 'r') as f:
    ACCESS_TOKEN = f.readline().strip()


def get_memberships(api, spaces):
    """
    Get memberships for all spaces by calling the respective API one by one
    :param spaces: list of spaces
    :return: tuple list of list of memberhips, seconds
    """
    start = datetime.datetime.utcnow()
    result = list(
        tqdm.tqdm(
            (list(api.memberships.list(roomId=space.id)) for space in spaces),
            total=len(spaces)))
    diff = datetime.datetime.utcnow() - start
    seconds = diff.total_seconds()
    return result, seconds


def get_memberships_concurrent(api, spaces):
    """
    Get memberships for all spaces by calling the respective API in multiple threass
    :param spaces: list of spaces
    :return: tuple list of list of memberhips, seconds
    """
    start = datetime.datetime.utcnow()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        # create a dictionary mapping futures to the space id for all spaces and schedule tasks on the fly
        # each call to executor.submit() schedules a task and returns a future for that task
        future_to_space_id = {executor.submit(lambda: list(api.memberships.list(roomId=space.id))): space.id for space
                              in spaces}
        result = {}
        # then iterate through the futures as they become done
        # not necessarily in the same order as they were submitted
        # as_completed() is only used to be able to get an interator which can be passed to tqdm to get a progress bar
        # else a simple executor.map() could be used to schedule all tasks and wait for all results
        for future_done in tqdm.tqdm(concurrent.futures.as_completed(future_to_space_id), total=len(spaces)):
            # store the results of the future in a dictionary mapping from space id to results
            result[future_to_space_id[future_done]] = future_done.result()
    # finally create list of results in the order of the spaces.
    result = [result[space.id] for space in spaces]
    diff = datetime.datetime.utcnow() - start
    seconds = diff.total_seconds()
    return result, seconds


async def get_membership(space_id, throttle):
    """
    Get membership list for a given space
    :param space_id: ID of space to obtain membership list for
    :param throttle: throttling semaphore
    :return: tuple space id, membership list
    """
    url = 'https://api.ciscospark.com/v1/memberships'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    params = {'roomId': space_id}
    try:
        await throttle.acquire()
        async with aiohttp.request('GET', url, headers=headers, params=params) as resp:
            resp.raise_for_status()
            result = await resp.json()
    finally:
        throttle.release()
    memberships = [webexteamssdk.Membership(i) for i in result['items']]
    return space_id, memberships


async def get_memberships_asyncio(spaces):
    """
    Get memberships for all spaces by calling the respective API in multiple threass
    :param spaces: list of spaces
    :return: tuple list of list of memberhips, seconds
    """
    throttle = asyncio.Semaphore(MAX_WORKER)

    start = datetime.datetime.utcnow()
    # create list of tasks
    tasks = [get_membership(space.id, throttle) for space in spaces]
    result = {}
    # then iterate through the futures as they become done
    # not necessarily in the same order as they were submitted
    # as_completed() is only used to be able to get an interator which can be passed to tqdm to get a progress bar
    # else a simple asyncio.gather() could be used to schedule all tasks and wait for all results
    for future_done in tqdm.tqdm(asyncio.as_completed(tasks), total=len(spaces)):
        space_id, memberships = await future_done
        result[space_id] = memberships
    # finally create list of results in the order of the spaces.
    result = [result[space.id] for space in spaces]
    diff = datetime.datetime.utcnow() - start
    seconds = diff.total_seconds()
    return result, seconds


def main():
    api = webexteamssdk.WebexTeamsAPI(access_token=ACCESS_TOKEN)
    # take 1st few spaces
    print(f'Getting first {SPACES} spaces...')
    spaces = list(itertools.islice(api.rooms.list(max=100), SPACES))
    print(f'Got first {SPACES} spaces...')
    _, seconds = get_memberships(api, spaces)

    _, seconds_concurrent = get_memberships_concurrent(api, spaces)

    _, seconds_asncio = asyncio.run(get_memberships_asyncio(spaces))

    print(f'get_memberships() took {seconds} seconds')
    print(f'get_memberships_concurrent() took {seconds_concurrent} seconds')
    print(f'get_memberships_asyncio() took {seconds_asncio} seconds')


if __name__ == '__main__':
    main()
