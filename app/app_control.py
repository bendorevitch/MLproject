from tkinter import *
from tkinter.ttk import *
from app_functions import app_functions


class MainApp:
      def __init__(self, master = None):
            self.master = master
      
            # Calls create method of class MainApp
            self.create()

      def create(self):
            get_today_scoreboard = Button(root, text="get todays games", command = self.get_scoreboard_window)
            get_today_scoreboard.pack()

      def get_scoreboard_window(self):
            scoreboard = Toplevel()

            scoreboard.title("New Window")
            
            # sets the geometry of toplevel
            scoreboard.geometry("600x200")

            ap = app_functions
            sb_date , games, ids = ap.get_scoreboard()

            # A Label widget to show in toplevel
            Label(scoreboard, 
                  text =sb_date).pack()
            for (item, id) in zip(games, ids):
                  button = Button(scoreboard,text=item,command=lambda x=id : self.get_boxscore_window(x))
                  button.pack()

      def get_boxscore_window(self, id):
            boxscore = Toplevel()

            boxscore.title("New Window")
            
            # sets the geometry of toplevel
            boxscore.geometry("600x400")

            ap = app_functions
            probs, game_time, scores_colours = ap.get_boxscore(id)
            

            probs_new_teams = probs.iloc[0, :].values.tolist()

            probs_new_num = probs.iloc[1, :].values.tolist()

            print(probs_new_num)

            # A Label widget to show in toplevel
            Label(boxscore, 
                  text =game_time).pack()
            Label(boxscore, 
                  text = "Away Team: " + probs_new_teams[0] + ' Score: ' + str(scores_colours[0])).pack()
            Label(boxscore, 
                  text = "Home Team: " + probs_new_teams[1] + ' Score: ' + str(scores_colours[1])).pack()
            self.canvas = Canvas(boxscore)
            print(scores_colours[2])
           
            self.canvas.create_rectangle(100,100,(100 + (probs_new_num[0]*400)),90, fill=scores_colours[2])
            self.canvas.create_rectangle(((probs_new_num[0]*400)),100,(100 + (probs_new_num[1]*400)),90, fill=scores_colours[3])
            
            self.canvas.pack(fill = BOTH, expand = True)


if __name__ == "__main__":
     
      # initalise app
      root = Tk()
      geeks = MainApp(root)
      
      # This sets the title to Lines
      root.title('percent chance of winning')
      
      # This sets the geometry and position of window
      # on the screen
      root.geometry("600x200")

      # Infinite loop breaks only by interrupt
      root.mainloop()