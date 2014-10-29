import struct
print struct.calcsize("P") * 8

import json

# json tests

data = {"tribunal":[]}


data["tribunal"].append({"b":0})
data["tribunal"].append({"b":7})

with open('./json/data.json', 'w') as outfile:
  json.dump(data, outfile)
