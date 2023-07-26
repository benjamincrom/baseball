from collections import OrderedDict
from json import dumps

from pytz import timezone

from baseball import (EASTERN_TIMEZONE_STR, STADIUM_TIMEZONE_DICT)
from baseball.generate_svg import get_game_svg_str

from baseball.stats import (get_all_pitcher_stats,
                            get_all_batter_stats,
                            get_box_score_total,
                            get_team_stats)

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
