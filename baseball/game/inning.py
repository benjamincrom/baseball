
from baseball.stats import (get_half_inning_stats)

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
