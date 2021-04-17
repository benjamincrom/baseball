import datetime

from re import search, sub

from pytz import timezone

from baseball.baseball import (Player, PlayerAppearance, PlateAppearance, Game,
                               Inning, Team)

from baseball.baseball_events import (AUTOMATIC_BALL_POSITION, Pitch, Pickoff,
                                      RunnerAdvance)

from baseball.process_game_xml import (
    get_datetime, get_sub_switch_steal_flags, parse_substitution,
    process_substitution, parse_switch_description, process_switch,
    fix_description
)

def process_pitch(event):
    pitch_description = event['details']['call']['description']
    if event['details'].get('type'):
        pitch_type = event['details']['type']['code']
    else:
        pitch_type = ''

    pitch_datetime = get_datetime(event['startTime'])

    if (not event['pitchData']['coordinates'].get('x') or
            not event['pitchData']['coordinates'].get('y') or
            event['pitchData']['coordinates'].get('x') == 'None' or
            event['pitchData']['coordinates'].get('y') == 'None'):
        (pitch_x, pitch_y) = AUTOMATIC_BALL_POSITION
    else:
        pitch_x = float(event['pitchData']['coordinates'].get('x'))
        pitch_y = float(event['pitchData']['coordinates'].get('y'))

    pitch_position = (pitch_x, pitch_y)

    if event['pitchData'].get('startSpeed'):
        pitch_speed = float(event['pitchData'].get('startSpeed'))
    else:
        pitch_speed = None

    pitch_obj = Pitch(pitch_datetime, pitch_description, pitch_type,
                      pitch_speed, pitch_position)

    return pitch_obj

def process_pickoff(event):
    pickoff_description = event['details'].get('description')
    pickoff_base = pickoff_description.split()[-1]

    if (pickoff_description.split()[1] == 'Attempt' or
            pickoff_description.split()[1] == 'Error'):
        pickoff_was_successful = False
    elif len(pickoff_description.split()) == 2:
        pickoff_was_successful = True
    else:
        raise ValueError('Bad Pickoff description.')

    pickoff_obj = Pickoff(
        pickoff_description,
        pickoff_base,
        pickoff_was_successful
    )

    return pickoff_obj

def process_plate_appearance(plate_appearance, inning_half_str, inning_num,
                             next_batter_num, game_obj):
    event_list = []
    scoring_runners_list = []
    runners_batted_in_list = []
    for event in plate_appearance['playEvents']:
        if event['type'] == 'pitch':
            pitch_obj = process_pitch(event)
            event_list.append(pitch_obj)
        elif event['type'] == 'pickoff':
            pickoff_obj = process_pickoff(event)
            event_list.append(pickoff_obj)
        elif event['type'] == 'action':
            event_description = event['details']['description']
            event_summary = event['details'].get('event', '')
            event_datetime = get_datetime(event['startTime'])

            substitution_flag, switch_flag, _ = get_sub_switch_steal_flags(
                event_summary,
                event_description
            )

            if substitution_flag:
                (substituting_team,
                 substitution_obj) = parse_substitution(event_datetime,
                                                        event_description,
                                                        event_summary,
                                                        inning_half_str,
                                                        game_obj)

                event_list.append(substitution_obj)
                process_substitution(substitution_obj, inning_num,
                                     inning_half_str, next_batter_num,
                                     substituting_team)

            elif switch_flag:
                (switch_obj,
                 switching_team) = parse_switch_description(event_datetime,
                                                            event_description,
                                                            event_summary,
                                                            game_obj,
                                                            inning_half_str)

                event_list.append(switch_obj)
                process_switch(switch_obj, inning_num, inning_half_str,
                               next_batter_num, switching_team)
        elif event['type'] == 'no_pitch':
            pass
        else:
            raise Exception('Invalid event type')

    (event_list,
     scoring_runners_list,
     runners_batted_in_list) = process_runner_list(plate_appearance,
                                                   game_obj,
                                                   event_list,
                                                   scoring_runners_list,
                                                   runners_batted_in_list)

    return event_list, scoring_runners_list, runners_batted_in_list

