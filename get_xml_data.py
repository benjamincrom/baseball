import datetime
import multiprocessing
import os
import re
import sys
import xml.etree.ElementTree

import pytz
import requests
import dateutil.parser

import baseball
import baseball_events
import constants

def get_list_of_lists(this_list, size):
    chunk_size = len(this_list) // size
    return [this_list[i:i+chunk_size]
            for i in range(0, len(this_list), chunk_size)]

def get_team_abbreviation(mlb_code):
    for abbreviation, this_mlb_code in constants.MLB_TEAM_CODE_DICT.items():
        if mlb_code == this_mlb_code:
            return abbreviation

    raise ValueError('Invalid mlb code')

def set_pitch_times(event, game_obj):
    if event.get('tfs_zulu'):
        tfs_zulu_str = event.get('tfs_zulu')
        year = int(tfs_zulu_str[0:4])
        month = int(tfs_zulu_str[5:7])
        day = int(tfs_zulu_str[8:10])
        hour = int(tfs_zulu_str[11:13])
        minute = int(tfs_zulu_str[14:16])
        second = int(tfs_zulu_str[17:19])
        event_datetime = datetime.datetime(year, month, day, hour, minute,
                                           second, tzinfo=pytz.UTC)

        if not game_obj.first_pitch_datetime:
            game_obj.first_pitch_datetime = event_datetime

        game_obj.last_pitch_datetime = event_datetime

def process_pitch(event):
    pitch_description = event.get('des')
    pitch_type = event.get('pitch_type')

    if not (event.get('x') and event.get('y')):
        (pitch_x, pitch_y) = constants.AUTOMATIC_BALL_POSITION
    else:
        pitch_x = float(event.get('x'))
        pitch_y = float(event.get('y'))

    pitch_position = (pitch_x, pitch_y)

    if event.get('start_speed'):
        pitch_speed = float(event.get('start_speed'))
    else:
        pitch_speed = None

    pitch_obj = baseball_events.Pitch(pitch_description,
                                      pitch_type,
                                      pitch_speed,
                                      pitch_position)

    return pitch_obj

def process_pickoff(event):
    pickoff_description = event.get('des')
    pickoff_base = pickoff_description.split()[-1]

    if (pickoff_description.split()[1] == 'Attempt' or
            pickoff_description.split()[1] == 'Error'):
        pickoff_was_successful = False
    elif len(pickoff_description.split()) == 2:
        pickoff_was_successful = True
    else:
        raise ValueError('Bad Pickoff description.')

    pickoff_obj = baseball_events.Pickoff(pickoff_description,
                                          pickoff_base,
                                          pickoff_was_successful)

    return pickoff_obj

def process_runner_advance(event, game_obj):
    runner_id = int(event.get('id'))

    if runner_id in game_obj.away_team.player_id_dict:
        runner = game_obj.away_team.player_id_dict[runner_id]
    elif runner_id in game_obj.home_team.player_id_dict:
        runner = game_obj.home_team.player_id_dict[runner_id]
    else:
        raise ValueError('Runner ID not in player dict')

    start_base = event.get('start')
    end_base = event.get('end')
    run_description = event.get('event')
    runner_scored = (event.get('score') == 'T')
    run_earned = (event.get('earned') == 'T')
    is_rbi = (event.get('rbi') == 'T')

    runner_advance_obj = baseball_events.RunnerAdvance(run_description,
                                                       runner,
                                                       start_base,
                                                       end_base,
                                                       runner_scored,
                                                       run_earned,
                                                       is_rbi)

    return runner_advance_obj

def process_plate_appearance(plate_appearance, game_obj):
    event_list = []
    scoring_runners_list = []
    runners_batted_in_list = []

    for event in plate_appearance:
        if event.tag == 'pitch':
            set_pitch_times(event, game_obj)
            pitch_obj = process_pitch(event)
            event_list.append(pitch_obj)
        elif event.tag == 'po':
            pickoff_obj = process_pickoff(event)
            event_list.append(pickoff_obj)
        elif event.tag == 'runner':
            runner_advance_obj = process_runner_advance(event, game_obj)
            event_list.append(runner_advance_obj)

            if runner_advance_obj.runner_scored:
                scoring_runners_list.append(runner_advance_obj.runner)

                if runner_advance_obj.is_rbi:
                    runners_batted_in_list.append(runner_advance_obj.runner)
        else:
            raise ValueError('Undefined event')

    return event_list, scoring_runners_list, runners_batted_in_list

