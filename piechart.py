import requests
import datetime
import pytz
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from constants import SUMMMONER_BY_NAME_URL, MATCH_HISTORY_URL, MATCH_DETAILS_URL

summoner_entry = None
result_label = None
chart_canvas = None
window = None

def get_stats_per_day():
    global summoner_entry, result_label, chart_canvas

    summoner_name = summoner_entry.get()
    response = requests.get(SUMMMONER_BY_NAME_URL.format(summoner_name))

    if response.status_code == 200:
        summoner_data = response.json()
        puuid = summoner_data["puuid"]

        # Get the current date in the desired timezone (EST)
        est_timezone = pytz.timezone("US/Eastern")
        now = datetime.datetime.now(est_timezone)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Calculate the start time for the previous day
        start_time = midnight - datetime.timedelta(days=1)

        # Convert the start and end times to UTC
        start_time_utc = start_time.astimezone(pytz.utc)
        midnight_utc = midnight.astimezone(pytz.utc)

        # Format the start and end times to match the API requirements
        formatted_start_time = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
        formatted_midnight = midnight_utc.strftime("%Y-%m-%dT%H:%M:%S")

        match_history_response = requests.get(MATCH_HISTORY_URL.format(puuid, formatted_start_time, formatted_midnight))

        if match_history_response.status_code == 200:
            match_history_data = match_history_response.json()

            if len(match_history_data) > 0:
                matches = match_history_data

                stats_per_day = {}  # Dictionary to store stats per day

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

                            # Get the date of the match
                            timestamp = match_details_data["info"]["gameCreation"] / 1000
                            match_date = datetime.datetime.fromtimestamp(timestamp, tz=est_timezone).date()

                            # Add the stats to the corresponding date in the dictionary
                            if match_date not in stats_per_day:
                                stats_per_day[match_date] = {
                                    "wins": 0,
                                    "losses": 0,
                                    "total_kills": 0,
                                    "total_deaths": 0,
                                    "total_assists": 0
                                }

                            stats_per_day[match_date]["total_kills"] += kills
                            stats_per_day[match_date]["total_deaths"] += deaths
                            stats_per_day[match_date]["total_assists"] += assists

                            if win:
                                stats_per_day[match_date]["wins"] += 1
                            else:
                                stats_per_day[match_date]["losses"] += 1

                # Prepare the result text
                result_text = ""
                for date, stats in sorted(stats_per_day.items()):
                    result_text += f"Date: {date}\n"
                    result_text += f"Wins: {stats['wins']}\n"
                    result_text += f"Losses: {stats['losses']}\n\n"

                    # Plotting the pie chart for each day
                    fig = Figure(figsize=(4, 4), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.pie([stats['wins'], stats['losses']], labels=["Wins", "Losses"], autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')
                    ax.set_title(f"Win/Loss Ratio for {date}")

                    # Convert the figure to a Tkinter canvas
                    chart_canvas = FigureCanvasTkAgg(fig, master=window)
                    chart_canvas.draw()
                    chart_canvas.get_tk_widget().pack(side=tk.LEFT)

                result_label.config(text=result_text)
            else:
                result_label.config(text="No matches found.")
        else:
            result_label.config(text="Error fetching match history")
    else:
        result_label.config(text="Error fetching summoner details")

def main():
    global summoner_entry, result_label, chart_canvas, window

    # Create the main window
    window = tk.Tk()
    window.title("Stats Per Day")
    window.geometry("600x400")

    # Create a label and an entry for summoner name input
    summoner_label = ttk.Label(window, text="Summoner Name:")
    summoner_label.pack(pady=10)

    summoner_entry = ttk.Entry(window, width=50)
    summoner_entry.pack()

    # Create a button to fetch the stats per day
    fetch_button = ttk.Button(window, text="Get Stats Per Day", command=get_stats_per_day)
    fetch_button.pack(pady=10)

    # Create a frame to hold the result label and the chart canvas
    result_frame = ttk.Frame(window)
    result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Create a label to display the result
    result_label = ttk.Label(result_frame, text="", anchor="center")
    result_label.pack(side=tk.LEFT)

    # Run the main event loop
    window.mainloop()

if __name__ == "__main__":
    main()