def process_runner_list(plate_appearance, game_obj, event_list,
                        scoring_runners_list, runners_batted_in_list):
    for runner_event in plate_appearance['runners']:
        runner_id = int(runner_event['details']['runner']['id'])

        if runner_id in game_obj.away_team:
            runner = game_obj.away_team[runner_id]
        elif runner_id in game_obj.home_team:
            runner = game_obj.home_team[runner_id]
        else:
            raise ValueError('Runner ID not in player dict')

        start_base = runner_event['movement'].get('start') or ''
        end_base = runner_event['movement'].get('end', '') or ''
        run_description = runner_event['details'].get('event')
        runner_scored = (runner_event['movement'].get('end') == 'score')
        run_earned = runner_event['details'].get('earned')
        is_rbi = runner_event['details'].get('rbi')

        runner_advance_obj = RunnerAdvance(run_description,
                                           runner,
                                           start_base,
                                           end_base,
                                           runner_scored,
                                           run_earned,
                                           is_rbi)

        if runner_advance_obj.runner_scored:
            scoring_runners_list.append(runner_advance_obj.runner)

            if runner_advance_obj.is_rbi:
                runners_batted_in_list.append(runner_advance_obj.runner)

        event_list.append(runner_advance_obj)

    return event_list, scoring_runners_list, runners_batted_in_list

def process_at_bat(plate_appearance, event_list, game_obj,
                   inning_half_str, inning_num, next_batter_num):
    (new_event_list,
     scoring_runners_list,
     runners_batted_in_list) = process_plate_appearance(plate_appearance,
                                                        inning_half_str,
                                                        inning_num,
                                                        next_batter_num,
                                                        game_obj)

    event_list += new_event_list
    if plate_appearance['result'].get('description'):
        plate_appearance_desc = fix_description(
            plate_appearance['result'].get('description')
        )
    else:
        plate_appearance_desc = ''

    pitcher_id = int(plate_appearance['matchup']['pitcher']['id'])
    inning_outs = int(plate_appearance['count']['outs'])

    pitcher = None
    for this_team in [game_obj.home_team, game_obj.away_team]:
        if pitcher_id in this_team:
            pitcher = this_team[pitcher_id]

    if not pitcher:
        raise ValueError('Batter ID not in player_dict')

    batter_id = int(plate_appearance['matchup']['batter']['id'])
    if batter_id in game_obj.home_team:
        batter = game_obj.home_team[batter_id]
        batting_team = game_obj.home_team
    elif batter_id in game_obj.away_team:
        batter = game_obj.away_team[batter_id]
        batting_team = game_obj.away_team
    else:
        raise ValueError('Batter ID not in player_dict')

    start_datetime = get_datetime(plate_appearance['about']['startTime'])
    end_datetime = get_datetime(plate_appearance['about']['endTime'])
    plate_appearance_summary = (
        plate_appearance['result'].get('event', '').strip()
    )

    plate_appearance_obj = PlateAppearance(start_datetime,
                                           end_datetime,
                                           batting_team,
                                           plate_appearance_desc,
                                           plate_appearance_summary,
                                           pitcher,
                                           batter,
                                           inning_outs,
                                           scoring_runners_list,
                                           runners_batted_in_list,
                                           event_list)

    return plate_appearance_obj

def set_pitcher_wls_codes(game_dict, game):
    teams_dict = game_dict['liveData']['boxscore']['teams']
    away_wls_dict = {
        x['person']['id']: x['stats']['pitching']['note'][1]
        for _, x in teams_dict['away']['players'].items()
        if x['stats']['pitching'].get('note')
    }

    home_wls_dict = {
        x['person']['id']: x['stats']['pitching']['note'][1]
        for _, x in teams_dict['home']['players'].items()
        if x['stats']['pitching'].get('note')
    }

    for pitcher_appearance in game.away_team.pitcher_list:
        pitcher_id = pitcher_appearance.player_obj.mlb_id
        if pitcher_id in away_wls_dict:
            pitcher_appearance.pitcher_credit_code = (
                away_wls_dict[pitcher_id]
            )
        else:
            pitcher_appearance.pitcher_credit_code = ''


    for pitcher_appearance in game.home_team.pitcher_list:
        pitcher_id = pitcher_appearance.player_obj.mlb_id
        if pitcher_id in home_wls_dict:
            pitcher_appearance.pitcher_credit_code = (
                home_wls_dict[pitcher_id]
            )
        else:
            pitcher_appearance.pitcher_credit_code = ''