def parse_substitution_description(description):
    if ('remains in game' in description and
            'leaves the game' in description):
        incoming_str, action_str, outgoing_str = description.split(', ')
        action_list = [action_str]
        player_list = [incoming_str.split(' remains')[0],
                       outgoing_str.split(' leaves')[0]]
    elif 'enters the batting order' in description:
        action_list = [description.split(', ')[1]]
        start_str = description.split(', ')[0]
        predicate_str = description.split(', ')[2]
        player_list = [
            start_str.split(' enters')[0],
            predicate_str.split(' leaves')[0]
        ]
    else:
        description = description.strip(' .')
        description = description.split(': ')[1]
        description_list = description.split(', ')

        player_list = description_list[0].split(' replaces ')
        action_list = description_list[1:]

    return player_list, action_list

def get_name_only(player_str):
    name_flag = False
    player_name = None

    for word in player_str.split():
        if name_flag:
            player_name += (' ' + word)
        elif word[0].isupper():
            player_name = word
            name_flag = True

    return player_name

def get_player_names(player_list):
    incoming_player_name = (
        player_list[0].replace(
            'Pinch-hitter ', ''
        ).replace(
            'Pinch hitter ', ''
        ).replace(
            'Pinch-runner ', ''
        ).replace(
            'Pinch runner ', ''
        ).replace(
            'Pitcher ', ''
        )
    )
    outgoing_player_name = get_name_only(player_list[1])

    return incoming_player_name.strip(), outgoing_player_name.strip()

def lookup_player(player_name, this_team):
    if player_name in this_team.player_name_dict:
        player = this_team.player_name_dict[player_name]
    else:
        player_name = re.sub(r' Jr$', '', player_name.strip(' .'))
        player_name = re.sub(r' Sr$', '', player_name.strip(' .'))
        player_name = re.sub(r' II$', '', player_name.strip())
        player_name = re.sub(r' III$', '', player_name.strip())
        player_name = re.sub(r' IV$', '', player_name.strip())

        player_name = baseball.strip_suffixes(player_name.strip())
        first_name_initial = player_name[0]
        last_name = player_name.split()[-1]

        player = this_team.player_last_name_dict[first_name_initial + last_name]

    return player

def parse_substitution(description, event_summary, inning_half_str, game_obj):
    player_list, action_list = parse_substitution_description(description)
    incoming_player_name, outgoing_player_name = get_player_names(player_list)
    batting_order, position_str = None, None

    for item in action_list:
        if 'batting' in item:
            batting_order_str = item.replace('batting ', '')[:-2]
            batting_order = int(batting_order_str)
        elif 'replacing' in item:
            outgoing_player_name = item.replace('replacing ', '').strip()
        elif 'playing' in item:
            position_str = item.replace('playing ', '').split()[0].strip()

    position_num = get_position_number(position_str)

    if (event_summary == 'Pitching Substitution' or
            event_summary == 'Defensive Sub' or
            event_summary == 'Defensive sub'):
        if inning_half_str == 'top':
            this_team = game_obj.home_team
        else:
            this_team = game_obj.away_team
    elif (event_summary == 'Offensive Sub' or
          event_summary == 'Offensive sub'):
        if inning_half_str == 'top':
            this_team = game_obj.away_team
        else:
            this_team = game_obj.home_team
    else:
        raise ValueError('Invalid Substitution event summary')

    if ('Pinch-hitter ' in player_list[0] or
            'Pinch hitter' in player_list[0]):
        position_num = 'PH'
    elif ('Pinch-runner ' in player_list[0] or
          'Pinch runner' in player_list[0]):
        position_num = 'PR'
    elif event_summary == 'Pitching Substitution':
        position_num = 1

    outgoing_player_name = get_name_only(outgoing_player_name)

    incoming_player = lookup_player(incoming_player_name, this_team)
    outgoing_player = lookup_player(outgoing_player_name, this_team)
    substitution_obj = baseball_events.Substitution(incoming_player,
                                                    outgoing_player,
                                                    batting_order,
                                                    position_num)

    return this_team, substitution_obj

