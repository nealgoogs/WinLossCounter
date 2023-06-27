import requests
import datetime
import pytz
import tkinter as tk
from tkinter import ttk

from constants import SUMMMONER_BY_NAME_URL, MATCH_HISTORY_URL, MATCH_DETAILS_URL

summoner_entry = None
result_label = None

def get_stats_for_january():
    global summoner_entry, result_label

    summoner_name = summoner_entry.get()
    response = requests.get(SUMMMONER_BY_NAME_URL.format(summoner_name))

    if response.status_code == 200:
        summoner_data = response.json()
        puuid = summoner_data["puuid"]

        est_tz = pytz.timezone("US/Eastern")
        start_time = datetime.datetime(2023, 1, 1, tzinfo=est_tz)
        end_time = datetime.datetime(2023, 2, 1, tzinfo=est_tz)

        start_time_utc = start_time.astimezone(pytz.utc)
        end_time_utc = end_time.astimezone(pytz.utc)

        formatted_start_time = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
        formatted_end_time = end_time_utc.strftime("%Y-%m-%dT%H:%M:%S")

        match_history_response = requests.get(MATCH_HISTORY_URL.format(puuid, formatted_start_time, formatted_end_time))

        if match_history_response.status_code == 200:
            match_history_data = match_history_response.json()

            if "info" in match_history_data:
                matches = match_history_data["info"]["matches"]

                stats_for_january = {
                    "wins": 0,
                    "losses": 0,
                    "total_kills": 0,
                    "total_deaths": 0,
                    "total_assists": 0
                }

                for match in matches:
                    match_timestamp = match["timestamp"] / 1000
                    match_date = datetime.datetime.fromtimestamp(match_timestamp, tz=est_tz)

                    if start_time <= match_date < end_time:
                        match_id = match["gameId"]

                        match_details_response = requests.get(MATCH_DETAILS_URL.format(match_id))

                        if match_details_response.status_code == 200:
                            match_details_data = match_details_response.json()

                            participants = match_details_data["info"]["participants"]
                            participant = next((p for p in participants if p["summonerName"] == summoner_name), None)

                            if participant:
                                win = participant["win"]
                                kills = participant["kills"]
                                deaths = participant["deaths"]
                                assists = participant["assists"]

                                stats_for_january["total_kills"] += kills
                                stats_for_january["total_deaths"] += deaths
                                stats_for_january["total_assists"] += assists

                                if win:
                                    stats_for_january["wins"] += 1
                                else:
                                    stats_for_january["losses"] += 1

                # Calculate KDA ratio for January
                total_kills = stats_for_january["total_kills"]
                total_deaths = stats_for_january["total_deaths"]
                total_assists = stats_for_january["total_assists"]

                if total_deaths == 0:
                    kda_ratio = (total_kills + total_assists) / 1
                else:
                    kda_ratio = (total_kills + total_assists) / total_deaths

                stats_for_january["kda_ratio"] = kda_ratio

                # Prepare the result text
                result_text = ""
                result_text += f"Wins: {stats_for_january['wins']}\n"
                result_text += f"Losses: {stats_for_january['losses']}\n"
                result_text += f"KDA Ratio: {stats_for_january['kda_ratio']:.2f}\n"

                result_label.config(text=result_text)
            else:
                result_label.config(text="No matches found.")
        else:
            result_label.config(text="Error fetching match history")
    else:
        result_label.config(text="Error fetching summoner details")

def main():
    global summoner_entry, result_label

    # Create the main window
    window = tk.Tk()
    window.title("Stats for January 2023")
    window.geometry("400x300")

    # Create a label and an entry for summoner name input
    summoner_label = ttk.Label(window, text="Summoner Name:")
    summoner_label.pack(pady=10)

    summoner_entry = ttk.Entry(window, width=50)
    summoner_entry.pack()

    # Create a button to fetch the stats for January
    fetch_button = ttk.Button(window, text="Get Stats for January", command=get_stats_for_january)
    fetch_button.pack(pady=10)

    # Create a label to display the result
    result_label = ttk.Label(window, text="", anchor="center")
    result_label.pack(pady=10, fill=tk.BOTH, expand=True)

    # Run the main event loop
    window.mainloop()

if __name__ == "__main__":
    main()
