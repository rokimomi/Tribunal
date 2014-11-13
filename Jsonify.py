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

data = {"tribunal":[]}

##

files_list = glob.glob('./cases/*.html')

num_files = len(files_list)
current_file_num = 0
num_files_thrown = 0

for file in files_list:

    if current_file_num % 1000 == 0:
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)
        summary.print_(sum1)

    #if current_file_num == 50: break

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

            # todo report comments
            # have only ever seen one comment here, run some kind of test to find a page with multiple reports and multiple comments

            # chat
            # instead of saving each line as it's own dictionary element, concatenate the chat lines together and insert
            # as one object to save on processing memory needed

            chat_log = []

            chat = game.find_all("tr", class_=re.compile('alliesFilter|enemiesFilter'))

            for line in chat:

                chat_type = 'ally'
                chat_class_list = line.get('class')
                if 'enemy' in chat_class_list:
                    chat_type = 'enemy'
                elif 'reported-player' in chat_class_list:
                    chat_type = 'reported-player'

                chat_user = line.find_all("td", class_=re.compile('chat-user'))[0].contents[0].extract()
                chat_timestamp = line.find_all("td", class_=re.compile('chat-timestamp'))[0].contents[0].extract()
                chat_message = line.find_all("td", class_=re.compile('chat-message'))[0].contents[0].extract()

                chat_log.append({"user": chat_user, "type":chat_type, "timestamp": chat_timestamp, "message": chat_message})

            full_chat = ''

            for c in chat_log:
                full_chat = full_chat + c['user'] + ';@;' + c['type'] + ';@;' + c['timestamp'] + ';@;' + c['message'] + ';@@@;'

            full_chat = full_chat[:-5]

            chat_log = []

            # player stats
            player_list = []

            player_container = game.find_all("div", class_=re.compile('players-container'))[0].extract()
            players = player_container.find_all("tr", class_=re.compile('reported-player|ally'))

            for p in players:

                player_level = p.find_all("td", class_=re.compile('player-level'))[0].contents[0].extract()
                # todo champion and summoner spells are referenced by image only on a tribunal case (image grabs a
                # todo portion of a tileset
                #player_champion = p.find_all("td", class_=re.compile('player-champion'))[0].contents[0].extract()
                #player_summoners = p.find_all("td", class_=re.compile('player-summoner-spells'))[0].contents[0].extract()
                player_kda = p.find_all("td", class_=re.compile('player-kda'))[0].contents[0].extract()

                # todo gold and cs dont exist in dominion, so this script doesnt grab dominion matches
                player_gold = p.find_all("td", class_=re.compile('player-gold'))[0].contents[0].extract()
                player_cs = p.find_all("td", class_=re.compile('player-creep-score'))[0].contents[0].extract()

                player_type = 'ally'
                if 'reported-player' in p.get('class'):
                    player_type = 'reported-player'

                player_list.append({"level":player_level, "kda": player_kda, "gold": player_gold, "creepScore": player_cs})

            recentGames.append({"gameType": gameType, "gameLength": gameLength, "outcome": outcome, "chatLog": full_chat, "players": player_list})

        # create case
        case = {"caseNum": caseNum, "reports": reports, "games": games, "decision": decision, "agreement": agreement, "punishment": punishment, "recentGames": recentGames}

        # add this case to larger json
        data["tribunal"].append(case)

        # free up some memory
        soup.decompose()
        gc.collect()
        html.close()

    except IndexError, e:
        print "IndexError: case " + caseNum + ". Throwing case out..."
        num_files_thrown += 1
        soup.decompose()
        gc.collect()
        html.close()
    except UnicodeDecodeError, e:
        print "UnicodeDecodeError: case " + caseNum + ". Throwing case out..."
        num_files_thrown += 1
        soup.decompose()
        gc.collect()
        html.close()

# save data
with open('./json/data.json', 'w') as outfile:
    json.dump(data, outfile)

print 'Processed ' + str(num_files) + ' total cases.'
print str(num_files_thrown) + ' cases thrown out ('+ str((num_files_thrown/float(num_files)*100)) +'%)'
print str(num_files - num_files_thrown) + ' remaining (' + str(((num_files-num_files_thrown)/float(num_files)*100)) + '%)'

# todo update these comments on what the structure of the json output looks like

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