def get_position_number(position_str):
    if position_str in constants.POSITION_CODE_DICT:
        position = constants.POSITION_CODE_DICT[position_str]
    elif position_str in constants.POSITION_ABBREV_DICT:
        position = constants.POSITION_ABBREV_DICT[position_str]
    elif position_str == 'PH':
        position = 'PH'
    elif position_str == 'PR':
        position = 'PR'
    elif not position_str:
        position = None
    else:
        raise ValueError('Invalid Position')

    return position

def get_out_runners_list(team, description):
    description = baseball.strip_suffixes(description)
    description = baseball.fix_initials(description)

    runner_name_list = re.findall(
        (r'([A-Z][\w\'-]+\s+(?:[A-Z,a-z][\w\'-]+\s+)?'
         r'(?:[A-Z,a-z][\w\'-]+\s+)?[A-Z][\w\'-]+)\s+'
         r'(?:out at|(?:was )?picked off and caught stealing|'
         r'(?:was )?caught stealing|(?:was )?picked off|'
         r'(?:was )?doubled off)'
         r' +(\w+)'),
        description
    )

    runner_tuple_list = []
    for name, base in runner_name_list:
        if re.findall(re.escape(name) + r' (?:was )?doubled off', description):
            base = constants.INCREMENT_BASE_DICT[base]

        runner_tuple_list.append(
            (lookup_player(name, team), base)
        )

    return runner_tuple_list

def process_at_bat(plate_appearance, event_list, game_obj):
    (new_event_list,
     scoring_runners_list,
     runners_batted_in_list) = process_plate_appearance(plate_appearance,
                                                        game_obj)

    event_list += new_event_list

    plate_appearance_desc = plate_appearance.get('des')
    pitcher_id = int(plate_appearance.get('pitcher'))
    inning_outs = int(plate_appearance.get('o'))

    pitcher = None
    for this_team in [game_obj.home_team, game_obj.away_team]:
        if pitcher_id in this_team.player_id_dict:
            pitcher = this_team.player_id_dict[pitcher_id]

    if not pitcher:
        raise ValueError('Batter ID not in player_dict')

    batter_id = int(plate_appearance.get('batter'))

    if batter_id in game_obj.home_team.player_id_dict:
        batter = game_obj.home_team.player_id_dict[batter_id]
        batting_team = game_obj.home_team
    elif batter_id in game_obj.away_team.player_id_dict:
        batter = game_obj.away_team.player_id_dict[batter_id]
        batting_team = game_obj.away_team
    else:
        raise ValueError('Batter ID not in player_dict')

    plate_appearance_summary = plate_appearance.get('event')
    out_runners_list = get_out_runners_list(batting_team, plate_appearance_desc)

    plate_appearance_obj = baseball.PlateAppearance(plate_appearance_desc,
                                                    plate_appearance_summary,
                                                    pitcher,
                                                    batter,
                                                    inning_outs,
                                                    out_runners_list,
                                                    scoring_runners_list,
                                                    runners_batted_in_list,
                                                    event_list)

    return plate_appearance_obj

def process_substitution(substitution_obj, inning_num, inning_half_str,
                         next_batter_num, substituting_team):
    player_appearance_obj = baseball.PlayerAppearance(
        substitution_obj.incoming_player,
        substitution_obj.position,
        inning_num,
        inning_half_str,
        next_batter_num
    )

    batting_list_list = substituting_team.batting_order_list_list
    player_appearance_list = None
    processed_flag = False

    if substitution_obj.batting_order:
        batting_index = substitution_obj.batting_order - 1
        player_appearance_list = batting_list_list[batting_index]
    else:
        for this_appearance_list in batting_list_list:
            if (this_appearance_list[-1].player_obj.mlb_id ==
                    substitution_obj.outgoing_player.mlb_id):
                player_appearance_list = this_appearance_list

    if player_appearance_list:
        processed_flag = True
        set_player_position_from_list(player_appearance_obj,
                                      player_appearance_list)

        final_appearance = player_appearance_list[-1]
        final_appearance.end_inning_num = inning_num
        final_appearance.end_inning_half = inning_half_str
        final_appearance.end_inning_batter_num = next_batter_num
        player_appearance_list.append(player_appearance_obj)

    if player_appearance_obj.position == 1:
        processed_flag = True
        pitching_appearance_list = substituting_team.pitcher_list
        final_appearance = pitching_appearance_list[-1]
        final_appearance.end_inning_num = inning_num
        final_appearance.end_inning_half = inning_half_str
        final_appearance.end_inning_batter_num = next_batter_num
        pitching_appearance_list.append(player_appearance_obj)

    if not processed_flag:
        raise ValueError('Invalid substitution.')

