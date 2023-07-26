
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
