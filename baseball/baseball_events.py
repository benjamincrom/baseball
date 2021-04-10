AUTOMATIC_BALL_POSITION = (1.0, 1.0)


class Substitution:
    def __init__(self, substitution_datetime, incoming_player, outgoing_player,
                 batting_order, position):
        self.substitution_datetime = substitution_datetime
        self.incoming_player = incoming_player
        self.outgoing_player = outgoing_player
        self.batting_order = batting_order
        self.position = position

    def _asdict(self):
        return (
            {'substitution_datetime': str(self.substitution_datetime),
             'incoming_player': self.incoming_player._asdict(),
             'outgoing_player': self.outgoing_player._asdict(),
             'batting_order': self.batting_order,
             'position': self.position}
        )

    def __repr__(self):
        incoming_player_name = str(self.incoming_player)

        if self.batting_order:
            batting_str = 'Batting {}'.format(self.batting_order)
            if self.position:
                batting_str += ', '
        else:
            batting_str = ''

        if self.position:
            position_str = 'Position {}'.format(self.position)
        else:
            position_str = ''

        if batting_str or position_str:
            summary_str = '({}{})'.format(batting_str, position_str)
        else:
            summary_str = ''

        return_str = '{:23} {}'.format('- IN: ' + incoming_player_name,
                                       summary_str)

        if summary_str:
            return_str = '{:48}  {}'.format(
                return_str,
                'OUT: ' + str(self.outgoing_player)
            )

        return return_str


class Switch:
    def __init__(self, switch_datetime, player, old_position_num,
                 new_position_num, new_batting_order):
        self.switch_datetime = switch_datetime
        self.player = player
        self.old_position_num = old_position_num
        self.new_position_num = new_position_num
        self.new_batting_order = new_batting_order

    def _asdict(self):
        return (
            {'switch_datetime': str(self.switch_datetime),
             'player': self.player._asdict(),
             'old_position_num': self.old_position_num,
             'new_position_num': self.new_position_num,
             'new_batting_order': self.new_batting_order}
        )

    def __repr__(self):
        position_str = (
            '(from position {} to position {}'
        ).format(
            self.old_position_num,
            self.new_position_num
        )

        if self.new_batting_order:
            position_str += ', batting {})'.format(self.new_batting_order)
        else:
            position_str += ')'

        return_str = (
            '- SWITCH: {:31} {:>32}'
        ).format(
            str(self.player),
            position_str
        )

        return return_str


class Pitch:
    def __init__(self, pitch_datetime, pitch_description, pitch_type,
                 pitch_speed, pitch_position):
        self.pitch_datetime = pitch_datetime
        self.pitch_description = pitch_description
        self.pitch_type = pitch_type
        self.pitch_speed = pitch_speed
        self.pitch_position = pitch_position

    def _asdict(self):
        return (
            {'pitch_datetime': str(self.pitch_datetime),
             'pitch_description': self.pitch_description,
             'pitch_type': self.pitch_type,
             'pitch_speed': self.pitch_speed,
             'pitch_position': self.pitch_position}
        )

    def __repr__(self):
        position_str = (
            '(' +
            '%.2f, ' % self.pitch_position[0] +
            '%.2f' % self.pitch_position[1] +
            ')'
        )

        return_str = (
            '- Pitch:' + (' ' * 16) + '{:19} {:4}  {:4} {:>19}'
        ).format(
            self.pitch_description,
            str(self.pitch_type),
            str(self.pitch_speed),
            position_str
        )

        return return_str


class Pickoff:
    def __init__(self, pickoff_description, pickoff_base,
                 pickoff_was_successful):
        self.pickoff_description = pickoff_description
        self.pickoff_base = pickoff_base
        self.pickoff_was_successful = pickoff_was_successful

    def _asdict(self):
        return self.__dict__

    def __repr__(self):
        if self.pickoff_was_successful:
            call_str = 'Out'
        else:
            call_str = 'Safe'

        return_str = (
            '- Pickoff:' + (' ' * 14) + '{} ({})'
        ).format(
            self.pickoff_description.split()[-1],
            call_str
        )

        return return_str


class RunnerAdvance:
    def __init__(self, run_description, runner, start_base, end_base,
                 runner_scored, run_earned, is_rbi):
        self.run_description = run_description
        self.runner = runner
        self.start_base = start_base
        self.end_base = end_base
        self.runner_scored = runner_scored
        self.run_earned = run_earned
        self.is_rbi = is_rbi

    def _asdict(self):
        return (
            {'run_description': self.run_description,
             'runner': self.runner._asdict(),
             'start_base': self.start_base,
             'end_base': self.end_base,
             'runner_scored': self.runner_scored,
             'run_earned': self.run_earned,
             'is_rbi': self.is_rbi}
        )
    def __repr__(self):
        score_str = ''
        if self.runner_scored:
            score_str += '(Scored'

        if self.run_earned:
            score_str += ', Earned'

        if self.is_rbi:
            score_str += ', RBI'

        if self.runner_scored:
            score_str += ')'

        return_str = '- {:21} {:19} {:2}--->{:2} {:>21}'.format(
            str(self.runner) + ':',
            self.run_description,
            self.start_base,
            self.end_base,
            score_str
        )

        return return_str