def process_switch(switch_obj, inning_num, inning_half_str,
                   next_batter_num, switching_team):
    player_appearance_obj = baseball.PlayerAppearance(
        switch_obj.player,
        switch_obj.new_position_num,
        inning_num,
        inning_half_str,
        next_batter_num
    )

    batting_list_list = switching_team.batting_order_list_list
    old_player_appearance_list = None
    for this_appearance_list in batting_list_list:
        if (this_appearance_list[-1].player_obj.mlb_id ==
                switch_obj.player.mlb_id):
            old_player_appearance_list = this_appearance_list

    if not old_player_appearance_list:
        if (switching_team.pitcher_list[-1].player_obj.mlb_id ==
                switch_obj.player.mlb_id):
            old_player_appearance_list = switching_team.pitcher_list

    if not old_player_appearance_list:
        raise ValueError('Invalid player switch')

    final_appearance = old_player_appearance_list[-1]
    final_appearance.end_inning_num = inning_num
    final_appearance.end_inning_half = inning_half_str
    final_appearance.end_inning_batter_num = next_batter_num

    if switch_obj.new_batting_order:
        new_player_appearance_list = batting_list_list[
            switch_obj.new_batting_order - 1
        ]

        new_player_appearance_list.append(player_appearance_obj)
    else:
        old_player_appearance_list.append(player_appearance_obj)

    if player_appearance_obj.position == 1:
        switching_team.pitcher_list.append(player_appearance_obj)

def parse_switch_description(description, event_summary, game_obj,
                             inning_half_str):
    if 'Substitution: ' in description:
        description = description.split('Substitution: ')[1]

    if 'Defensive' in event_summary:
        if inning_half_str == 'top':
            switching_team = game_obj.home_team
        else:
            switching_team = game_obj.away_team
    elif 'Offensive' in event_summary:
        if inning_half_str == 'top':
            switching_team = game_obj.away_team
        else:
            switching_team = game_obj.home_team

    if ', batting' in description:
        description, batting_str = description.split(', batting')
        new_batting_order = int(batting_str.strip()[0])
    else:
        new_batting_order = None

    if 'remains' in description:
        position_str = description.split(' as the ')[1].strip(' .')
        new_position = constants.POSITION_CODE_DICT[position_str.split()[0]]
        player_name = description.split(' remains ')[0]
    elif 'switch from' in description:
        position_str = description.split(' switch from ')[1]
        position_str = position_str.split(' for ')[0]
        new_position_str = position_str.split(' to ')[1]
        new_position = constants.POSITION_CODE_DICT[new_position_str.split()[0]]
        player_name = description.split(' for ')[1]
        player_name = player_name.strip(' .')
    else:
        raise ValueError('Invalid switch')

    player = lookup_player(player_name, switching_team)

    old_position = None
    for player_list in switching_team.batting_order_list_list:
        if player_list[-1].player_obj.mlb_id == player.mlb_id:
            old_position = player_list[-1].position

    for pitcher_appearance in switching_team.pitcher_list:
        if pitcher_appearance.player_obj.mlb_id == player.mlb_id:
            old_position = 1

    if not old_position:
        raise ValueError('Cannot find player\'s position')

    switch_obj = baseball_events.Switch(player, old_position, new_position,
                                        new_batting_order)

    return switch_obj, switching_team

def get_subsitution_switch_flags(event_summary, event_description):
    substitution_flag = (
        ('Sub' in event_summary or 'sub' in event_summary) and
        'remains in the game' not in event_description and
        'Umpire' not in event_description and
        'umpire' not in event_description and
        'is now pitching' not in event_description and
        'Dropped foul pop error' not in event_description
    )

    switch_flag = (
        ('Switch' in event_summary or
         'remains in the game' in event_description) and
        'is now pitching' not in event_description and
        'Dropped foul pop error' not in event_description
    )

    return substitution_flag, switch_flag

