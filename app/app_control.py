from tkinter import *
from tkinter.ttk import *
from app_functions import app_functions


root = Tk()
root.geometry("600x200")
root.title('percent chance of winning')

def get_scoreboard_window():
    scoreboard = Toplevel(root)

    scoreboard.title("New Window")
 
    # sets the geometry of toplevel
    scoreboard.geometry("600x200")

    ap = app_functions
    sb_date , games, ids = ap.get_scoreboard()

    # A Label widget to show in toplevel
    Label(scoreboard, 
          text =sb_date).pack()
    for (item, id) in zip(games, ids):
        button = Button(scoreboard,text=item,command=lambda x=id :get_boxscore_window(x))
        button.pack()

def get_boxscore_window(id):
    boxscore = Toplevel(root)

    boxscore.title("New Window")
 
    # sets the geometry of toplevel
    boxscore.geometry("600x200")

    ap = app_functions
    probs = ap.get_boxscore(id)

    # A Label widget to show in toplevel
    Label(boxscore, 
          text =probs).pack()



get_today_scoreboard = Button(root, text="get todays games", command = get_scoreboard_window)
get_today_scoreboard.pack()

root.mainloop()