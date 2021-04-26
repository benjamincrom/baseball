from collections import OrderedDict
from json import dumps
from textwrap import TextWrapper
from re import search, sub, findall, escape

from pytz import timezone

from baseball.baseball_events import RunnerAdvance
from baseball.generate_svg import get_game_svg_str
from baseball.stats import (get_all_pitcher_stats,
                            get_all_batter_stats,
                            get_box_score_total,
                            get_team_stats,
                            get_half_inning_stats)

POSITION_CODE_DICT = {'pitcher': 1,
                      'catcher': 2,
                      'first': 3,
                      'second': 4,
                      'third': 5,
                      'shortstop': 6,
                      'left': 7,
                      'center': 8,
                      'right': 9,
                      'designated': 10,
                      '1B': 3,
                      '2B': 4,
                      '3B': 5,
                      'SS': 6,
                      'P': 1,
                      'C': 2,
                      'LF': 7,
                      'CF': 8,
                      'RF': 9}

ON_BASE_SUMMARY_DICT = {'Single': '1B',
                        'Double': '2B',
                        'Triple': '3B',
                        'Hit By Pitch': 'HBP',
                        'Home Run': 'HR',
                        'Walk': 'BB',
                        'Intent Walk': 'IBB'}

PLAY_CODE_ORDERED_DICT = OrderedDict([
    ('picks off', 'PO'),
    ('caught stealing', 'CS'),
    ('wild pitch', 'WP'),
    ('passed ball', 'PB'),
    ('balk', 'BLK'),
    ('steals', 'S'),
    ('fan interference', 'FI'),
    ('catcher interference', 'CI'),
    ('error', 'E'),
    ('ground', 'G'),
    ('grand slam', 'HR'),
    ('homers', 'HR'),
    ('pop', 'P'),
    ('line', 'L'),
    ('fly', 'F'),
    ('flies', 'F'),
    ('sacrifice fly', 'SF'),
    ('hit by pitch', 'HBP'),
    ('bunt', 'B'),
    ('sacrifice bunt', 'SH'),
    ('walks', 'BB'),
    ('intentionally walks', 'IBB'),
    ('called out on strikes', 'ꓘ'),
    ('strikes out', 'K'),
    ('choice', 'FC')
])

NO_HIT_CODE_LIST = ['K', 'ꓘ', 'BB', 'IBB']

BASE_PLUS_ONE_DICT = {'': '1st',
                      '1B': '2nd',
                      '2B': '3rd',
                      '3B': 'home'}

INCREMENT_BASE_DICT = {'1st': '2nd',
                       '2nd': '3rd',
                       '3rd': 'home'}

STADIUM_TIMEZONE_DICT = {
    'Fenway Park': 'America/New_York',
    'George M. Steinbrenner Field': 'America/New_York',
    'Yankee Stadium': 'America/New_York',
    'Roger Dean Stadium': 'America/New_York',
    'Joker Marchant Stadium': 'America/New_York',
    'JetBlue Park': 'America/New_York',
    'Citi Field': 'America/New_York',
    'LECOM Park': 'America/New_York',
    'First Data Field': 'America/New_York',
    'The Ballpark of the Palm Beaches': 'America/New_York',
    'Citizens Bank Park': 'America/New_York',
    'Spectrum Field': 'America/New_York',
    'Oriole Park': 'America/New_York',
    'Nationals Park': 'America/New_York',
    'Champion Stadium': 'America/New_York',
    'Truist Park': 'America/New_York',
    'Tropicana Field': 'America/New_York',
    'Marlins Park': 'America/New_York',
    'Rogers Centre': 'America/New_York',
    'PNC Park': 'America/New_York',
    'Progressive Field': 'America/New_York',
    'Comerica Park': 'America/New_York',
    'Great American Ball Park': 'America/New_York',
    'Miller Park': 'America/Chicago',
    'Wrigley Field': 'America/Chicago',
    'Guaranteed Rate Field': 'America/Chicago',
    'Busch Stadium': 'America/Chicago',
    'Target Field': 'America/Chicago',
    'Globe Life Field': 'America/Chicago',
    'Minute Maid Park': 'America/Chicago',
    'Kauffman Stadium': 'America/Chicago',
    'American Family Field': 'America/Chicago',
    'Coors Field': 'America/Denver',
    'Chase Field': 'America/Denver',
    'Safeco Field': 'America/Los_Angeles',
    'AT&T Park': 'America/Los_Angeles',
    'Oakland-Alameda County Coliseum': 'America/Los_Angeles',
    'Oakland Coliseum': 'America/Los_Angeles',
    'Angel Stadium': 'America/Los_Angeles',
    'Oracle Park': 'America/Los_Angeles',
    'Dodger Stadium': 'America/Los_Angeles',
    'Petco Park': 'America/Los_Angeles',
    'T-Mobile Park': 'America/Los_Angeles'
}