def process_half_inning(baseball_half_inning, inning_half_str, game_obj):
    if inning_half_str != 'top' and inning_half_str != 'bottom':
        raise ValueError('Invalid inning half str.')

    plate_appearance_list = []
    event_list = []
    for event_container in baseball_half_inning:
        event_description = event_container.get('des')
        event_summary = event_container.get('event')
        inning_num = len(game_obj.inning_list) + 1
        next_batter_num = len(plate_appearance_list) + 1
        if event_container.tag == 'atbat':
            plate_appearance_obj = process_at_bat(event_container, event_list,
                                                  game_obj)

            plate_appearance_list.append(plate_appearance_obj)
            event_list = []
        elif event_container.tag == 'action':
            substitution_flag, switch_flag = get_subsitution_switch_flags(
                event_summary,
                event_description
            )

            if substitution_flag:
                (substituting_team,
                 substitution_obj) = parse_substitution(event_description,
                                                        event_summary,
                                                        inning_half_str,
                                                        game_obj)

                event_list.append(substitution_obj)
                process_substitution(substitution_obj, inning_num,
                                     inning_half_str, next_batter_num,
                                     substituting_team)
            elif switch_flag:
                (switch_obj,
                 switching_team) = parse_switch_description(event_description,
                                                            event_summary,
                                                            game_obj,
                                                            inning_half_str)

                event_list.append(switch_obj)
                process_switch(switch_obj, inning_num, inning_half_str,
                               next_batter_num, switching_team)
        else:
            raise ValueError('Unexpected event container tag')

    return plate_appearance_list

def set_player_position_from_list(player_appearance_obj, appearance_list):
    if not player_appearance_obj.position:
        for previous_appearance in reversed(appearance_list):
            if previous_appearance.position != 'PH':
                player_appearance_obj.position = previous_appearance.position
                break

    if not player_appearance_obj.position:
        raise ValueError('Invalid substitution: no position')

def create_player(player_xml):
    if (player_xml.get('num') and
            player_xml.get('num') != '--' and
            player_xml.get('num') != '-' and
            player_xml.get('num') != 'null'):
        player_num = int(player_xml.get('num'))
    else:
        player_num = None

    return baseball.Player(player_xml.get('last'),
                           player_xml.get('first'),
                           int(player_xml.get('id')),
                           None,
                           None,
                           player_num)

def init_player_list(player_obj, position):
    return [baseball.PlayerAppearance(player_obj, position, 1, 'top', 1)]

def parse_name(batter):
    batter_name = batter.get('name_display_first_last')
    if re.search(r'\w\s+[A-Z]\.\s+', batter_name):
        batter_name = re.sub(r'\s[A-Z]\.\s+', ' ', batter_name)

    player_first_name, player_last_name = batter_name.split(' ', 1)

    return player_first_name, player_last_name

def initialize_team(team_name, team_code, batter_xml_list):
    this_team = baseball.Team(team_name, team_code)
    for batter in batter_xml_list:
        if batter.tag == 'batter':
            player_id = int(batter.get('id'))
            if batter.get('obp'):
                player_obp = float(batter.get('obp'))
            else:
                player_obp = None

            if batter.get('slg'):
                player_slg = float(batter.get('slg'))
            else:
                player_slg = None

            player_position_str = batter.get('pos').split('-')[0]
            player_position_num = get_position_number(player_position_str)
            player_first_name, player_last_name = parse_name(batter)
            if batter.get('bo'):
                player_order = int(batter.get('bo')[0])
            else:
                player_order = None

            this_player = baseball.Player(player_last_name,
                                          player_first_name,
                                          player_id,
                                          player_obp,
                                          player_slg,
                                          None)

            add_player_to_team_dictionaries(this_team, this_player)
            this_player_appearance_list = init_player_list(this_player,
                                                           player_position_num)

            if player_order:
                if not this_team.batting_order_list_list[player_order - 1]:
                    this_team.batting_order_list_list[player_order - 1] = (
                        this_player_appearance_list
                    )

    return this_team

