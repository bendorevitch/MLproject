from nba_api.live.nba.endpoints import scoreboard, boxscore
from datetime import datetime, timezone
from dateutil import parser
import pandas as pd

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 

board = scoreboard.ScoreBoard()
print("ScoreBoardDate: " + board.score_board_date)
games = board.games.get_dict()
for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))

box = boxscore.BoxScore('0022300511') 

away_stats = box.away_team_stats.get_dict()
home_stats = box.home_team_stats.get_dict()

df = pd.DataFrame(columns=['FG_PCT_home','FT_PCT_home','FG3_PCT_home','AST_home','REB_home','FG_PCT_away','FT_PCT_away','FG3_PCT_away','AST_away','REB_away'])
df_per = pd.DataFrame(columns=['home','away'])


stats_list = []
teams_list = []

#get home stats
teams_list.append(home_stats['teamId'])

stats_list.append(home_stats['statistics']['fieldGoalsPercentage'])
stats_list.append(home_stats['statistics']['freeThrowsPercentage'])
stats_list.append(home_stats['statistics']['threePointersPercentage'])
stats_list.append(home_stats['statistics']['assists'])
stats_list.append(home_stats['statistics']['reboundsTotal'])

#get away stats
teams_list.append(away_stats['teamId'])

stats_list.append(away_stats['statistics']['fieldGoalsPercentage'])
stats_list.append(away_stats['statistics']['freeThrowsPercentage'])
stats_list.append(away_stats['statistics']['threePointersPercentage'])
stats_list.append(away_stats['statistics']['assists'])
stats_list.append(away_stats['statistics']['reboundsTotal'])

#getting game time
s = home_stats['statistics']['minutesCalculated']
for r in (("PT", ""), ("M", "")):
    s = s.replace(*r)
s = 48/(int(s)/5)
print(s)



df.loc[len(df)] = stats_list
df_per.loc[len(df_per)] = teams_list
print(df)

to_multiply = ['AST_home','REB_home','AST_away','REB_away']
for x in to_multiply:
    df[x] *= s
    df[x] = df[x].round(0)

print(df)