def get_api_key():
    with open(r"C:\Users\thene\OneDrive\Desktop\config.txt") as config_file:
        for line in config_file:
            key, value = line.strip().split('=')
            if key == 'RIOT_API_KEY':
                return value
    return ''

RIOT_API_KEY = get_api_key()

SUMMMONER_BY_NAME_URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key=" + RIOT_API_KEY
MATCH_HISTORY_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start=0&count=20&api_key=" + RIOT_API_KEY
MATCH_DETAILS_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/{}?api_key=" + RIOT_API_KEY