def process_inning_xml(baseball_inning, game_obj):
    top_half_inning = baseball_inning[0]
    top_half_appearance_list = process_half_inning(top_half_inning,
                                                   'top',
                                                   game_obj)

    if len(baseball_inning) > 1:
        bottom_half_inning = baseball_inning[1]
        bottom_half_appearance_list = process_half_inning(bottom_half_inning,
                                                          'bottom',
                                                          game_obj)
    else:
        bottom_half_appearance_list = None

    this_inning_obj = baseball.Inning(top_half_appearance_list,
                                      bottom_half_appearance_list)

    return this_inning_obj

def add_player_to_team_dictionaries(this_team, this_player):
    last_name = re.sub(
        r' Jr$', '', this_player.last_name.strip('. ').replace(',', '')
    )
    last_name = re.sub(r' Sr$', '', last_name.strip('. ').replace(',', ''))
    last_name = re.sub(r' II$', '', last_name.strip())
    last_name = re.sub(r' III$', '', last_name.strip())
    last_name = re.sub(r' IV$', '', last_name.strip())
    last_name = re.sub(r' St\. ', ' St ', last_name.strip())

    if ' ' in last_name:
        last_name = last_name.split()[1]

    this_team.player_id_dict[this_player.mlb_id] = this_player

    this_team.player_name_dict[this_player.full_name()] = this_player
    this_team.player_last_name_dict[this_player.first_name[0] + last_name] = (
        this_player
    )

def process_team_xml(game_obj, team_xml):
    away_team_xml, home_team_xml = [x for x in team_xml if x.tag == 'team']

    team_tuple_list = [(game_obj.away_team, away_team_xml),
                       (game_obj.home_team, home_team_xml)]

    for this_team, this_team_xml in team_tuple_list:
        for player_xml in this_team_xml:
            if player_xml.tag == 'player':
                player_id = int(player_xml.get('id'))

                if player_id in this_team.player_id_dict:
                    this_player = this_team.player_id_dict[player_id]

                    if (player_xml.get('num') and
                            player_xml.get('num') != '--' and
                            player_xml.get('num') != 'null' and
                            player_xml.get('num') != ' '):
                        this_player.number = int(player_xml.get('num'))
                    else:
                        this_player.number = ''

                    if (player_xml.get('era') is not None and
                            '-' not in player_xml.get('era')):
                        this_player.era = float(player_xml.get('era'))
                    else:
                        this_player.era = None
                else:
                    if (player_xml.get('id') and
                            player_xml.get('last') and
                            player_xml.get('first')):
                        this_player = create_player(player_xml)
                        add_player_to_team_dictionaries(this_team, this_player)

def initialize_game_object(boxscore_xml):
    game_venue = boxscore_xml.get('venue_name')
    home_code = get_team_abbreviation(boxscore_xml.get('home_team_code'))
    home_name = boxscore_xml.get('home_fname')
    away_code = get_team_abbreviation(boxscore_xml.get('away_team_code'))
    away_name = boxscore_xml.get('away_fname')
    boxscore_date = boxscore_xml.get('date')
    home_pitcher_status_dict = {}
    away_pitcher_status_dict = {}
    home_starting_pitcher_id = None
    away_starting_pitcher_id = None

    for item in boxscore_xml:
        if item.tag == 'batting':
            if item.get('team_flag') == 'away':
                away_team = initialize_team(away_name, away_code, item)
            elif item.get('team_flag') == 'home':
                home_team = initialize_team(home_name, home_code, item)
            else:
                raise ValueError('Invalid team flag')
        elif item.tag == 'pitching':
            if item.get('team_flag') == 'away':
                for pitcher_xml in item:
                    pitcher_id = int(pitcher_xml.get('id'))
                    if not away_starting_pitcher_id:
                        away_starting_pitcher_id = pitcher_id

                    note = pitcher_xml.get('note')
                    if note:
                        away_pitcher_status_dict[pitcher_id] = (
                            note.split('(')[1].split(',')[0]
                        )
                    else:
                        away_pitcher_status_dict[pitcher_id] = ''
            elif item.get('team_flag') == 'home':
                for pitcher_xml in item:
                    pitcher_id = int(pitcher_xml.get('id'))
                    if not home_starting_pitcher_id:
                        home_starting_pitcher_id = pitcher_id

                    note = pitcher_xml.get('note')
                    if note:
                        home_pitcher_status_dict[pitcher_id] = (
                            note.split('(')[1].split(',')[0]
                        )
                    else:
                        home_pitcher_status_dict[pitcher_id] = ''

    game_obj = baseball.Game(home_team, away_team, game_venue, boxscore_date)

    return (game_obj,
            away_pitcher_status_dict,
            home_pitcher_status_dict,
            away_starting_pitcher_id,
            home_starting_pitcher_id)

