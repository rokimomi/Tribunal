__author__ = 'amine'

# creates wordcloud from tribunal data

import json
import time

json_data = open('./json/data-10.json')

data = json.load(json_data)

word_cloud = {}
word_cloud_reported = {}

for case in data["tribunal"]:

    for game in case["recentGames"]:

        if not len(game["chatLog"]) > 0:
            continue

        line = game["chatLog"].split(';@@@;')

        for l in line:

            player_type = l.split(";@;")[1]

            words = l.split(";@;")[3].split(" ")

            # general
            for w in words:

                if not len(w) > 0:
                    continue

                if w not in word_cloud:
                    word_cloud[w] = 1
                else:
                    word_cloud[w] += 1

                if player_type == 'reported-player':

                    if w not in word_cloud_reported:
                        word_cloud_reported[w] = 1
                    else:
                        word_cloud_reported[w] += 1

# save data
with open('./json/word-cloud-10.txt', 'w') as outfile:

    for w in sorted(word_cloud, key=word_cloud.get, reverse=True):
        try:
            outfile.write(w +":"+ str(word_cloud[w]) + "\n")
        except UnicodeError, e:
            print w +":"+ str(word_cloud[w])
            print "unicode error here, continuing"

with open('./json/word-cloud-reported-10.txt', 'w') as outfile:

    for w in sorted(word_cloud_reported, key=word_cloud_reported.get, reverse=True):
        try:
            outfile.write(w +":"+ str(word_cloud_reported[w]) + "\n")
        except UnicodeError, e:
            print w +":"+ str(word_cloud_reported[w])
            print "unicode error here, continuing"

json_data.close()