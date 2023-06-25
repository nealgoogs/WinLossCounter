import requests

from constants import SUMMMONER_BY_NAME_URL, MATCH_HISTORY_URL, MATCH_DETAILS_URL

def main():
    summoner_name = "bronze draven gg"
    response = requests.get(SUMMMONER_BY_NAME_URL.format(summoner_name))

    if response.status_code == 200:
        data = response.json()
        puu_id = data["puuid"]

        match_history_response = requests.get(MATCH_HISTORY_URL.format(puu_id))

        if match_history_response.status_code == 200:
            print(match_history_response.json())

main()


