import requests
import json

ALL_GAMES_URL = ('http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1'
                     '&startDate={start_year:04d}-{start_month:02d}-{start_day:02d}'
                     '&endDate={end_year:04d}-{end_month:02d}-{end_day:02d}')


GAME_URL_TEMPLATE = 'http://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'


game_date_pk_tuple_list = []
for year in range(2025, 2026):
	all_games_dict = requests.get(
	    ALL_GAMES_URL.format(start_month=1, start_day=1, start_year=year,
	    					 end_month=12, end_day=31, end_year=year)
	).json()

	if len(all_games_dict['dates']) > 0:
		for date_dict in all_games_dict['dates']:
			for game in date_dict['games']:
				game_date_pk_tuple_list.append((date_dict['date'], game['gamePk']))


for game_date, game_pk in game_date_pk_tuple_list:
    game_dict = requests.get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
    with open(f'./raw_reference_data/{game_date}-{game_pk}.json', 'w') as fh:
    	fh.write(json.dumps(game_dict))
