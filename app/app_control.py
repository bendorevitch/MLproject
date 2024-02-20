from tkinter import *
from tkinter.ttk import *
from app_functions import app_functions

class MainApp:
      def __init__(self, master = None):
            self.master = master
      
            # Calls create method of class MainApp
            self.create()

      def create(self):
            Label(root, text = "NBA Chance of Winning", background = "#eed9c4", font=("Arial", 30)).pack(pady=(20,30))
            
            Button(root, text="Get Todays Games", command = self.get_scoreboard_window).pack()

      def get_scoreboard_window(self):
            scoreboard = Toplevel()

            scoreboard.title("New Window")
            
            # sets the geometry of toplevel
            scoreboard.geometry("600x400")
            scoreboard.configure(background='#eed9c4')

            ap = app_functions
            sb_date , games, ids = ap.get_scoreboard()

            # A Label widget to show in toplevel
            Label(scoreboard, 
                  text =sb_date, background = "#eed9c4", font=("Arial", 30)).pack()
            for (item, id) in zip(games, ids):
                  button = Button(scoreboard,text=item,command=lambda x=id : self.get_boxscore_window(x))
                  button.pack()
            Button(scoreboard,text='TEST',command=lambda x='0021701171' : self.get_boxscore_window(x)).pack()
                  

      def get_boxscore_window(self, id):
            boxscore = Toplevel()

            boxscore.title("New Window")
            
            # sets the geometry of toplevel
            boxscore.geometry("600x400")
            boxscore.configure(background='#eed9c4')

            ap = app_functions
            probs, game_time, scores_colours, df_list = ap.get_boxscore(id)
            
            probs_new_teams = probs.iloc[0, :].values.tolist()

            probs_new_num = probs.iloc[1, :].values.tolist()

            print(probs_new_num)

            x1, x2, x3 = ap.figure_bars(probs_new_num[0], probs_new_num[1])
            
            # A Label widget to show in toplevel
            Label(boxscore, 
                  text =game_time).pack()
            Label(boxscore, 
                  text = "Away Team: " + probs_new_teams[0] + ' Score: ' + str(scores_colours[0])).pack()
            Label(boxscore, 
                  text = "Home Team: " + probs_new_teams[1] + ' Score: ' + str(scores_colours[1])).pack()
            self.canvas = Canvas(boxscore)
            print(scores_colours[2])
           
            self.canvas.create_rectangle(100,100,x1,90, fill=scores_colours[2])
            self.canvas.create_rectangle(x2,100,x3,90, fill=scores_colours[3])
            
            self.canvas.pack()


if __name__ == "__main__":
     
      # initalise app
      root = Tk()
      geeks = MainApp(root)
      
      # This sets the title to Lines
      root.title('percent chance of winning')
      
      # This sets the geometry and position of window
      # on the screen
      root.geometry("600x400")
      root.configure(background='#eed9c4')

      # Infinite loop breaks only by interrupt
      root.mainloop()