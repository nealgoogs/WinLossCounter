import tkinter as tk

def button1_clicked():
    global counter1
    counter1 += 1
    counter_label1.config(text=str(counter1))

def button2_clicked():
    global counter2
    counter2 += 1
    counter_label2.config(text=str(counter2))

# Create the main window
window = tk.Tk()

# Set the window title
window.title("Win Counter")

window.configure(bg="black")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y position to center the window
x = (screen_width - 400) // 2
y = (screen_height - 300) // 2

# Set the window geometry
window.geometry(f"400x300+{x}+{y}")

# Counter variables
counter1 = 0
counter2 = 0

# Create a frame for button 1 and its counter label
button1_frame = tk.Frame(window, bg="lightblue")
button1_frame.place(relx=0.25, rely=0.5, anchor="center")

# Create counter label for button 1
counter_label1 = tk.Label(button1_frame, text=str(counter1), font=("Impact", 30), bg="lightblue", fg="white")
counter_label1.pack(pady=10)

# Create Button 1
button1 = tk.Button(button1_frame, text="WIN", command=button1_clicked, font=("Impact", 16), height=3, width=12, bg="blue", fg="white")
button1.pack()

# Create a frame for button 2 and its counter label
button2_frame = tk.Frame(window, bg="lightcoral")
button2_frame.place(relx=0.75, rely=0.5, anchor="center")

# Create counter label for button 2
counter_label2 = tk.Label(button2_frame, text=str(counter2), font=("Impact", 30), bg="lightcoral", fg="white")
counter_label2.pack(pady=10)

# Create Button 2
button2 = tk.Button(button2_frame, text="LOSS", command=button2_clicked, font=("Impact", 16), height=3, width=12, bg="red", fg="white")
button2.pack()

# Run the main event loop
window.mainloop()




