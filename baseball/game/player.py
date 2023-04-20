
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
