from nba_api.live.nba.endpoints import scoreboard, boxscore
from datetime import timezone
from dateutil import parser

import pandas as pd
import pickle
import tkinter as tk


class app_functions():
    def get_scoreboard():
        f = "{awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 
        board = scoreboard.ScoreBoard()
        game_dates= ("ScoreBoardDate: " + board.score_board_date)

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

        away_stats = box.away_team_stats.get_dict()
        home_stats = box.home_team_stats.get_dict()

        df = pd.DataFrame(columns=['FG_PCT_home','FT_PCT_home','FG3_PCT_home','AST_home','REB_home','FG_PCT_away','FT_PCT_away','FG3_PCT_away','AST_away','REB_away'])
        df_per = pd.DataFrame(columns=['away','home'])


        stats_list = []
        teams_list = []

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

        #get team id
        teams_list.append(away_stats['teamId'])
        teams_list.append(home_stats['teamId'])


        #getting game time
        s = home_stats['statistics']['minutesCalculated']
        for r in (("PT", ""), ("M", "")):
            s = s.replace(*r)
        s = 48/(int(s)/5)

        df.loc[len(df)] = stats_list
        df_per.loc[len(df_per)] = teams_list

        to_multiply = ['AST_home','REB_home','AST_away','REB_away']
        for x in to_multiply:
            df[x] *= s
            df[x] = df[x].round(0)

        loaded_model = pickle.load(open('model/LogisticRegression.sav', 'rb'))

        score = loaded_model.predict_proba(df)
        score_list = score.tolist()
        df_per.loc[len(df_per)] = score_list[0]
        return df_per
