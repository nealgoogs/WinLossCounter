import tkinter as tk

def button1_clicked():
    global counter1
    counter1 += 1
    counter_label1.config(text=str(counter1))

def button2_clicked():
    global counter2
    counter2 += 1
    counter_label2.config(text=str(counter2))

def calculate_kda():
    global kills, deaths, assists, total_kills, total_deaths, total_assists
    kda_label.config(text=f"KDA: {kills}/{deaths}/{assists}")
    kda_ratio = (kills + assists) / max(deaths, 1)
    kda_ratio = round(kda_ratio, 2)
    kda_ratio_label.config(text=f"KDA Ratio: {kda_ratio}")

    total_kills += kills
    total_deaths += deaths
    total_assists += assists
    total_kda_ratio = (total_kills + total_assists) / max(total_deaths, 1)
    total_kda_ratio = round(total_kda_ratio, 2)
    total_kda_ratio_label.config(text=f"Total KDA Ratio: {total_kda_ratio}")

    # Reset kills, deaths, and assists to zero
    kills = 0
    deaths = 0
    assists = 0

# Create the main window
window = tk.Tk()

# Set the window title
window.title("Win Counter")

window.configure(bg="black")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y position to center the window
x = (screen_width - 800) // 2
y = (screen_height - 600) // 2

# Set the window geometry
window.geometry(f"800x600+{x}+{y}")

# Counter variables
counter1 = 0
counter2 = 0
kills = 0
deaths = 0
assists = 0
total_kills = 0
total_deaths = 0
total_assists = 0

# Create a frame for button 1 and its counter label
button1_frame = tk.Frame(window, bg="lightblue")
button1_frame.place(relx=0.25, rely=0.4, anchor="center")

# Create counter label for button 1
counter_label1 = tk.Label(button1_frame, text=str(counter1), font=("Impact", 30), bg="lightblue", fg="white")
counter_label1.pack(pady=10)

# Create Button 1
button1 = tk.Button(button1_frame, text="WIN", command=button1_clicked, font=("Impact", 16), height=3, width=12, bg="blue", fg="white")
button1.pack()

# Create a frame for button 2 and its counter label
button2_frame = tk.Frame(window, bg="lightcoral")
button2_frame.place(relx=0.75, rely=0.4, anchor="center")

# Create counter label for button 2
counter_label2 = tk.Label(button2_frame, text=str(counter2), font=("Impact", 30), bg="lightcoral", fg="white")
counter_label2.pack(pady=10)

# Create Button 2
button2 = tk.Button(button2_frame, text="LOSS", command=button2_clicked, font=("Impact", 16), height=3, width=12, bg="red", fg="white")
button2.pack()

# Create a frame for the KDA section
kda_frame = tk.Frame(window, bg="white")
kda_frame.place(relx=0.5, rely=0.8, anchor="center")

# Create KDA label
kda_label = tk.Label(kda_frame, text="KDA: 0/0/0", font=("Impact", 16), bg="white")
kda_label.pack()

# Create KDA ratio label
kda_ratio_label = tk.Label(kda_frame, text="KDA Ratio: 0.00", font=("Impact", 16), bg="white")
kda_ratio_label.pack()

# Create total KDA ratio label
total_kda_ratio_label = tk.Label(kda_frame, text="Total KDA Ratio: 0.00", font=("Impact", 16), bg="white")
total_kda_ratio_label.pack()

# Create labels and entry widgets for kills, deaths, and assists
kills_label = tk.Label(kda_frame, text="Kills:", font=("Impact", 12), bg="white")
kills_label.pack(side="left", padx=5, pady=5)
kills_entry = tk.Entry(kda_frame, font=("Impact", 12), width=5)
kills_entry.pack(side="left", padx=5, pady=5)

deaths_label = tk.Label(kda_frame, text="Deaths:", font=("Impact", 12), bg="white")
deaths_label.pack(side="left", padx=5, pady=5)
deaths_entry = tk.Entry(kda_frame, font=("Impact", 12), width=5)
deaths_entry.pack(side="left", padx=5, pady=5)

assists_label = tk.Label(kda_frame, text="Assists:", font=("Impact", 12), bg="white")
assists_label.pack(side="left", padx=5, pady=5)
assists_entry = tk.Entry(kda_frame, font=("Impact", 12), width=5)
assists_entry.pack(side="left", padx=5, pady=5)

def calculate_kda_from_entries():
    global kills, deaths, assists
    try:
        kills = int(kills_entry.get())
        deaths = int(deaths_entry.get())
        assists = int(assists_entry.get())
        calculate_kda()
    except ValueError:
        pass

# Create a button to calculate the KDA ratio
calculate_button = tk.Button(kda_frame, text="Calculate", command=calculate_kda_from_entries, font=("Impact", 12))
calculate_button.pack(pady=10)

# Run the main event loop
window.mainloop()

