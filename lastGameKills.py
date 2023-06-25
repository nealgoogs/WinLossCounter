import requests
import tkinter as tk


from constants import SUMMMONER_BY_NAME_URL, MATCH_HISTORY_URL, MATCH_DETAILS_URL

def get_last_10_games_stats():
    summoner_name = summoner_entry.get()
    response = requests.get(SUMMMONER_BY_NAME_URL.format(summoner_name))

    if response.status_code == 200:
        summoner_data = response.json()
        puuid = summoner_data["puuid"]

        match_history_response = requests.get(MATCH_HISTORY_URL.format(puuid))

        if match_history_response.status_code == 200:
            match_history_data = match_history_response.json()

            if len(match_history_data) > 0:
                matches = match_history_data[:10]  # Retrieve the last 10 matches

                wins = 0
                losses = 0
                total_kills = 0
                total_deaths = 0
                total_assists = 0

                for match_id in matches:
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

                            if win:
                                wins += 1
                            else:
                                losses += 1

                            total_kills += kills
                            total_deaths += deaths
                            total_assists += assists



                if total_deaths == 0:
                    kda_ratio = (total_kills + total_assists) / 1
                else:
                    kda_ratio = (total_kills + total_assists) / total_deaths

                result_label.config(text=f"Wins: {wins}\nLosses: {losses}\n"
                                         f"KDA Ratio in the last 10 games: {kda_ratio:.2f}")
                


            else:
                result_label.config(text="No match history found for the summoner.")
        else:
            result_label.config(text="Error fetching match history")
    else:
        result_label.config(text="Error fetching summoner details")

# Create the main window
window = tk.Tk()
window.title("Last 10 Games Stats")
window.geometry("500x300")
window.configure(bg="lightgray") 

# Create a label and an entry for summoner name input
summoner_label = tk.Label(window, text="Summoner Name:", font=("Arial", 14), bg="lightgray")
summoner_label.pack(pady=10)

summoner_entry = tk.Entry(window, width=30, font=("Arial", 12))
summoner_entry.pack()

# Create a button to fetch the last 10 games stats
fetch_button = tk.Button(window, text="Get Stats", command=get_last_10_games_stats, font=("Arial", 12), bg="blue", fg="white")
fetch_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(window, text="", font=("Arial", 14), bg="lightgray")
result_label.pack(pady=10)

# Run the main event loop
window.mainloop()