EASTERN_TIMEZONE_STR = 'America/New_York'

def strip_this_suffix(pattern, suffix, input_str):
    match = search(pattern, input_str)
    while match:
        start = match.start()
        end = match.end()
        str_beginning = input_str[:start]
        str_middle = sub(suffix, '.', input_str[start:end])
        str_end = input_str[end:]
        input_str = str_beginning + str_middle + str_end
        match = search(pattern, input_str)

    input_str = sub(suffix, '', input_str)

    return input_str.strip()

def strip_suffixes(input_str):
    input_str = strip_this_suffix(r' Jr\.\s+[A-Z]', r' Jr\.', input_str)
    input_str = strip_this_suffix(r' Sr\.\s+[A-Z]', r' Sr\.', input_str)
    input_str = sub(r' II', '', input_str)
    input_str = sub(r' III', '', input_str)
    input_str = sub(r' IV', '', input_str)
    input_str = sub(r' St\. ', ' St ', input_str)

    initials_match = findall(r'([A-Z]\.[A-Z]\.? )', input_str)
    while initials_match:
        new_initials = initials_match[0].replace('.', '')
        input_str = sub(initials_match[0], new_initials, input_str, 1)
        initials_match = findall(r'([A-Z]\.[A-Z]\.? )', input_str)

    return input_str


class PlayerAppearance:
    def __init__(self, player_obj, position, start_inning_num,
                 start_inning_half, start_inning_batter_num):
        self.player_obj = player_obj
        self.position = position
        self.start_inning_num = start_inning_num
        self.start_inning_half = start_inning_half
        self.start_inning_batter_num = start_inning_batter_num

        self.end_inning_num = None
        self.end_inning_half = None
        self.end_inning_batter_num = None
        self.pitcher_credit_code = None

    def _asdict(self):
        return (
            {'player_obj': self.player_obj._asdict(),
             'position': self.position,
             'start_inning_num': self.start_inning_num,
             'start_inning_half': self.start_inning_half,
             'start_inning_batter_num': self.start_inning_batter_num,
             'end_inning_num': self.end_inning_num,
             'end_inning_half': self.end_inning_half,
             'end_inning_batter_num': self.end_inning_batter_num,
             'pitcher_credit_code': self.pitcher_credit_code}
        )

    def __repr__(self):
        start_inning_str = '{}-{}'.format(self.start_inning_num,
                                          self.start_inning_half,)

        return_str = '{}\n'.format(str(self.player_obj))

        if self.player_obj.era is not None:
            return_str += '    {}\n'.format(self.player_obj.pitching_stats())

        return_str += (
            '    {}\n'
            '    Entered:     {:12} before batter #{}'
            '    (position {})\n'
        ).format(
            self.player_obj.hitting_stats(),
            start_inning_str,
            self.start_inning_batter_num,
            self.position
        )

        if self.end_inning_num:
            end_inning_str = '{}-{}'.format(self.end_inning_num,
                                            self.end_inning_half)

            return_str += (
                '    Exited:      {:12} before batter #{}\n'
            ).format(
                end_inning_str,
                self.end_inning_batter_num
            )

        return return_str


