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

box = boxscore.BoxScore('0022300467') 
away_stats = box.away_team_stats.get_dict()
home_stats = box.home_team_stats.get_dict()

df = pd.DataFrame(columns=['teamId','score','freeThrowsPercentage','fieldGoalsPercentage','threePointersPercentage','assists','reboundsTotal','home'])

#get away stats
away_stats_list = []
away_stats_list.append(away_stats['teamId'])
away_stats_list.append(away_stats['score'])
away_stats_list.append(away_stats['statistics']['freeThrowsPercentage'])
away_stats_list.append(away_stats['statistics']['fieldGoalsPercentage'])
away_stats_list.append(away_stats['statistics']['threePointersPercentage'])
away_stats_list.append(away_stats['statistics']['assists'])
away_stats_list.append(away_stats['statistics']['reboundsTotal'])
away_stats_list.append(0)

#get home stats
home_stats_list = []
home_stats_list.append(home_stats['teamId'])
home_stats_list.append(home_stats['score'])
home_stats_list.append(home_stats['statistics']['freeThrowsPercentage'])
home_stats_list.append(home_stats['statistics']['fieldGoalsPercentage'])
home_stats_list.append(home_stats['statistics']['threePointersPercentage'])
home_stats_list.append(home_stats['statistics']['assists'])
home_stats_list.append(home_stats['statistics']['reboundsTotal'])
home_stats_list.append(1)

print(home_stats_list)

df.loc[len(df)] = away_stats_list
df.loc[len(df)] = home_stats_list
print(df)