def get_game_xml_data(date, away_team_code, home_team_code, game_number):
    request_url_base = constants.MLB_URL_PATTERN.format(
        year=date.year,
        month=str(date.month).zfill(2),
        day=str(date.day).zfill(2),
        away_mlb_code=constants.MLB_TEAM_CODE_DICT[away_team_code],
        home_mlb_code=constants.MLB_TEAM_CODE_DICT[home_team_code],
        game_number=game_number
    )

    boxscore_request_text = requests.get(
        request_url_base + constants.BOXSCORE_SUFFIX
    ).text

    if boxscore_request_text == 'GameDay - 404 Not Found':
        boxscore_raw_xml, team_raw_xml, game_raw_xml = None, None, None
    else:
        boxscore_raw_xml = xml.etree.ElementTree.fromstring(
            boxscore_request_text
        )

        team_raw_xml = xml.etree.ElementTree.fromstring(
            requests.get(request_url_base + constants.PLAYERS_SUFFIX).text
        )

        game_raw_xml = xml.etree.ElementTree.fromstring(
            requests.get(request_url_base + constants.GAME_SUFFIX).text
        )

    return boxscore_raw_xml, team_raw_xml, game_raw_xml

def set_pitcher_wls_codes(game, away_pitcher_status_dict,
                          home_pitcher_status_dict):
    team_tuple_list = [(game.home_team.pitcher_list, home_pitcher_status_dict),
                       (game.away_team.pitcher_list, away_pitcher_status_dict)]

    for pitcher_list, pitcher_status_dict in team_tuple_list:
        for pitcher_appearance in pitcher_list:
            pitcher_id = pitcher_appearance.player_obj.mlb_id

            if pitcher_id in pitcher_status_dict:
                pitcher_appearance.pitcher_credit_code = (
                    pitcher_status_dict[pitcher_id]
                )

def set_starting_pitchers(game, away_starting_pitcher_id,
                          home_starting_pitcher_id):
    game.away_team.pitcher_list.append(
        baseball.PlayerAppearance(
            game.away_team.player_id_dict[away_starting_pitcher_id],
            1, 1, 'top', 1
        )
    )

    game.home_team.pitcher_list.append(
        baseball.PlayerAppearance(
            game.home_team.player_id_dict[home_starting_pitcher_id],
            1, 1, 'top', 1
        )
    )

def get_game_obj(boxscore_xml, team_xml, game_xml):
    (game,
     away_pitcher_status_dict,
     home_pitcher_status_dict,
     away_starting_pitcher_id,
     home_starting_pitcher_id) = initialize_game_object(boxscore_xml)

    process_team_xml(game, team_xml)

    set_starting_pitchers(game,
                          away_starting_pitcher_id,
                          home_starting_pitcher_id)

    for inning_xml in game_xml:
        game.inning_list.append(
            process_inning_xml(inning_xml, game)
        )

    set_pitcher_wls_codes(game,
                          away_pitcher_status_dict,
                          home_pitcher_status_dict)

    game.set_batting_box_score_dict()
    game.set_pitching_box_score_dict()
    game.set_team_stats()
    game.set_gametimes()

    return game