class Player:
    def __init__(self, last_name, first_name, mlb_id, obp, slg, number):
        self.last_name = last_name
        self.first_name = first_name
        self.mlb_id = mlb_id
        self.obp = obp
        self.slg = slg
        self.number = number

        self.era = None
        self.pitch_hand = None
        self.bat_side = None

    def _asdict(self):
        return (
            {'last_name': self.last_name,
             'first_name': self.first_name,
             'mlb_id': self.mlb_id,
             'obp': self.obp,
             'slg': self.slg,
             'number': self.number,
             'era': self.era,
             'pitch_hand': self.pitch_hand,
             'bat_side': self.bat_side}
        )

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def hitting_stats(self):
        if self.obp and self.slg:
            return_str = 'OBP: {}   SLG: {}'.format('%.3f' % self.obp,
                                                    '%.3f' % self.slg)
        else:
            return_str = ''

        return return_str

    def pitching_stats(self):
        if self.era:
            era_str = 'ERA: {}'.format('%.2f' % self.era)
        else:
            era_str = 'ERA: {}'.format(self.era)

        return era_str


    def __repr__(self):
        return_str = ''
        if self.number is not None:
            return_str += '{:2} '.format(self.number)
        else:
            return_str += '   '

        return_str += '{}'.format(self.full_name())

        return return_str


class Team:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

        self.pitcher_list = []
        self.batting_order_list_list = [None] * 9
        self.player_id_dict = {}
        self.player_name_dict = {}
        self.player_last_name_dict = {}

    def _asdict(self):
        return (
            {'name': self.name,
             'abbreviation': self.abbreviation,
             'pitcher_list': [x._asdict() for x in self.pitcher_list],
             'batting_order_list_list': [[x._asdict() for x in y]
                                         for y in self.batting_order_list_list]}
        )

    def find_player(self, player_key):
        player = None
        if isinstance(player_key, int):
            player_id = player_key
            player = self.player_id_dict.get(player_id)
        elif isinstance(player_key, str):
            player_name = player_key
            player_name_no_spaces = ''.join(player_name.split())
            for player_name_key in self.player_name_dict:
                if player_name_no_spaces in player_name_key:
                    player = self.player_name_dict[player_name_key]

            if not player:
                player_name = sub(r' Jr$', '', player_name.strip(' .'))
                player_name = sub(r' Sr$', '', player_name.strip(' .'))
                player_name = sub(r' II$', '', player_name.strip())
                player_name = sub(r' III$', '', player_name.strip())
                player_name = sub(r' IV$', '', player_name.strip())

                player_name = strip_suffixes(player_name.strip())
                first_name_initial = player_name[0]
                last_name = player_name.split()[-1]

                initial_plus_last_name = first_name_initial + last_name
                player = self.player_last_name_dict.get(initial_plus_last_name)
        else:
            raise ValueError(
                'Player key: {player_key} must be either int or str'.format(
                    player_key=player_key
                )
            )

        return player

    def append(self, player):
        last_name = sub(
            r' Jr$', '', player.last_name.strip('. ').replace(',', '')
        )

        last_name = sub(r' Sr$', '', last_name.strip('. ').replace(',', ''))
        last_name = sub(r' II$', '', last_name.strip())
        last_name = sub(r' III$', '', last_name.strip())
        last_name = sub(r' IV$', '', last_name.strip())
        last_name = sub(r' St\. ', ' St ', last_name.strip())
        if ' ' in last_name:
            last_name = last_name.split()[1]

        self.player_id_dict[player.mlb_id] = player
        self.player_name_dict[''.join(player.full_name().split())] = player
        self.player_last_name_dict[player.first_name[0] + last_name] = player

        if '-' in last_name:
            last_half_name = last_name.split('-')[1]
            self.player_name_dict[
                '{}{}'.format(player.first_name, last_half_name)
            ] = player

            self.player_last_name_dict[
                player.first_name[0] + last_half_name
            ] = player

    def __contains__(self, player_key):
        return bool(self.find_player(player_key))

    def __getitem__(self, player_key):
        player = self.find_player(player_key)
        if player:
            return player
        else:
            raise ValueError('{} not found in team'.format(player_key))

    def __repr__(self):
        return_str = (
            '{}\n# {} ({}) #\n{}\n\n'
            '---------\n'
            ' Batters \n'
            '---------\n'
        ).format(
            '#' * (len(self.name) + 10),
            self.name.upper(),
            self.abbreviation,
            '#' * (len(self.name) + 10)
        )

        for batter_list in self.batting_order_list_list:
            return_str += '{}\n'.format(
                batter_list
            )

        return_str += (
            '\n----------\n'
            ' Pitchers \n'
            '----------\n'
            '{}\n\n'
        ).format(
            self.pitcher_list
        )

        return return_str