def process_half_inning(plate_appearance_dict_list, inning_half_str, game_obj):
    if inning_half_str not in ('top', 'bottom'):
        raise ValueError('Invalid inning half str.')

    plate_appearance_list = []
    inning_num = len(game_obj.inning_list) + 1
    next_batter_num = 1
    for plate_appearance_dict in plate_appearance_dict_list:
        event_list = []
        if plate_appearance_dict['result'].get('event') == 'Game Advisory':
            continue

        plate_appearance_list.append(
            process_at_bat(plate_appearance_dict,
                           event_list,
                           game_obj,
                           inning_half_str,
                           inning_num,
                           next_batter_num))

        next_batter_num += 1

    return plate_appearance_list

def process_inning(baseball_inning, game_obj):
    top_half_appearance_list = process_half_inning(
        baseball_inning['top'],
        'top',
        game_obj
    ) or []

    if baseball_inning.get('bottom'):
        bottom_half_appearance_list = process_half_inning(
            baseball_inning['bottom'],
            'bottom',
            game_obj
        )
    else:
        bottom_half_appearance_list = []

    if top_half_appearance_list and top_half_appearance_list[-1] is None:
        del top_half_appearance_list[-1]
    if bottom_half_appearance_list and bottom_half_appearance_list[-1] is None:
        del bottom_half_appearance_list[-1]

    this_inning_obj = Inning(top_half_appearance_list,
                             bottom_half_appearance_list)

    return this_inning_obj

def parse_name(batter_name):
    if search(r'\w\s+[A-Z]\.\s+', batter_name):
        batter_name = sub(r'\s[A-Z]\.\s+', ' ', batter_name)

    player_first_name, player_last_name = batter_name.split(' ', 1)

    return player_first_name, player_last_name

def set_player_list(team_dict, gamedata_dict, team):
    digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for player_id, this_player_dict in team_dict['players'].items():
        gamedata_player_dict = gamedata_dict['players'][player_id]
        jersey_number = ''
        if ('jerseyNumber' in this_player_dict and
                this_player_dict.get('jerseyNumber')):
            if all([character in digit_list
                    for character in this_player_dict.get('jerseyNumber')]):
                jersey_number = int(this_player_dict.get('jerseyNumber'))

        (first_name, last_name) = parse_name(
            this_player_dict['person']['fullName']
        )

        new_player = Player(
            last_name,
            first_name,
            this_player_dict['person']['id'],
            float(this_player_dict['seasonStats']['batting']['obp']),
            float(this_player_dict['seasonStats']['batting']['slg']),
            jersey_number
        )

        new_player.pitch_hand = gamedata_player_dict['pitchHand']['code']
        new_player.bat_side = gamedata_player_dict['batSide']['code']

        if this_player_dict['seasonStats']['pitching']['era'] != '-.--':
            this_era = float(this_player_dict['seasonStats']['pitching']['era'])
            if this_era != 0.0:
                new_player.era = this_era
            else:
                new_player.era = ''
        else:
            new_player.era = ''

        team.append(new_player)

def initialize_team(team_gamedata_dict, team_livedata_dict, full_gamedata_dict):
    team = Team(
        team_gamedata_dict['name'],
        team_gamedata_dict['abbreviation']
    )

    set_player_list(team_livedata_dict, full_gamedata_dict, team)
    if team_livedata_dict.get('pitchers'):
        team.pitcher_list = [
            PlayerAppearance(
                team[team_livedata_dict['pitchers'][0]], 1, 1, 'top', 1
            )
        ]
    else:
        team.pitcher_list = []

    for _, player_dict in team_livedata_dict['players'].items():
        if player_dict.get('battingOrder'):
            batting_order = int(player_dict['battingOrder'])
            position = player_dict['allPositions'][0]['code']

            if batting_order % 100 == 0:
                batting_index = int((batting_order / 100) - 1)
                team.batting_order_list_list[batting_index] = [
                    PlayerAppearance(team[int(player_dict['person']['id'])],
                                     position,
                                     1,
                                     'top',
                                     1)
                ]

    return team

