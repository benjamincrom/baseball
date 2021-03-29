from datetime import datetime
from re import search, sub

from pytz import UTC

from baseball.baseball import (POSITION_CODE_DICT,
                               PlateAppearance,
                               Player,
                               PlayerAppearance,
                               Inning,
                               Team,
                               Game)

from baseball.baseball_events import (AUTOMATIC_BALL_POSITION,
                                      Pitch,
                                      Pickoff,
                                      RunnerAdvance,
                                      Substitution,
                                      Switch)


MLB_TEAM_CODE_DICT = {'LAA': 'ana',
                      'SEA': 'sea',
                      'BAL': 'bal',
                      'CLE': 'cle',
                      'CIN': 'cin',
                      'NYM': 'nyn',
                      'COL': 'col',
                      'LAD': 'lan',
                      'DET': 'det',
                      'TOR': 'tor',
                      'HOU': 'hou',
                      'OAK': 'oak',
                      'MIA': 'mia',
                      'ATL': 'atl',
                      'MIL': 'mil',
                      'CHC': 'chn',
                      'MIN': 'min',
                      'KC': 'kca',
                      'NYY': 'nya',
                      'TEX': 'tex',
                      'PHI': 'phi',
                      'WSH': 'was',
                      'PIT': 'pit',
                      'STL': 'sln',
                      'SD': 'sdn',
                      'ARI': 'ari',
                      'SF': 'sfn',
                      'CHW': 'cha',
                      'TB': 'tba',
                      'BOS': 'bos'}

POSITION_ABBREV_DICT = {'P': 1,
                        'C': 2,
                        '1B': 3,
                        '2B': 4,
                        '3B': 5,
                        'SS': 6,
                        'LF': 7,
                        'CF': 8,
                        'RF': 9,
                        'DH': 10}


def get_team_abbreviation(mlb_code):
    for abbreviation, this_mlb_code in MLB_TEAM_CODE_DICT.items():
        if mlb_code == this_mlb_code:
            return abbreviation

    raise ValueError('Invalid mlb code')

def get_datetime(tfs_zulu_str):
    if tfs_zulu_str:
        year = int(tfs_zulu_str[0:4])
        month = int(tfs_zulu_str[5:7])
        day = int(tfs_zulu_str[8:10])
        hour = int(tfs_zulu_str[11:13])
        minute = int(tfs_zulu_str[14:16])
        second = int(tfs_zulu_str[17:19])
        event_datetime = datetime(year, month, day, hour, minute, second,
                                  tzinfo=UTC)
    else:
        event_datetime = None

    return event_datetime

