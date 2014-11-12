__author__ = 'amine'

import json
import math
from pprint import pprint

# basic stats questions, answer by combing through json

###

# average length of games?

# what's the kda of reported players?

# what percent of reported players cuss?

# what's the message rate of the reported player compared to the rest of the game?

# average games of times below 21 minutes (20 mins is minimum for surrendering, allow one minute for surrendering)

# how many dominion games are in this dataset?

# are the dominion versions of the above different at all?

####

# todo what about hours encoding
def time_to_seconds(time):
    hms = time.split(':')

    if(len(hms) == 3):
        print 'HOURS'
    elif(len(hms) == 2):
        print 'ONLY MINS'

def seconds_to_time(seconds):
    print 'HERE YA GO'

def percent(numerator, denominator):
    return "%.4f" % (numerator / float(denominator) * 100)

def summary(tribunal_dict):
    for d in tribunal_dict:
        count = tribunal_dict[d]
        print d + ': ' + str(count) + '/' + str(total) + ' (' + (percent(count,total)) + '%)'

json_data = open('./json/data-10.json')

data = json.load(json_data)

#pprint(data) # pretty print??

total = len(data["tribunal"])

winCount = 0
lossCount = 0

total_time = 0;

decisionCounts = {}
agreementCounts = {}
punishmentCounts = {}

for case in data["tribunal"]:

    decision = case["decision"]
    agreement = case["agreement"]
    punishment = case["punishment"]

    if decision not in decisionCounts:
        decisionCounts[decision] = 1
    else:
        decisionCounts[decision] += 1

    if agreement not in agreementCounts:
        agreementCounts[agreement] = 1
    else:
        agreementCounts[agreement] += 1

    if punishment not in punishmentCounts:
        punishmentCounts[punishment] = 1
    else:
        punishmentCounts[punishment] += 1

    for game in case["recentGames"]:
        if game["outcome"] == "Win":
            winCount += 1
        elif game["outcome"] == "Loss":
            lossCount += 1

        total_time = time_to_seconds(game["gameLength"])

total_games = winCount+lossCount

print str(total) + 'tribunal cases total'
print str(total_games) + " games total \n"
#todo print 'Average game time' + str((total_time / float(total_games)))

print '\nDecisions Summary --'
summary(decisionCounts)

print '\nAgreements Summary --'
summary(agreementCounts)

print '\nPunishments Summary --'
summary(punishmentCounts)

print "\n\nWin rate of reported players: " + str(winCount) + "/" + str(winCount + lossCount) + " (" + (percent(winCount, lossCount + winCount)) + "%)"

json_data.close()

time_to_seconds("22:01:33")
