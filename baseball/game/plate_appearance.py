from textwrap import TextWrapper
from re import search, findall, escape

from baseball import (PLAY_CODE_ORDERED_DICT,
                      ON_BASE_SUMMARY_DICT,
                      POSITION_CODE_DICT,
                      NO_HIT_CODE_LIST,
                      strip_suffixes,
                      RunnerAdvance)

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
