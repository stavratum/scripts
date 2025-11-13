# Steam API key
# https://steamcommunity.com/dev/apikey
key = ""

# SteamID
# https://steamid.pro/lookup
steamid = "76561198845412957"

#
# 
#

import requests
import json
import time
import os

player_summaries_endpoint = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}"
player_data               = {}

#
#
#

# TODO: better logging
def badappend(line: str):
    with open("player_history.txt", 'a') as player_history_fd:
        player_history_fd.write(
            time.strftime(
                f"%Y-%m-%d %H:%M:%S: {line}\n",
                time.localtime()
            )
        )

if os.path.exists("player_data.txt"):
    with open("player_data.txt", 'r') as fd:
        player_data = json.loads(
            fd.read()
        )

while True:
    player_summaries = requests.get(player_summaries_endpoint).json()

    for key, v in player_summaries["response"]["players"][0].items():
        if player_data.get(key) != v:
            player_data[key] = v

            match key:
                case "avatarhash":
                    badappend(f"a nice new avatar: {v}")
                case "avatar":
                    pass
                case "avatarmedium":
                    pass
                case "avatarfull":
                    avatar        = requests.get(v).content
                    avatar_path   = f"avatars/{ int(time.time()) }.jpg"

                    with open(avatar_path, 'wb') as fd:
                        fd.write(avatar)

                    badappend(f"saved the avatar to {avatar_path}")
                case _:
                    badappend(f"{key} = {v}")

            # update the fallback file
            with open("player_data.txt", 'w') as fd:
                fd.write(
                    json.dumps(player_data)
                )

    
    # requesting summaries every 1-5 minutes ensures a nice update rate.
    # i believe 1 minute is the best. maybe this is all just placebo,
    # but it gave me a good guess of someones timezone or EVEN sleeping schedule
    time.sleep(300)

    # TODO: add clans and friend list updates (well i cant sleep until this is DOOONEEEE theyre in my HEAD theyre in my SOUL)
    # why does steam show somebody online then offline a lot? is this when ur on phone or wat

# is this unnecessary
player_history_fd.close()