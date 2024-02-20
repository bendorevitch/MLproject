from nba_api.live.nba.endpoints import scoreboard, boxscore
from datetime import timezone
from dateutil import parser

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import tkinter as tk

from team_colours import team_colours


class app_functions():
    def get_scoreboard():
        f = "{awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 
        board = scoreboard.ScoreBoard()
        game_dates= ("Score Board Date: " + board.score_board_date)

        games = board.games.get_dict()
        today_games = []
        today_games_id = []
        for game in games:
            gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
            today_games.append(f.format(awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
            today_games_id.append(game['gameId'])
        return game_dates ,today_games, today_games_id
    
    def get_boxscore(id):
        box = boxscore.BoxScore(id) 

        #get home and away team stats
        away_stats = box.away_team_stats.get_dict()
        home_stats = box.home_team_stats.get_dict()
    
        #create empty dataframe for stats
        df = pd.DataFrame(columns=['FG_PCT_home','FT_PCT_home','FG3_PCT_home','AST_home','REB_home','FG_PCT_away','FT_PCT_away','FG3_PCT_away','AST_away','REB_away'])
        df_per = pd.DataFrame(columns=['away','home'])

        #create empty lists to store stats in
        stats_list = []
        teams_list = []
        scores_colours = []

        #get home stats
        stats_list.append(home_stats['statistics']['fieldGoalsPercentage'])
        stats_list.append(home_stats['statistics']['freeThrowsPercentage'])
        stats_list.append(home_stats['statistics']['threePointersPercentage'])
        stats_list.append(home_stats['statistics']['assists'])
        stats_list.append(home_stats['statistics']['reboundsTotal'])

        #get away stats
        stats_list.append(away_stats['statistics']['fieldGoalsPercentage'])
        stats_list.append(away_stats['statistics']['freeThrowsPercentage'])
        stats_list.append(away_stats['statistics']['threePointersPercentage'])
        stats_list.append(away_stats['statistics']['assists'])
        stats_list.append(away_stats['statistics']['reboundsTotal'])

        #get team name
        away_name = away_stats['teamCity'] + ' ' + away_stats['teamName'] 
        home_name = home_stats['teamCity'] + ' ' + home_stats['teamName'] 
        teams_list.append(away_name)
        teams_list.append(home_name)

        #get scores
        away_score = away_stats['statistics']['points']
        home_score = home_stats['statistics']['points']
        scores_colours.append(away_score)
        scores_colours.append(home_score)

        #get colours
        away_colour= away_stats['teamTricode']
        home_colour = home_stats['teamTricode']

        #getting team colours from dict
        away_colour_code = team_colours[away_colour][0]
        home_colour_code = team_colours[home_colour][0]
        #if colours are same get another colour
        if away_colour_code == home_colour_code:
            away_colour_code = team_colours[away_colour][1]

        scores_colours.append(away_colour_code)
        scores_colours.append(home_colour_code)

        #adding stats to df
        df.loc[len(df)] = stats_list
        
        #adding teams to df
        df_per.loc[len(df_per)] = teams_list

        #for displaying original stats
        df_list = df.loc[0, :].values.tolist()

        #getting game time
        s = home_stats['statistics']['minutesCalculated']
        for r in (("PT", ""), ("M", "")):
            s = s.replace(*r)
        time_5 = int(s)/5
        per_of_time = 48/time_5 
        
        quater = time_5 //12
        minute = time_5 % 12

        game_time = 'Quater: ' + str(round(quater)) + ' Game Clock: ' + str(minute)

        #treating stats as if game was 48 minutes in (full time)
        to_multiply = ['AST_home','REB_home','AST_away','REB_away']
        for x in to_multiply:
            df[x] *= per_of_time
            df[x] = df[x].round(0)

        #loading in model
        loaded_model = pickle.load(open('model/LogisticRegression.sav', 'rb'))

        #getting win prediction from model
        score = loaded_model.predict_proba(df)
        
        #converting score to list
        score_list = score.tolist()
        
        #adding score to df
        df_per.loc[len(df_per)] = score_list[0]
        
        return df_per, game_time, scores_colours, df_list
    
    def figure_bars(a, b):
        end_first_rec = (a*400) + 100
        start_second_rec = end_first_rec 
        end_second_rec = start_second_rec + (b*400) - 100
        return end_first_rec, start_second_rec, end_second_rec
