"""
Second version of the EVE Universe scraper - using asyncio to do things faster - almost 6x faster!

"""

import httpx
import asyncio
import time
import json
from progress.bar import Bar

constellations = {}
systems = {}


timing = True
logging = True

async def gather_with_concurrency(n,bar, *tasks):
    """
    Stolen from Andrei's answer here:
    https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio

    Elegant little utility function
    """
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task,bar):
        async with semaphore:
            bar.next()
            return await task
    return await asyncio.gather(*(sem_task(task,bar) for task in tasks))

async def get_limited(url : str, n : int = 5):
    async with httpx.AsyncClient() as client:
        n -= 1 # this limits it to the requested number of requests
        i = 0
        while i > -1:
            response = {}
            response = await client.get(url)
            if response.status_code == 200:
                i = -1
            elif i < n:
                await asyncio.sleep( (2**i) / 2 )
                if logging: print("URL " + url +" produced code" + str(response.status_code))
                i += 1
            else:
                raise Exception("\nFailed to get valid response after " + str(i+1) + " attempts")
        return response


async def get_info(context,thing):
    async with httpx.AsyncClient() as client:
        response = await get_limited(url = 'https://esi.evetech.net/latest/universe/'+ context + '/' + str(thing) + '/?datasource=tranquility')
        info = json.loads(response.content)
    return info

async def get_all_info(context):
    things = []
    async with httpx.AsyncClient() as client:
        response = await get_limited(url = 'https://esi.evetech.net/latest/universe/'+ context +'/?datasource=tranquility')
        things = (json.loads(response.content))
    with Bar('reticulating splines', max = len(things)) as bar:
        completed = await gather_with_concurrency(50,bar,*[get_info(context, thing) for thing in things])
    return completed

async def main():
    t_start = time.perf_counter()
    regions = await get_all_info('regions')
    t_region = time.perf_counter()
    if timing: print(t_region - t_start)

    # convert from list of region info to dict with id as key

    with open("regions.txt","w") as regionsfile:
        regionsfile.write(json.dumps(regions))
        regionsfile.close
    print("Regions saved!")

    constellations = await get_all_info('constellations')
    t_constellation = time.perf_counter()
    if timing: print(t_constellation - t_region)
    
    # convert from list of const info to dict with id as key

    with open("constellations.txt","w") as constellationsfile:
        constellationsfile.write(json.dumps(constellations))
        constellationsfile.close
    print("Constellations saved!")

    systems = await get_all_info('systems')
    t_system = time.perf_counter()
    if timing: print(t_system - t_constellation)
    
    # convert from list of system info to dict with id as key

    with open("systems.txt","w") as systemsfile:
        systemsfile.write(json.dumps(systems))
        systemsfile.close
    print("Systems saved!")

    t_end = time.perf_counter()
    if timing: print(t_end - t_start)



asyncio.run(main())




print("done")