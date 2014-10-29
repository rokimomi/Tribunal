__author__ = 'amine'

import json
from pprint import pprint

# basic stats questions, answer by combing through json

###

# how many reported players are punished, how many pardoned

# what's the win rate of reported players

# what's the kda of reported players

# what percent of reported players cuss

# what's the message rate of the reported player compared to the rest of the game?

####


json_data = open('./json/data.json')

data = json.load(json_data)

#pprint(data) # pretty print??

total = len(data["tribunal"])

pardonCount = 0
punishCount = 0

winCount = 0
lossCount = 0

for case in data["tribunal"]:
    if case["decision"] == "Pardon":
        pardonCount += 1
    elif case["decision"] == "Punish":
        punishCount += 1

    for game in case["recentGames"]:
        if game["outcome"] == "Win":
            winCount += 1
        elif game["outcome"] == "Loss":
            lossCount += 1

print str(total) + " tribunal cases total"
print str(winCount+lossCount) + " games total \n"

print str(pardonCount) + "/" + str(total) + " Players pardoned (" + str(pardonCount/float(total)*100) + "%)"
print str(punishCount) + "/" + str(total) + " Players punished (" + str(punishCount/float(total)*100) + "%)"

print "Win rate of reported players: " + str(winCount) + "/" + str(winCount + lossCount) + " (" + str(winCount/float(lossCount + winCount)*100) + "%)"

json_data.close()
