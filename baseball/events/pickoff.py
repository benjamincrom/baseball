
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
