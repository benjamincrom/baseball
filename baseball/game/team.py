from re import sub

from baseball import strip_suffixes

class Team:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

        self.pitcher_list = []
        self.batting_order_list_list = [None] * 9
        self.player_id_dict = {}
        self.player_name_dict = {}
        self.player_last_name_dict = {}

    def _asdict(self):
        return (
            {'name': self.name,
             'abbreviation': self.abbreviation,
             'pitcher_list': [x._asdict() for x in self.pitcher_list],
             'batting_order_list_list': [[x._asdict() for x in y]
                                         for y in self.batting_order_list_list]}
        )

    def find_player(self, player_key):
        player = None
        if isinstance(player_key, int):
            player_id = player_key
            player = self.player_id_dict.get(player_id)
        elif isinstance(player_key, str):
            player_name = player_key
            player_name_no_spaces = ''.join(player_name.split())
            for player_name_key in self.player_name_dict:
                if player_name_no_spaces in player_name_key:
                    player = self.player_name_dict[player_name_key]

            if not player:
                player_name = sub(r' Jr$', '', player_name.strip(' .'))
                player_name = sub(r' Sr$', '', player_name.strip(' .'))
                player_name = sub(r' II$', '', player_name.strip())
                player_name = sub(r' III$', '', player_name.strip())
                player_name = sub(r' IV$', '', player_name.strip())

                player_name = strip_suffixes(player_name.strip())
                first_name_initial = player_name[0]
                last_name = player_name.split()[-1]

                initial_plus_last_name = first_name_initial + last_name
                player = self.player_last_name_dict.get(initial_plus_last_name)
        else:
            raise ValueError(
                'Player key: {player_key} must be either int or str'.format(
                    player_key=player_key
                )
            )

        return player

    def append(self, player):
        last_name = sub(
            r' Jr$', '', player.last_name.strip('. ').replace(',', '')
        )

        last_name = sub(r' Sr$', '', last_name.strip('. ').replace(',', ''))
        last_name = sub(r' II$', '', last_name.strip())
        last_name = sub(r' III$', '', last_name.strip())
        last_name = sub(r' IV$', '', last_name.strip())
        last_name = sub(r' St\. ', ' St ', last_name.strip())
        if ' ' in last_name:
            last_name = last_name.split()[1]

        self.player_id_dict[player.mlb_id] = player
        self.player_name_dict[''.join(player.full_name().split())] = player
        self.player_last_name_dict[player.first_name[0] + last_name] = player

        if '-' in last_name:
            last_half_name = last_name.split('-')[1]
            self.player_name_dict[
                '{}{}'.format(player.first_name, last_half_name)
            ] = player

            self.player_last_name_dict[
                player.first_name[0] + last_half_name
            ] = player

    def __contains__(self, player_key):
        return bool(self.find_player(player_key))

    def __getitem__(self, player_key):
        player = self.find_player(player_key)
        if player:
            return player
        else:
            raise ValueError('{} not found in team'.format(player_key))

    def __repr__(self):
        return_str = (
            '{}\n# {} ({}) #\n{}\n\n'
            '---------\n'
            ' Batters \n'
            '---------\n'
        ).format(
            '#' * (len(self.name) + 10),
            self.name.upper(),
            self.abbreviation,
            '#' * (len(self.name) + 10)
        )

        for batter_list in self.batting_order_list_list:
            return_str += '{}\n'.format(
                batter_list
            )

        return_str += (
            '\n----------\n'
            ' Pitchers \n'
            '----------\n'
            '{}\n\n'
        ).format(
            self.pitcher_list
        )

        return return_str
