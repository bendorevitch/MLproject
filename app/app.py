from nba_api.live.nba.endpoints import scoreboard

# Today's Score Board
games = scoreboard.ScoreBoard()

# json
games.get_json()

# dictionary
g = games.get_dict()

print(g)