def process_pitch(event):
    pitch_description = event.get('des')
    pitch_type = event.get('pitch_type')
    pitch_datetime = get_datetime(event.get('tfs_zulu'))

    if (not event.get('x') or
            not event.get('y') or
            event.get('x') == 'None' or
            event.get('y') == 'None'):
        (pitch_x, pitch_y) = AUTOMATIC_BALL_POSITION
    else:
        pitch_x = float(event.get('x'))
        pitch_y = float(event.get('y'))

    pitch_position = (pitch_x, pitch_y)

    if event.get('start_speed'):
        pitch_speed = float(event.get('start_speed'))
    else:
        pitch_speed = None

    pitch_obj = Pitch(pitch_datetime,
                      pitch_description,
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

    pickoff_obj = Pickoff(pickoff_description,
                          pickoff_base,
                          pickoff_was_successful)

    return pickoff_obj

def process_runner_advance(event, game_obj):
    runner_id = int(event.get('id'))

    if runner_id in game_obj.away_team:
        runner = game_obj.away_team[runner_id]
    elif runner_id in game_obj.home_team:
        runner = game_obj.home_team[runner_id]
    else:
        raise ValueError('Runner ID not in player dict')

    start_base = event.get('start')
    end_base = event.get('end')
    run_description = event.get('event')
    runner_scored = (event.get('score') == 'T')
    run_earned = (event.get('earned') == 'T')
    is_rbi = (event.get('rbi') == 'T')

    runner_advance_obj = RunnerAdvance(run_description,
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

def parse_substitution(substitution_datetime, description, event_summary,
                       inning_half_str, game_obj):
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
          event_summary == 'Offensive sub' or
          event_summary == 'Offensive Substitution'):
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
    incoming_player = this_team[incoming_player_name]
    outgoing_player = this_team[outgoing_player_name]
    substitution_obj = Substitution(substitution_datetime,
                                    incoming_player,
                                    outgoing_player,
                                    batting_order,
                                    position_num)

    return this_team, substitution_obj

def get_position_number(position_str):
    if position_str in POSITION_CODE_DICT:
        position = POSITION_CODE_DICT[position_str]
    elif position_str in POSITION_ABBREV_DICT:
        position = POSITION_ABBREV_DICT[position_str]
    elif position_str == 'PH':
        position = 'PH'
    elif position_str == 'PR':
        position = 'PR'
    elif position_str == 'EH':
        position = 'EH'
    elif not position_str:
        position = None
    else:
        raise ValueError('Invalid Position')

    return position

def fix_description(input_str):
    match = search(r'[A-Z]\.\s+[A-Z]\.\s+', input_str)
    while match:
        index_start = match.start()
        index_end = match.end()
        string_start = input_str[:index_start]
        string_end = input_str[index_end:]
        string_middle = input_str[index_start:index_end]
        string_middle = sub(r'\.\s+', '', string_middle)
        input_str = (string_start + string_middle + ' ' + string_end)
        match = search(r'[A-Z]\.\s+[A-Z]\.\s+', input_str)

    match = search(r'[A-Z]\.\s+[A-Z]', input_str)
    while match:
        index_start = match.start()
        index_end = match.end()
        string_start = input_str[:index_start]
        string_middle = input_str[index_start:index_end].replace('.', '')
        string_end = input_str[index_end:]
        input_str = (string_start + string_middle + string_end).strip()
        match = search(r'[A-Z]\.\s+[A-Z]', input_str)

    input_str = sub(r'\.\s+', '. ', input_str)
    input_str = input_str.strip()

    return input_str

def process_at_bat(plate_appearance, event_list, game_obj, steal_description):
    (new_event_list,
     scoring_runners_list,
     runners_batted_in_list) = process_plate_appearance(plate_appearance,
                                                        game_obj)

    event_list += new_event_list
    plate_appearance_desc = fix_description(plate_appearance.get('des'))

    pitcher_id = int(plate_appearance.get('pitcher'))
    inning_outs = int(plate_appearance.get('o'))

    out_runner_supplemental_list = None
    pitcher = None
    for this_team in [game_obj.home_team, game_obj.away_team]:
        if pitcher_id in this_team:
            pitcher = this_team[pitcher_id]
        elif steal_description:
            out_runner_supplemental_list = (
                PlateAppearance.get_out_runners_list(steal_description,
                                                     this_team)
            )

    if not pitcher:
        raise ValueError('Batter ID not in player_dict')

    batter_id = int(plate_appearance.get('batter'))
    if batter_id in game_obj.home_team:
        batter = game_obj.home_team[batter_id]
        batting_team = game_obj.home_team
    elif batter_id in game_obj.away_team:
        batter = game_obj.away_team[batter_id]
        batting_team = game_obj.away_team
    else:
        raise ValueError('Batter ID not in player_dict')

    start_datetime = get_datetime(plate_appearance.get('end_tfs_zulu'))
    end_datetime = get_datetime(plate_appearance.get('end_tfs_zulu'))
    plate_appearance_summary = plate_appearance.get('event').strip()
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

    if out_runner_supplemental_list:
        plate_appearance_obj.out_runners_list += out_runner_supplemental_list

    return plate_appearance_obj

def process_substitution(substitution_obj, inning_num, inning_half_str,
                         next_batter_num, substituting_team):
    player_appearance_obj = PlayerAppearance(
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

    if not player_appearance_list:
        position_list = [batting_list[-1].position
                         for batting_list in batting_list_list]

        duplicate_position_set = set(
            [x for x in position_list if ((position_list.count(x) > 1) and (x not in ['PH', 'PR']))]
        )

        if duplicate_position_set:
            duplicate_position = [x for x in duplicate_position_set][0]
            duplicate_appearance_list = []
            for batting_list in batting_list_list:
                if batting_list[-1].position == duplicate_position:
                    duplicate_appearance_list.append(batting_list)

            first_player_start = int(
                '{}{}{}'.format(
                    duplicate_appearance_list[0][-1].start_inning_num,
                    int(duplicate_appearance_list[0][-1].start_inning_half == 'bottom'),
                    duplicate_appearance_list[0][-1].start_inning_batter_num,
                )
            )

            second_player_start = int(
                '{}{}{}'.format(
                    duplicate_appearance_list[1][-1].start_inning_num,
                    int(duplicate_appearance_list[1][-1].start_inning_half == 'bottom'),
                    duplicate_appearance_list[1][-1].start_inning_batter_num,
                )
            )

            if first_player_start < second_player_start:
                player_appearance_list = duplicate_appearance_list[0]
            else:
                player_appearance_list = duplicate_appearance_list[1]

    if not player_appearance_list:
        for this_appearance_list in batting_list_list:
            if (len(this_appearance_list) > 1 and
                    this_appearance_list[-2].player_obj.mlb_id == substitution_obj.outgoing_player.mlb_id):
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
    player_appearance_obj = PlayerAppearance(
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

def parse_switch_description(event_datetime, description, event_summary,
                             game_obj, inning_half_str):
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
        new_position = POSITION_CODE_DICT[position_str.split()[0]]
        player_name = description.split(' remains ')[0]
    elif 'switch from' in description:
        position_str = description.split(' switch from ')[1]
        position_str = position_str.split(' for ')[0]
        new_position_str = position_str.split(' to ')[1]
        new_position = POSITION_CODE_DICT[new_position_str.split()[0]]
        player_name = description.split(' for ')[1]
        player_name = player_name.strip(' .')
    else:
        raise ValueError('Invalid switch')

    player = switching_team[player_name]

    old_position = None
    for player_list in switching_team.batting_order_list_list:
        if player_list[-1].player_obj.mlb_id == player.mlb_id:
            old_position = player_list[-1].position

    for pitcher_appearance in switching_team.pitcher_list:
        if pitcher_appearance.player_obj.mlb_id == player.mlb_id:
            old_position = 1

    if not old_position:
        raise ValueError('Cannot find player\'s position')

    switch_obj = Switch(event_datetime, player, old_position, new_position,
                        new_batting_order)

    return switch_obj, switching_team

def get_sub_switch_steal_flags(event_summary, event_description):
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

    steal_flag = 'Steal' in event_summary or 'steal' in event_description

    return substitution_flag, switch_flag, steal_flag

def process_half_inning(baseball_half_inning, inning_half_str, game_obj):
    if inning_half_str != 'top' and inning_half_str != 'bottom':
        raise ValueError('Invalid inning half str.')

    plate_appearance_list = []
    event_list = []
    steal_description = None
    for event_container in baseball_half_inning:
        event_datetime = get_datetime(event_container.get('tfs_zulu'))
        event_description = event_container.get('des')
        event_summary = event_container.get('event')
        inning_num = len(game_obj.inning_list) + 1
        next_batter_num = len(plate_appearance_list) + 1
        if event_container.tag == 'action':
            (substitution_flag,
             switch_flag,
             steal_flag) = get_sub_switch_steal_flags(event_summary,
                                                      event_description)

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

            elif steal_flag:
                steal_description = event_description
        elif event_container.tag == 'atbat':
            if event_container.get('des'):
                plate_appearance_obj = process_at_bat(event_container, event_list,
                                                      game_obj, steal_description)

                plate_appearance_list.append(plate_appearance_obj)
                event_list = []
                steal_description = None
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

    return Player(player_xml.get('last'),
                  player_xml.get('first'),
                  int(player_xml.get('id')),
                  None,
                  None,
                  player_num)

def init_player_list(player_obj, position):
    return [PlayerAppearance(player_obj, position, 1, 'top', 1)]

def parse_name(batter):
    batter_name = batter.get('name_display_first_last')
    if search(r'\w\s+[A-Z]\.\s+', batter_name):
        batter_name = sub(r'\s[A-Z]\.\s+', ' ', batter_name)

    player_first_name, player_last_name = batter_name.split(' ', 1)

    return player_first_name, player_last_name

def initialize_team(team_name, team_code, batter_xml_list):
    this_team = Team(team_name, team_code)
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

            this_player = Player(player_last_name,
                                 player_first_name,
                                 player_id,
                                 player_obp,
                                 player_slg,
                                 None)

            this_team.append(this_player)
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

    this_inning_obj = Inning(top_half_appearance_list,
                             bottom_half_appearance_list)

    return this_inning_obj

def process_team_xml(game_obj, team_xml):
    away_team_xml, home_team_xml = [x for x in team_xml if x.tag == 'team']

    team_tuple_list = [(game_obj.away_team, away_team_xml),
                       (game_obj.home_team, home_team_xml)]

    for this_team, this_team_xml in team_tuple_list:
        for player_xml in this_team_xml:
            if player_xml.tag == 'player':
                player_id = int(player_xml.get('id'))

                if player_id in this_team:
                    this_player = this_team[player_id]

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
                        this_team.append(this_player)

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

    game_obj = Game(home_team, away_team, game_venue, boxscore_date)

    return (game_obj,
            away_pitcher_status_dict,
            home_pitcher_status_dict,
            away_starting_pitcher_id,
            home_starting_pitcher_id)

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
        PlayerAppearance(
            game.away_team[away_starting_pitcher_id],
            1, 1, 'top', 1
        )
    )

    game.home_team.pitcher_list.append(
        PlayerAppearance(
            game.home_team[home_starting_pitcher_id],
            1, 1, 'top', 1
        )
    )

def get_game_obj(boxscore_xml, team_xml, game_xml):
    (game,
     away_pitcher_status_dict,
     home_pitcher_status_dict,
     away_starting_pitcher_id,
     home_starting_pitcher_id) = initialize_game_object(boxscore_xml)

    if not away_starting_pitcher_id or not home_starting_pitcher_id:
        game = None
    else:
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
