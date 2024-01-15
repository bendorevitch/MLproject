import tkinter as tk
from app_functions import app_functions

app = tk.Tk()
app.title("Python Desktop App")
app.geometry("800x600")

ap = app_functions()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=ap.get_scoreboard
)
button.pack()

app.mainloop()