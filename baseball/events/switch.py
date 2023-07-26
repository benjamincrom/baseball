
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
