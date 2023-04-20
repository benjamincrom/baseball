
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
