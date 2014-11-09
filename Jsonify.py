__author__ = 'amine'

# turn html cases into one big json file

from bs4 import BeautifulSoup as bs
import re
import json
import glob
import gc
import sys

from pympler import muppy
from pympler import summary

all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)
summary.print_(sum1)


# 6030355 SHOWS A "DID NOT LOAD CORRECTLY" MESSAGE FOR GAMES 2 and 3

data = {"tribunal":[]}

##

files_list = glob.glob('./cases/*.html')

num_files = len(files_list)
current_file_num = 0
num_files_thrown = 0


# !!! DELETE LATER
#num_files = 500


for file in files_list:

    #if current_file_num == num_files:
    #    break

    if current_file_num % 1000 == 0:
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)
        summary.print_(sum1)

    current_file_num += 1

    print str(current_file_num) + ' / ' + str(num_files) + ' (%.2f' % (current_file_num/float(num_files)*100) + '%)'

    print file[8:]

    # open case file
    case_file = file
    html = open(case_file, "r")

    try:

        soup = bs(html)

        caseNum = soup.find_all("span", class_=re.compile('raw-case-number'))[0].contents[0].extract()

        reports = soup.find_all("span", class_=re.compile('total-reports-fill'))[0].contents[0].extract()
        games = soup.find_all("span", class_=re.compile('total-games-fill'))[0].contents[0].extract()
        decision = soup.find_all("p", class_=re.compile('verdict-stat'))[2].contents[0].extract()
        agreement = soup.find_all("p", class_=re.compile('agreement'))[0].contents[0].extract()
        punishment = soup.find_all("p", class_=re.compile('verdict-stat'))[0].contents[0].extract()


        ####

        games_div = soup.find_all("div", class_=re.compile('tab-content-container'))[0].extract()

        recentGames = []

        # cycle through the games this player was reported in



        for i in range(1, int(games)+1):

            game = games_div.find_all("div", id=re.compile('game'+str(i)))[0].extract()

            # basic game metadata
            gameType = game.find_all("p", id=re.compile('stat-type-fill'))[0].contents[0].extract()
            gameLength = game.find_all("p", id=re.compile('stat-length-fill'))[0].contents[0].extract()
            outcome = game.find_all("p", id=re.compile('stat-outcome-fill'))[0].contents[0].extract()

            recentGames.append({"gameType": gameType, "gameLength": gameLength, "outcome": outcome})

        # create case
        case = {"caseNum": caseNum, "reports": reports, "games": games, "decision": decision, "agreement": agreement, "punishment": punishment, "recentGames": recentGames}

        # add this case to larger json
        data["tribunal"].append(case)

        soup.decompose()

        gc.collect()

        html.close()



    except IndexError, e:
        print "IndexError: case " + caseNum + ". Throwing case out..."
        num_files_thrown += 1
        soup.decompose()
        gc.collect()
    except UnicodeDecodeError, e:
        print "UnicodeDecodeError: case " + caseNum + ". Throwing case out..."
        num_files_thrown += 1
        soup.decompose()
        gc.collect()

# save data
with open('./json/data.json', 'w') as outfile:
    json.dump(data, outfile)

print 'Processed ' + str(num_files) + ' total cases.'
print str(num_files_thrown) + ' cases thrown out ('+ str((num_files_thrown/float(num_files)*100)) +'%)'
print str(num_files - num_files_thrown) + ' remaining (' + str(((num_files-num_files_thrown)/float(num_files)*100)) + '%)'

"""
http://www.jsoneditoronline.org/

{
  "tribunal":[

    {
      "caseNum": 1234,
      "reports": 3,
      "games": 5,
      "decision": "something",
      "agreement": "majority",
      "punishment": "warning",
      "recentGames":[
        {
          "gameType": "summoner's rift",
          "gameLength": "35:15",
          "outcome": "win",
          "reportComments": [

            {
              "reportedBy": "b",
              "comment": "b"
            },
            {
              "reportedBy": "b",
              "comment": "b"
            }

          ],
          "chatLog": "aflskfjalskfjlaksjf",
          "players": {
            "character": "b",
            "summoner1": "b",
            "summoner2": "b",
            "level": "b",
            "kda": "b",
            "gold": "b",
            "cs": "b"
          }
        }
      ]
    }

  ]
}"""

"""

caseNum // case id
reports // how many reports in this case across all games
games // how many games in this case
Decision // final decision
agreement // how collective was the agreement
punishment // what punishment was decreed

recentGames

    gameid // game id (1-5 typically)
    game type // classic tree, etc
    game length
    outcome // win/loss

    ReportComments
        ReportedBy // ally/enemy
        comment // written report comment if any

    ChatLog // full table of chat log FOR NOW, later turn it into json as well, so no need for table parsing

    Players // just for reported character FOR NOW
        character // char they were playing
        summoner 1 // summoners skill 1
        summoner 2 // "             " 2
        level
        kda
        gold
        cs
"""