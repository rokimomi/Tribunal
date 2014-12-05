__author__ = 'amine'

import json
import time
import datetime
import math
from pprint import pprint

# basic stats questions, answer by combing through json

###

# what's the kda of reported players?

# what percent of reported players cuss?

# what's the message rate of the reported player compared to the rest of the game?

# average games of times below 21 minutes (20 mins is minimum for surrendering, allow one minute for surrendering)

# how many dominion games are in this dataset?

# are the dominion versions of the above different at all?

####

def time_to_seconds(t):
    hms = t.split(':')
    return (int(hms[0]) * 60) + int(hms[1])

def seconds_to_time(seconds):
    if(seconds < 3600):
        return time.strftime('%M:%S', time.gmtime(seconds))
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def percent(numerator, denominator):
    return "%.4f" % (numerator / float(denominator) * 100)

def summary(tribunal_dict):
    for d in tribunal_dict:
        count = tribunal_dict[d]
        print d + ': ' + str(count) + '/' + str(total) + ' (' + (percent(count,total)) + '%)'

json_data = open('./json/data.json')

data = json.load(json_data)

total = len(data["tribunal"])

winCount = 0
lossCount = 0

total_time = 0;
time_sub_20 = 0;

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

    reported_msg_count = 0
    ally_msg_count = 0

    for game in case["recentGames"]:
        if game["outcome"] == "Win":
            winCount += 1
        elif game["outcome"] == "Loss":
            lossCount += 1

        game_time = time_to_seconds(game["gameLength"])

        total_time += game_time

        if game_time < time_to_seconds("20:00"):
            time_sub_20 += 1

        # chat things

        if not len(game["chatLog"]) > 0:
            continue

        line = game["chatLog"].split(';@@@;')

        for l in line:
            player_type = l.split(";@;")[1]
            if player_type == "ally":
                ally_msg_count += 1
            elif player_type == "reported-player":
                reported_msg_count += 1

total_games = winCount+lossCount

print str(total) + ' tribunal cases total'
print str(total_games) + ' games total \n'
print 'Average game time: ' + seconds_to_time((total_time / (total_games)))

print 'Games ending before 20 minutes: ' + str(time_sub_20)

print '\nDecisions Summary --'
summary(decisionCounts)

print '\nAgreements Summary --'
summary(agreementCounts)

print '\nPunishments Summary --'
summary(punishmentCounts)

print "\nWin rate of reported players: " + str(winCount) + "/" + str(winCount + lossCount) + " (" + (percent(winCount, lossCount + winCount)) + "%)"

print "\nReported player chat percentage: (" + str(reported_msg_count) + "/" + str(reported_msg_count+ally_msg_count) + ") (" + percent(reported_msg_count, reported_msg_count + ally_msg_count) + "%)"

json_data.close()