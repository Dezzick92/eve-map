"""
First version of the EVE Universe scraper - naive version that does everything sequentially and takes a while to do it.
Systems code is commented out as it is estimated to take about 30 minutes and nobody wants that.

"""

from lxml import html
import time
import json
import requests
from progress.bar import Bar

regions = {}
constellations = {}
systems = {}


timing = True
logging = False

time_start = time.perf_counter()
print(" ")
print("---------------")
print("loading regions")
print("---------------")
print(" ")

try:
    t_0 = time.perf_counter()
    page = requests.get('https://esi.evetech.net/latest/universe/regions/?datasource=tranquility')
    info = json.loads(page.content)
    t_1 = time.perf_counter()
except:
    print("Failed to load regions from ESI - quitting")
    quit()

for i in info:
    regions[str(i)] = {}
    t_2 = time.perf_counter()
if timing: print("Time to get region request:",t_1-t_0)
if timing: print("Time to do data stuff:",t_2-t_1)

regionbar = Bar('Downloading Regions', max = len(regions))
for region in regions:
    if logging: print("loading region " + region)
    try:
        page = requests.get('https://esi.evetech.net/latest/universe/regions/' + region + '/?datasource=tranquility')
        info = json.loads(page.content)
    except:
        print("Failed to load region " + region + " data from ESI - quitting")
        quit()
    
    if logging: print("region " + region +" loaded")
    regions[region] = info
    if logging: print("region " + region + " updated as " + regions[region]["name"])
    regionbar.next()

print(" ")
print("---------------")
print("regions downloaded!")
time_regions = time.perf_counter()


with open("regions.txt","w") as regionsfile:
    regionsfile.write(json.dumps(regions))
    regionsfile.close

print("regions saved!")
print("---------------")
print(" ")


print(" ")
print("---------------")
print("loading constellations")
print("---------------")
print(" ")

try:
    t_0 = time.perf_counter()
    page = requests.get('https://esi.evetech.net/latest/universe/constellations/?datasource=tranquility')
    info = json.loads(page.content)
    t_1 = time.perf_counter()
except:
    print("Failed to load constellations from ESI - quitting")
    quit()

for i in info:
    constellations[str(i)] = {}
    t_2 = time.perf_counter()
if timing: print("Time to get constellations request:",t_1-t_0)
if timing: print("Time to do data stuff:",t_2-t_1)

constellationbar = Bar('Downloading Constellations', max = len(constellations))
for constellation in constellations:
    if logging: print("loading constellations " + constellation)
    try:
        page = requests.get('https://esi.evetech.net/latest/universe/constellations/' + constellation + '/?datasource=tranquility')
        info = json.loads(page.content)
    except:
        print("Failed to load constellation " + constellation + " data from ESI - quitting")
        quit()
    
    if logging: print("constellation " + constellation +" loaded")
    constellations[constellation] = info
    if logging: print("constellation " + constellation + " updated as " + constellations[constellation]["name"])
    constellationbar.next()

print(" ")
print("---------------")
print("constellations loaded!")

with open("constellations.txt","w") as constellationsfile:
    constellationsfile.write(json.dumps(constellations))
    constellationsfile.close

print("constellations saved!")
print("---------------")
print(" ")

# print(" ")
# print("---------------")
# print("loading systems")
# print("---------------")
# print(" ")

# try:
#     t_0 = time.perf_counter()
#     page = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
#     info = json.loads(page.content)
#     t_1 = time.perf_counter()
# except:
#     print("Failed to load systems from ESI - quitting")
#     quit()

# for i in info:
#     systems[str(i)] = {}
#     t_2 = time.perf_counter()
# if timing: print("Time to get system request:",t_1-t_0)
# if timing: print("Time to do data stuff:",t_2-t_1)

# for system in systems:
#     if logging: print("loading system " + system)
#     try:
#         page = requests.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility')
#         info = json.loads(page.content)
#     except:
#         print("Failed to load system " + system + " data from ESI - quitting")
#         quit()
    
#     if logging: print("system " + system +" loaded")
#     systems[system] = info
#     if logging: print("system " + system + " updated as " + systems[system]["name"])

# print(" ")
# print("---------------")
# print("systems loaded!")
# print("---------------")
# print(" ")


# with open("systems.txt","w") as systemsfile:
#     systemsfile.write(json.dumps(systems))
#     systemsfile.close


print("done")