def get_inning_dict_list(game_dict):
    inning_dict_list = []
    inning_num = 1
    inning_half = 'top'

    while True:
        play_dict_list = []
        for this_play_dict in game_dict['liveData']['plays']['allPlays']:
            if (this_play_dict['about']['inning'] == inning_num and
                    this_play_dict['about']['halfInning'] == inning_half):
                play_dict_list.append(this_play_dict)

        if play_dict_list and inning_half == 'top':
            inning_dict_list.append({'top': play_dict_list})
            inning_half = 'bottom'
        elif play_dict_list and inning_half == 'bottom':
            inning_dict_list[-1]['bottom'] = play_dict_list
            inning_num += 1
            inning_half = 'top'
        elif play_dict_list:
            raise Exception('Invalid inning half value')
        else:
            break

    return inning_dict_list

def set_game_inning_list(inning_dict_list, game_obj):
    for _, inning_dict in enumerate(inning_dict_list):
        game_obj.inning_list.append(process_inning(inning_dict, game_obj))

def initialize_game(this_game, attendance_str, temperature_str, weather_str,
                    start_datetime_str):
    away_team = initialize_team(
        this_game['gameData']['teams']['away'],
        this_game['liveData']['boxscore']['teams']['away'],
        this_game['gameData'],
    )

    home_team = initialize_team(
        this_game['gameData']['teams']['home'],
        this_game['liveData']['boxscore']['teams']['home'],
        this_game['gameData']
    )

    location = '{}, {}, {}'.format(
        this_game['gameData']['venue']['name'],
        this_game['gameData']['venue']['location']['city'],
        this_game['gameData']['venue']['location']['stateAbbrev']
    )

    start_date = None
    end_date = None
    if this_game['liveData']['plays'].get('allPlays'):
        first_play = this_game['liveData']['plays']['allPlays'][0]
        for play_event in first_play['playEvents']:
            if play_event['type'] == 'pitch':
                start_date = get_datetime(
                    play_event['startTime']
                )
                break

        end_date = get_datetime(
            this_game['liveData']['plays']['allPlays'][-1]['about']['endTime']
        )

    if start_date:
        game_str = '{:04d}-{:02d}-{:02d}-{}-{}{}'.format(
            int(start_date.astimezone(timezone('America/New_York')).year),
            int(start_date.astimezone(timezone('America/New_York')).month),
            int(start_date.astimezone(timezone('America/New_York')).day),
            away_team.abbreviation,
            home_team.abbreviation,
            this_game['gameData']['game']['id'][-2:]
        )
    else:
        game_str = '{}-{}{}'.format(
            away_team.abbreviation,
            home_team.abbreviation,
            this_game['gameData']['game']['id'][-2:]
        )

    game_obj = Game(home_team, away_team, location, game_str)
    game_obj.start_date = start_date
    game_obj.end_date = end_date

    if attendance_str:
        game_obj.attendance = int(attendance_str)

    if temperature_str:
        game_obj.temp = int(temperature_str)

    if weather_str:
        game_obj.weather = weather_str

    if start_datetime_str:
        game_obj.expected_start_datetime = get_datetime(start_datetime_str)

    return game_obj

def get_game_obj(game_dict):
    game = initialize_game(
        game_dict,
        game_dict.get('gameData', {}).get('gameInfo', {}).get(
            'attendance', ''),
        game_dict.get('gameData', {}).get('weather', {}).get(
            'temp', ''),
        game_dict.get('gameData', {}).get('weather', {}).get(
            'condition', ''),
        game_dict.get('gameData', {}).get('datetime', {}).get(
            'dateTime', '')
    )

    inning_dict_list = get_inning_dict_list(game_dict)
    set_game_inning_list(inning_dict_list, game)
    set_pitcher_wls_codes(game_dict, game)

    if game.home_team.batting_order_list_list[0] is None:
        game.home_team.batting_order_list_list = [[]] * 9

    if game.away_team.batting_order_list_list[0] is None:
        game.away_team.batting_order_list_list = [[]] * 9

    game.set_batting_box_score_dict()
    game.set_pitching_box_score_dict()
    game.set_team_stats()
    game.set_gametimes()

    est_time = (game.start_datetime if game.start_datetime
                else game.expected_start_datetime).astimezone(
                    timezone('America/New_York')
                )

    if ('Postponed' in game_dict.get('gameData', {}).get('status', {}).get(
            'detailedState', {}) or
            (est_time.hour == 23 and est_time.minute == 33)):
        game.is_postponed = True
    else:
        game.is_postponed = False

    return game
