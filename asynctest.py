from ast import Num
from asyncio.tasks import wait
import httpx
import asyncio
import json
import random

def rand_code(odds = 0.5):
    """
    Returns a url that will respond with either code 200 or code 502.
    Odds are favoured towards 502, so if odds = 0.8, there will be a 0.8 chance of error 502.
    If odds input > 1, it will use 1/odds -- if you input 4, the odds will be 1/4
    
    """
    if odds > 1: odds = 1/odds

    if random.random() > odds:
        print("200")
        return 'https://httpstat.us/200'
    else:
        print("502")
        return 'https://httpstat.us/502'

async def main():

    random.seed(100)

    async with httpx.AsyncClient() as client:
        i = 0
        while i > -1:
            response = {}
            response = await client.get(url = rand_code(4), headers={'Accept' : 'application/json'})
            if response.status_code == 200:
                info = json.loads(response.content)
                i = -1
            elif i < 5:
                await asyncio.sleep( (2**i) / 2 )
                response.status_code = 0
                i += 1
            else:
                raise Exception("Failed to get valid response after " + str(i+1) + " attempts")
        print(info)
        return info


    

asyncio.run(main())