class Game:
    def __init__(self, home_team, away_team, location, game_date_str):
        self.home_team = home_team
        self.away_team = away_team
        self.location = location or ''
        self.game_date_str = game_date_str

        self.start_datetime = None
        self.end_datetime = None
        self.inning_list = []
        self.away_batter_box_score_dict = None
        self.home_batter_box_score_dict = None
        self.away_pitcher_box_score_dict = None
        self.home_pitcher_box_score_dict = None
        self.away_team_stats = None
        self.home_team_stats = None
        self.attendance = None
        self.temp = None
        self.weather = None
        self.expected_start_datetime = None
        self.timezone_str = EASTERN_TIMEZONE_STR
        self.is_postponed = False
        self.is_suspended = False
        self.is_doubleheader = False
        self.is_today = True

    def json(self):
        return dumps(self._asdict())

    @staticmethod
    def denormalize_box_score_dict(box_score_dict):
        tuple_list = []
        for x, y in box_score_dict.items():
            if isinstance(x, str):
                value = x
            elif isinstance(x, Player):
                value = x._asdict()
            else:
                raise ValueError('Wrong type.')

            tuple_list.append((value, y._asdict()))

        return tuple_list

    def _asdict(self):
        return (
            {'home_team': self.home_team._asdict(),
             'away_team': self.away_team._asdict(),
             'location': self.location,
             'game_date_str': self.game_date_str,
             'start_datetime': str(self.start_datetime),
             'end_datetime': str(self.end_datetime),
             'inning_list': [x._asdict() for x in self.inning_list],
             'away_batter_box_score_dict': self.denormalize_box_score_dict(
                 self.away_batter_box_score_dict
             ),
             'home_batter_box_score_dict': self.denormalize_box_score_dict(
                 self.home_batter_box_score_dict
             ),
             'away_pitcher_box_score_dict': self.denormalize_box_score_dict(
                 self.away_pitcher_box_score_dict
             ),
             'home_pitcher_box_score_dict': self.denormalize_box_score_dict(
                 self.home_pitcher_box_score_dict
             ),
             'away_team_stats': self.away_team_stats._asdict(),
             'home_team_stats': self.home_team_stats._asdict(),
             'attendance': self.attendance,
             'temp': self.temp,
             'weather': self.weather,
             'expected_start_datetime': str(self.expected_start_datetime),
             'timezone_str': self.timezone_str}
        )

    def get_svg_str(self):
        return get_game_svg_str(self)

    def set_gametimes(self):
        for ballpark, this_timezone in STADIUM_TIMEZONE_DICT.items():
            if ballpark in self.location:
                self.timezone_str = this_timezone

        if not self.start_datetime:
            if self.inning_list:
                if self.inning_list[0].top_half_appearance_list:
                    self.start_datetime = (
                        self.inning_list[0].top_half_appearance_list[0].end_datetime
                    )

        if not self.end_datetime:
            if self.inning_list:
                last_inning_half_appearance_list = (
                    self.inning_list[-1].bottom_half_appearance_list or
                    self.inning_list[-1].top_half_appearance_list
                )

                if last_inning_half_appearance_list:
                    self.end_datetime = (
                        last_inning_half_appearance_list[-1].end_datetime
                    )

    def set_pitching_box_score_dict(self):
        self.away_pitcher_box_score_dict = OrderedDict([])
        self.home_pitcher_box_score_dict = OrderedDict([])

        tuple_list = [
            (self.away_pitcher_box_score_dict, self.away_team, 'bottom'),
            (self.home_pitcher_box_score_dict, self.home_team, 'top'),
        ]

        for box_score_dict, team, inning_half_str in tuple_list:
            for pitcher_appearance in team.pitcher_list:
                pitcher = pitcher_appearance.player_obj
                box_score_dict[pitcher] = (
                    get_all_pitcher_stats(self, team, pitcher, inning_half_str)
                )

    def set_batting_box_score_dict(self):
        self.away_batter_box_score_dict = OrderedDict([])
        self.home_batter_box_score_dict = OrderedDict([])

        tuple_list = [
            (self.away_batter_box_score_dict, self.away_team, 'top'),
            (self.home_batter_box_score_dict, self.home_team, 'bottom'),
        ]

        for box_score_dict, team, inning_half_str in tuple_list:
            for batting_order_list in team.batting_order_list_list:
                for batter_appearance in batting_order_list:
                    batter = batter_appearance.player_obj
                    if batter not in box_score_dict:
                        box_score_dict[batter] = (
                            get_all_batter_stats(self, batter, inning_half_str)
                        )

            box_score_dict['TOTAL'] = get_box_score_total(box_score_dict)

    def set_team_stats(self):
        self.away_team_stats = get_team_stats(self, 'top')
        self.home_team_stats = get_team_stats(self, 'bottom')

    def __repr__(self):
        return_str = '{}\n'.format(self.location)
        if self.start_datetime and self.end_datetime:
            start_str = self.start_datetime.astimezone(
                timezone(self.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p')

            end_str = self.end_datetime.astimezone(
                timezone(self.timezone_str)
            ).strftime(' - %-I:%M %p %Z')

            return_str += '{}{}\n\n'.format(start_str, end_str)
        else:
            return_str += '{}\n\n'.format(self.game_date_str)

        dict_list = [self.away_batter_box_score_dict,
                     self.away_pitcher_box_score_dict,
                     self.home_batter_box_score_dict,
                     self.home_pitcher_box_score_dict]

        for this_dict in dict_list:
            for name, tup in this_dict.items():
                return_str += '{!s:20s} {}\n'.format(name, str(tup))

            return_str += '\n'

        return_str += 'Away Team ({}): {}\nHome Team ({}): {}\n'.format(
            self.away_batter_box_score_dict['TOTAL'].R,
            str(self.away_team_stats),
            self.home_batter_box_score_dict['TOTAL'].R,
            str(self.home_team_stats)
        )

        return_str += '{}AT\n\n{}'.format(
            self.away_team,
            self.home_team
        )

        for i, inning in enumerate(self.inning_list):
            inning_number = i + 1
            return_str += (
                (' ' * 33) + '############\n' +
                (' ' * 33) + '# INNING {} #\n' +
                (' ' * 33) + '############\n\n{}\n\n'
            ).format(
                inning_number,
                inning
            )

        return return_str


class Inning:
    def __init__(self, top_half_appearance_list, bottom_half_appearance_list):
        self.top_half_appearance_list = top_half_appearance_list
        self.bottom_half_appearance_list = bottom_half_appearance_list
        (self.top_half_inning_stats,
         self.bottom_half_inning_stats) = (
             get_half_inning_stats(top_half_appearance_list,
                                   bottom_half_appearance_list)
         )

    def _asdict(self):
        if self.bottom_half_appearance_list:
            bottom_half_appearance_dict_list = [
                x._asdict()
                for x in self.bottom_half_appearance_list
            ]
        else:
            bottom_half_appearance_dict_list = []

        return (
            {'top_half_appearance_list': [
                x._asdict()
                for x in self.top_half_appearance_list
            ],
             'bottom_half_appearance_list': bottom_half_appearance_dict_list,
             'top_half_inning_stats': self.top_half_inning_stats,
             'bottom_half_inning_stats': self.bottom_half_inning_stats}
        )

    def __repr__(self):
        return (
            ('-' * 32) + ' TOP OF INNING ' + ('-' * 32) + '\n{}\n{}\n\n' +
            ('-' * 30) + ' BOTTOM OF INNING ' + ('-' * 31) + '\n{}\n{}'
        ).format(
            self.top_half_inning_stats,
            self.top_half_appearance_list,
            self.bottom_half_inning_stats,
            self.bottom_half_appearance_list
        )


class PlateAppearance:
    def __init__(self, start_datetime, end_datetime, batting_team,
                 plate_appearance_description, plate_appearance_summary,
                 pitcher, batter, inning_outs, scoring_runners_list,
                 runners_batted_in_list, event_list):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.batting_team = batting_team
        self.event_list = event_list or []
        self.plate_appearance_description = plate_appearance_description
        self.plate_appearance_summary = plate_appearance_summary
        self.pitcher = pitcher
        self.batter = batter
        self.inning_outs = inning_outs
        self.scoring_runners_list = scoring_runners_list
        self.runners_batted_in_list = runners_batted_in_list
        self.out_runners_list = self.get_out_runners_list(
            self.plate_appearance_description,
            self.batting_team,
            self.event_list,
            self.batter
        )

        self.hit_location = self.get_hit_location()
        self.error_str = self.get_error_str()
        (self.got_on_base,
         self.scorecard_summary) = self.get_on_base_and_summary()

    def _asdict(self):
        return (
            {'start_datetime': str(self.start_datetime),
             'end_datetime': str(self.end_datetime),
             'batting_team': self.batting_team.name,
             'event_list': [x._asdict() for x in self.event_list],
             'plate_appearance_description': self.plate_appearance_description,
             'plate_appearance_summary': self.plate_appearance_summary,
             'pitcher': self.pitcher._asdict(),
             'batter': self.batter._asdict(),
             'inning_outs': self.inning_outs,
             'scoring_runners_list': [x._asdict()
                                      for x in self.scoring_runners_list],
             'runners_batted_in_list': [x._asdict()
                                        for x in self.runners_batted_in_list],
             'out_runners_list': [(x[0]._asdict(), x[1])
                                  for x in self.out_runners_list],
             'hit_location': self.hit_location,
             'error_str': self.error_str,
             'got_on_base': self.got_on_base,
             'scorecard_summary': self.scorecard_summary}
        )

    @staticmethod
    def process_defense_predicate_list(defense_player_order):
        defense_code_order = []
        for defense_position in defense_player_order:
            if defense_position in POSITION_CODE_DICT:
                defense_code_order.append(
                    str(POSITION_CODE_DICT[defense_position])
                )

        return defense_code_order

    @staticmethod
    def get_defense_player_order(defense_predicate_list):
        defense_player_order = []
        for this_position in defense_predicate_list:
            if 'deep' in this_position:
                this_position = this_position.replace('deep', '').strip()

            if 'shallow' in this_position:
                this_position = this_position.replace('shallow', '').strip()

            this_position = this_position.split()[0].split('-')[0]
            defense_player_order.append(this_position)

        return defense_player_order

    @staticmethod
    def get_defense_predicate_list(description_str):
        if ('caught stealing' in description_str or
                'on fan interference' in description_str or
                'picks off' in description_str or
                'wild pitch by' in description_str):
            defense_predicate_list = []
        elif 'catcher interference by' in description_str:
            defense_predicate_list = ['catcher']
        elif 'fielded by' in description_str:
            description_str = description_str.split(' fielded by ')[1]
            defense_predicate_list = [description_str]
        elif ', ' in description_str and ' to ' in description_str:
            description_str = description_str.split(', ')[1]
            defense_predicate_list = description_str.split(' to ')
        elif  ' to ' in description_str:
            defense_predicate_list = description_str.split(' to ')[1:]
        elif ', ' in description_str and ' to ' not in description_str:
            description_str = description_str.split(', ')[1]
            defense_predicate_list = [description_str]
        else:
            defense_predicate_list = []

        if 'error by' in description_str:
            description_str = description_str.split(' error by ')[1]
            defense_predicate_list = [description_str]

        return defense_predicate_list

    @classmethod
    def get_defense_code_order(cls, description_str):
        defense_predicate_list = cls.get_defense_predicate_list(description_str)

        defense_player_order = cls.get_defense_player_order(
            defense_predicate_list
        )

        defense_code_order = cls.process_defense_predicate_list(
            defense_player_order
        )

        return defense_code_order

    @classmethod
    def get_defense_suffix(cls, suffix_str):
        this_search = search(
            r'(?:out at|(?:was )?picked off and caught stealing|'
            r'(?:was )?caught stealing|(?:was )?picked off|'
            r'(?:was )?doubled off)'
            r'[1-3,h][snro][tdm][e]?[\w\s]*, ',
            suffix_str
        )

        if this_search:
            suffix_str = suffix_str[this_search.start():]
            suffix_code_order = cls.get_defense_code_order(suffix_str)
            defense_suffix = ' (' + '-'.join(suffix_code_order) + ')'
        else:
            defense_suffix = ''

        return defense_suffix

    @staticmethod
    def get_out_runners_list(plate_appearance_description, batting_team,
                             event_list, batter):
        description = strip_suffixes(plate_appearance_description)
        runner_name_list = findall(
            (r'([A-Z][\w\'-]+\s+(?:[A-Z,a-z][\w\'-]+\s+)?'
             r'(?:[A-Z,a-z][\w\'-]+\s+)?[A-Z][\w\'-]+)\s+'
             r'(?:out at|(?:was )?picked off and caught stealing|'
             r'(?:was )?caught stealing|(?:was )?picked off|'
             r'(?:was )?doubled off)'
             r' +(\w+)'),
            description
        )

        runner_in_list = False
        for event in event_list:
            if (isinstance(event, RunnerAdvance) and event.end_base == ''
                    and not event.runner_scored and event.runner != batter):
                for name, _ in runner_name_list:
                    if event.runner.last_name in name:
                        runner_in_list = True
                        break

                if not runner_in_list:
                    runner_name_list.append(
                        (
                            '{} {}'.format(event.runner.first_name,
                                           event.runner.last_name),
                            BASE_PLUS_ONE_DICT[event.start_base]
                        )
                    )

        runner_tuple_list = []
        for name, base in runner_name_list:
            search_pattern = escape(name) + r' (?:was )?doubled off'
            if findall(search_pattern, description):
                base = INCREMENT_BASE_DICT[base]

            runner_tuple_list.append(
                (batting_team[name], base)
            )

        return runner_tuple_list

    def get_throws_str(self):
        description_str = strip_suffixes(self.plate_appearance_description)
        suffix_str = ''

        if '. ' in description_str:
            description_str, suffix_str = description_str.split('. ', 1)

        if ', deflected' in description_str:
            description_str = description_str.split(', deflected')[0]

        if ', assist' in description_str:
            description_str = description_str.split(', assist')[0]

        if ': ' in description_str:
            description_str = description_str.split(': ')[1]

        defense_code_order = self.get_defense_code_order(description_str)
        defense_str = '-'.join(defense_code_order)
        defense_suffix = self.get_defense_suffix(suffix_str)

        return defense_str, defense_suffix

    def get_hit_location(self):
        play_str = self.get_play_str()
        throws_str, _ = self.get_throws_str()

        if throws_str and play_str not in NO_HIT_CODE_LIST:
            hit_location = play_str + throws_str[0]
        else:
            hit_location = None

        return hit_location

    def get_play_str(self):
        description_str = strip_suffixes(self.plate_appearance_description)
        if '. ' in description_str:
            description_str = description_str.split('. ')[0]

        code = None
        for keyword, this_code in PLAY_CODE_ORDERED_DICT.items():
            if keyword in description_str.lower():
                code = this_code

        for keyword, this_code in [('Sac Fly', 'SF'), ('Sac Bunt', 'SH')]:
            if keyword in self.plate_appearance_summary:
                code = this_code

        if self.plate_appearance_summary == 'Fan interference':
            code = 'FI'
        elif ' out to ' in description_str and code is None:
            code = 'F'
        elif not code:
            disqualified_description = (
                'out at' in description_str or
                'singles' in description_str or
                'doubles' in description_str or
                'triples' in description_str or
                'hits a home run' in description_str or
                'ejected' in description_str or
                'remains in the game' in description_str or
                ' replaces ' in description_str or
                'mound visit' in description_str.lower() or
                'delay' in description_str.lower()
            )

            if disqualified_description:
                code = ''
            else:
                code = ''

        return code

    def get_error_str(self):
        error_str = None
        if 'error' in self.plate_appearance_description:
            description_str = self.plate_appearance_description
            description_str = description_str.split(' error by ')[1]
            defense_player = description_str.split()[0]
            defense_code = str(POSITION_CODE_DICT[defense_player])
            error_str = 'E' + defense_code
        elif 'catcher interference' in self.plate_appearance_description:
            error_str = 'E2'

        return error_str

    def get_on_base_and_summary(self):
        throws_str, suffix_str = self.get_throws_str()
        if self.plate_appearance_summary in ON_BASE_SUMMARY_DICT:
            on_base = True
            scorecard_summary = (
                ON_BASE_SUMMARY_DICT[self.plate_appearance_summary] +
                suffix_str
            )

            if (self.plate_appearance_summary == 'Home Run' and
                    ('inside-the-park' in self.plate_appearance_description or
                     'inside the park' in self.plate_appearance_description)):
                scorecard_summary = 'I' + scorecard_summary
        else:
            on_base = False
            if self.get_play_str() == 'CI':
                scorecard_summary = self.get_play_str() + suffix_str
            else:
                fielders_choice = False
                for event in self.event_list:
                    if (isinstance(event, RunnerAdvance) and
                            event.runner == self.batter and
                            event.end_base and
                            not 'Error' in self.plate_appearance_summary and
                            len(self.out_runners_list) > 0):
                        fielders_choice = True

                if fielders_choice:
                    scorecard_summary = 'FC' + throws_str + suffix_str
                else:
                    scorecard_summary = (self.get_play_str() + throws_str +
                                         suffix_str)

        return on_base, scorecard_summary

    def __repr__(self):
        wrapper = TextWrapper(width=80, subsequent_indent=' '*17)

        description_str = ' Description:    {}'.format(
            self.plate_appearance_description
        )

        return_str = ('\n'
                      ' Scorecard:      {}\n'
                      ' Hit location:   {}\n'
                      ' Pitcher:        {}\n'
                      ' Batter:         {}\n'
                      ' Got on base:    {}\n'
                      ' Fielding Error: {}\n'
                      ' Out Runners:    {}\n'
                      ' Scoring Runners:{}\n'
                      ' Runs Batted In: {}\n'
                      ' Inning Outs:    {}\n'
                      ' Summary:        {}\n'
                      '{}\n'
                      ' Events:\n').format(self.scorecard_summary,
                                           self.hit_location,
                                           self.pitcher,
                                           self.batter,
                                           self.got_on_base,
                                           self.error_str,
                                           self.out_runners_list,
                                           self.scoring_runners_list,
                                           self.runners_batted_in_list,
                                           self.inning_outs,
                                           self.plate_appearance_summary,
                                           wrapper.fill(description_str))

        for event in self.event_list:
            return_str += '     {}\n'.format(event)

        return return_str
