__author__ = 'amine'

# turn html cases into one big json file

from bs4 import BeautifulSoup as bs
import re
import json
import glob

# 6030355 SHOWS A "DID NOT LOAD CORRECTLY" MESSAGE FOR GAMES 2 and 3

data = {"tribunal":[]}

##

files_list = glob.glob('./cases/*.html')

for file in files_list:

    print file[8:]

    # open case file
    case_file = file
    html = open(case_file, "r")
    soup = bs(html)

    try:

        caseNum = soup.find_all("span", class_=re.compile('raw-case-number'))[0].contents[0]

        reports = soup.find_all("span", class_=re.compile('total-reports-fill'))[0].contents[0]
        games = soup.find_all("span", class_=re.compile('total-games-fill'))[0].contents[0]
        decision = soup.find_all("p", class_=re.compile('verdict-stat'))[2].contents[0]
        agreement = soup.find_all("p", class_=re.compile('agreement'))[0].contents[0]
        punishment = soup.find_all("p", class_=re.compile('verdict-stat'))[0].contents[0]

        ####

        games_div = soup.find_all("div", class_=re.compile('tab-content-container'))[0]

        recentGames = []

        # cycle through the games this player was reported in

        for i in range(1, int(games)+1):

            game = games_div.find_all("div", id=re.compile('game'+str(i)))[0]

            # basic game metadata
            gameType = game.find_all("p", id=re.compile('stat-type-fill'))[0].contents[0]
            gameLength = game.find_all("p", id=re.compile('stat-length-fill'))[0].contents[0]
            outcome = game.find_all("p", id=re.compile('stat-outcome-fill'))[0].contents[0]

            recentGames.append({"gameType": gameType, "gameLength": gameLength, "outcome": outcome})

        # create case
        case = {"caseNum": caseNum, "reports": reports, "games": games, "decision": decision, "agreement": agreement, "punishment": punishment, "recentGames": recentGames}

        # add this case to larger json
        data["tribunal"].append(case)

    except IndexError:
        print "IndexError: case " + caseNum + ". Throwing case out..."

# save data
with open('./json/data.json', 'w') as outfile:
    json.dump(data, outfile)

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