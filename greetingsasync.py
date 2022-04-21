''' Written by Anton Caceres
    https://github.com/MA3STR0/PythonAsyncWorkshop

    Functions:
        task
        request_greetings

    Author: Juraj Lapčák
    Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''


import time
import asyncio
import aiohttp

__author__ = 'Juraj Lapčák, Matúš Jokay'

URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]


async def task(responses, work_queue):
    '''
    Async run of task of requesting a URL path.

    Parameters:
        responses - list where to append request response
        work_queue - queue of tasks

    Returns:
        None
    '''
    if work_queue.empty():
        return

    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            async with session.get(url) as response:
                responses.append(await response.text())


async def request_greetings():
    '''
    Parameters:
        None

    Returns:
        None
    '''

    work_queue = asyncio.Queue()

    responses = []
    for url in URLS:
        await work_queue.put(url)

    tasks = [task(responses, work_queue), task(responses, work_queue)]
    await asyncio.gather(*tasks)
    texts = '\n'.join(responses)
    return texts


if __name__ == "__main__":
    t1 = time.time()
    greetings = asyncio.run(request_greetings())
    print(time.time() - t1, "seconds passed")
    print(greetings)
