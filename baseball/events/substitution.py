
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
