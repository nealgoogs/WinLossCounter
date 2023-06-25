import requests
import tkinter as tk

from constants import SUMMMONER_BY_NAME_URL, MATCH_HISTORY_URL, MATCH_DETAILS_URL

def get_last_game_kills():
    summoner_name = summoner_entry.get()
    response = requests.get(SUMMMONER_BY_NAME_URL.format(summoner_name))

    if response.status_code == 200:
        summoner_data = response.json()
        puuid = summoner_data["puuid"]

        match_history_response = requests.get(MATCH_HISTORY_URL.format(puuid))

        if match_history_response.status_code == 200:
            match_history_data = match_history_response.json()

            if len(match_history_data) > 0:
                match_id = match_history_data[0]
                match_details_response = requests.get(MATCH_DETAILS_URL.format(match_id))

                if match_details_response.status_code == 200:
                    match_details_data = match_details_response.json()

                    participants = match_details_data["info"]["participants"]
                    participant = next((p for p in participants if p["summonerName"] == summoner_name), None)

                    if participant:
                        kills = participant["kills"]
                        result_label.config(text=f"Kills in the last game: {kills}")
                    else:
                        result_label.config(text="No data found for the summoner in the last game.")
                else:
                    result_label.config(text="Error fetching match details")
            else:
                result_label.config(text="No match history found for the summoner.")
        else:
            result_label.config(text="Error fetching match history")
    else:
        result_label.config(text="Error fetching summoner details")

# Create the main window
window = tk.Tk()
window.title("Last Game Kills")

# Create a label and an entry for summoner name input
summoner_label = tk.Label(window, text="Summoner Name:")
summoner_label.pack(pady=10)

summoner_entry = tk.Entry(window, width=30)
summoner_entry.pack()

# Create a button to fetch the last game kills
fetch_button = tk.Button(window, text="Fetch Kills", command=get_last_game_kills)
fetch_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(window, text="")
result_label.pack(pady=10)

# Run the main event loop
window.mainloop()