def get_filename_list(start_date_str, end_date_str, input_path):
    filename_list = []
    start_date = dateutil.parser.parse(start_date_str)
    end_date = dateutil.parser.parse(end_date_str)
    day_delta = datetime.timedelta(days=1)
    this_date = start_date
    while this_date < end_date + day_delta:
        year = str(this_date.year)
        month = str(this_date.month).zfill(2)
        day = str(this_date.day).zfill(2)
        filename = '{}/{}/month_{}/day_{}/'.format(input_path, year, month, day)
        if os.path.isdir(filename):
            file_list = os.listdir(filename)
            if file_list:
                for subfile in file_list:
                    if subfile.startswith('gid_'):
                        away_code, home_code, game_num = subfile.split('_')[-3:]
                        away_code = away_code[:-3]
                        home_code = home_code[:-3]
                        away_team, home_team = None, None
                        for key, value in constants.MLB_TEAM_CODE_DICT.items():
                            if value == away_code:
                                away_team = key

                            if value == home_code:
                                home_team = key

                        if away_team and home_team:
                            output_name = (
                                '-'.join([year, month, day, away_team,
                                          home_team, game_num])
                            )

                            subfolder_name = filename + subfile + '/'
                            if os.listdir(subfolder_name):
                                boxscore_filename = (
                                    subfolder_name + 'boxscore.xml'
                                )
                                player_filename = subfolder_name + 'players.xml'
                                inning_filename = (
                                    subfolder_name + 'inning/inning_all.xml'
                                )

                                filename_list.append((output_name,
                                                      boxscore_filename,
                                                      player_filename,
                                                      inning_filename))

        this_date += day_delta

    return filename_list

def get_game_list_from_files(start_date_str, end_date_str, input_dir):
    if not os.path.exists(input_dir):
        raise ValueError('Invalid input directory')

    input_path = os.path.abspath(input_dir)
    manager = multiprocessing.Manager()
    return_queue = manager.Queue()
    filename_list = get_filename_list(start_date_str, end_date_str, input_path)
    list_of_filename_lists = get_list_of_lists(filename_list, 16)
    job_list = []
    for filename_list in list_of_filename_lists:
        process = multiprocessing.Process(
            target=get_game_sublist,
            args=(filename_list, return_queue)
        )

        job_list.append(process)
        process.start()

    for job in job_list:
        job.join()

    game_list = []
    while not return_queue.empty():
        game_list.extend(return_queue.get())

    return game_list

def get_game_sublist(filename_list, return_queue):
    game_sublist = []
    for _, boxscore, player, inning in filename_list:
        if (os.path.isfile(boxscore) and
                os.path.isfile(player) and
                os.path.isfile(inning)):
            boxscore_raw = open(boxscore, 'r', encoding='utf-8').read()
            boxscore_xml = xml.etree.ElementTree.fromstring(boxscore_raw)
            player_raw = open(player, 'r', encoding='utf-8').read()
            player_xml = xml.etree.ElementTree.fromstring(player_raw)
            inning_raw = open(inning, 'r', encoding='utf-8').read()
            inning_xml = xml.etree.ElementTree.fromstring(inning_raw)

            this_game = get_game_obj(boxscore_xml, player_xml, inning_xml)
            game_sublist.append(this_game)

    return_queue.put(game_sublist)

def generate_from_files(start_date_str, end_date_str, input_dir):
    game_list = get_game_list_from_files(start_date_str,
                                         end_date_str,
                                         input_dir)

    for game in game_list:
        print(game)

def get_game_from_url(date_str, away_code, home_code, game_num):
    formatted_date_str = get_formatted_date_str(date_str)
    date = dateutil.parser.parse(formatted_date_str)
    boxscore_xml, team_xml, game_xml = get_game_xml_data(date,
                                                         away_code,
                                                         home_code,
                                                         game_num)

    if boxscore_xml:
        this_game = get_game_obj(boxscore_xml, team_xml, game_xml)
    else:
        this_game = None

    return this_game

def generate_from_url(date_str, away_code, home_code, game_num):
    this_game = get_game_from_url(date_str, away_code, home_code, game_num)
    if this_game:
        print(this_game)
        status = True
    else:
        print('No data found for {} {} {} {}'.format(date_str,
                                                     away_code,
                                                     home_code,
                                                     game_num))

        status = False

    return status

def get_formatted_date_str(input_date_str):
    this_date = dateutil.parser.parse(input_date_str)
    this_date_str = '{}-{}-{}'.format(str(this_date.year),
                                      str(this_date.month).zfill(2),
                                      str(this_date.day).zfill(2))

    return this_date_str

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(constants.GET_XML_USAGE_STR)
        exit()
    if sys.argv[1] == 'files' and len(sys.argv) == 5:
        generate_from_files(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'url' and len(sys.argv) == 6:
        generate_from_url(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print(constants.GET_XML_USAGE_STR)
