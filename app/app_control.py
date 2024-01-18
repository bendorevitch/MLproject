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
    probs, game_time, scores_colours = ap.get_boxscore(id)

    probs_new, fig = ap.desgin_probs(probs)

    probs_new_teams = probs_new.iloc[0, :].values.tolist()

    # A Label widget to show in toplevel
    Label(boxscore, 
          text =game_time).pack()
    Label(boxscore, 
          text = "Away Team: " + probs_new_teams[0] + ' Score: ' + str(scores_colours[0])).pack()
    Label(boxscore, 
          text = "Home Team: " + probs_new_teams[1] + ' Score: ' + str(scores_colours[1])).pack()
    canvas = boxscore(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    

    


get_today_scoreboard = Button(root, text="get todays games", command = get_scoreboard_window)
get_today_scoreboard.pack()

root.mainloop()