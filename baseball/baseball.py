from collections import OrderedDict
from json import dumps
from textwrap import TextWrapper
from re import search, sub, findall, escape

from pytz import timezone

from baseball.baseball_events import RunnerAdvance
from baseball.generate_svg import get_game_svg_str
from baseball.stats import (get_all_pitcher_stats,
                            get_all_batter_stats,
                            get_box_score_total,
                            get_team_stats,
                            get_half_inning_stats)

POSITION_CODE_DICT = {'pitcher': 1,
                      'catcher': 2,
                      'first': 3,
                      'second': 4,
                      'third': 5,
                      'shortstop': 6,
                      'left': 7,
                      'center': 8,
                      'right': 9,
                      'designated': 10,
                      '1B': 3,
                      '2B': 4,
                      '3B': 5,
                      'SS': 6,
                      'P': 1,
                      'C': 2,
                      'LF': 7,
                      'CF': 8,
                      'RF': 9}

ON_BASE_SUMMARY_DICT = {'Single': '1B',
                        'Double': '2B',
                        'Triple': '3B',
                        'Hit By Pitch': 'HBP',
                        'Home Run': 'HR',
                        'Walk': 'BB',
                        'Intent Walk': 'IBB'}

PLAY_CODE_ORDERED_DICT = OrderedDict([
    ('picks off', 'PO'),
    ('caught stealing', 'CS'),
    ('wild pitch', 'WP'),
    ('passed ball', 'PB'),
    ('balk', 'BLK'),
    ('steals', 'S'),
    ('fan interference', 'FI'),
    ('catcher interference', 'CI'),
    ('error', 'E'),
    ('ground', 'G'),
    ('grand slam', 'HR'),
    ('homers', 'HR'),
    ('pop', 'P'),
    ('line', 'L'),
    ('fly', 'F'),
    ('flies', 'F'),
    ('sacrifice fly', 'SF'),
    ('hit by pitch', 'HBP'),
    ('bunt', 'B'),
    ('sacrifice bunt', 'SH'),
    ('walks', 'BB'),
    ('intentionally walks', 'IBB'),
    ('called out on strikes', 'ꓘ'),
    ('strikes out', 'K'),
    ('choice', 'FC')
])

NO_HIT_CODE_LIST = ['K', 'ꓘ', 'BB', 'IBB']

BASE_PLUS_ONE_DICT = {'': '1st',
                      '1B': '2nd',
                      '2B': '3rd',
                      '3B': 'home'}

INCREMENT_BASE_DICT = {'1st': '2nd',
                       '2nd': '3rd',
                       '3rd': 'home'}

STADIUM_TIMEZONE_DICT = {
    'Fenway Park': 'America/New_York',
    'George M. Steinbrenner Field': 'America/New_York',
    'Yankee Stadium': 'America/New_York',
    'Roger Dean Stadium': 'America/New_York',
    'Joker Marchant Stadium': 'America/New_York',
    'JetBlue Park': 'America/New_York',
    'Citi Field': 'America/New_York',
    'LECOM Park': 'America/New_York',
    'First Data Field': 'America/New_York',
    'The Ballpark of the Palm Beaches': 'America/New_York',
    'Citizens Bank Park': 'America/New_York',
    'Spectrum Field': 'America/New_York',
    'Oriole Park': 'America/New_York',
    'Nationals Park': 'America/New_York',
    'Champion Stadium': 'America/New_York',
    'Truist Park': 'America/New_York',
    'Tropicana Field': 'America/New_York',
    'Marlins Park': 'America/New_York',
    'Rogers Centre': 'America/New_York',
    'PNC Park': 'America/New_York',
    'Progressive Field': 'America/New_York',
    'Comerica Park': 'America/New_York',
    'Great American Ball Park': 'America/New_York',
    'Miller Park': 'America/Chicago',
    'Wrigley Field': 'America/Chicago',
    'Guaranteed Rate Field': 'America/Chicago',
    'Busch Stadium': 'America/Chicago',
    'Target Field': 'America/Chicago',
    'Globe Life Field': 'America/Chicago',
    'Minute Maid Park': 'America/Chicago',
    'Kauffman Stadium': 'America/Chicago',
    'American Family Field': 'America/Chicago',
    'Coors Field': 'America/Denver',
    'Chase Field': 'America/Phoenix',
    'Safeco Field': 'America/Los_Angeles',
    'AT&T Park': 'America/Los_Angeles',
    'Oakland-Alameda County Coliseum': 'America/Los_Angeles',
    'Oakland Coliseum': 'America/Los_Angeles',
    'Angel Stadium': 'America/Los_Angeles',
    'Oracle Park': 'America/Los_Angeles',
    'Dodger Stadium': 'America/Los_Angeles',
    'Petco Park': 'America/Los_Angeles',
    'T-Mobile Park': 'America/Los_Angeles'
}

EASTERN_TIMEZONE_STR = 'America/New_York'

def strip_this_suffix(pattern, suffix, input_str):
    match = search(pattern, input_str)
    while match:
        start = match.start()
        end = match.end()
        str_beginning = input_str[:start]
        str_middle = sub(suffix, '.', input_str[start:end])
        str_end = input_str[end:]
        input_str = str_beginning + str_middle + str_end
        match = search(pattern, input_str)

    input_str = sub(suffix, '', input_str)

    return input_str.strip()

def strip_suffixes(input_str):
    input_str = strip_this_suffix(r' Jr\.\s+[A-Z]', r' Jr\.', input_str)
    input_str = strip_this_suffix(r' Sr\.\s+[A-Z]', r' Sr\.', input_str)
    input_str = sub(r' II', '', input_str)
    input_str = sub(r' III', '', input_str)
    input_str = sub(r' IV', '', input_str)
    input_str = sub(r' St\. ', ' St ', input_str)

    initials_match = findall(r'([A-Z]\.[A-Z]\.? )', input_str)
    while initials_match:
        new_initials = initials_match[0].replace('.', '')
        input_str = sub(initials_match[0], new_initials, input_str, 1)
        initials_match = findall(r'([A-Z]\.[A-Z]\.? )', input_str)

    return input_str


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

        if player_key == 'William DeMars':
            player = self.find_player('Billy DeMars')
        elif player_key == 'Yo-Yo Davalillo':
            player = self.find_player('Pompeyo Davalillo')
        elif player_key == 'Moose Morton':
            player = self.find_player('Guy Morton')
        elif player_key == 'Lefty Hayden':
            player = self.find_player('Gene Hayden')
        elif player_key == 'Ted Wieand':
            player = self.find_player('Franklin Wieand')
        elif player_key == 'Bucky Brandon':
            player = self.find_player('Darrell Brandon')
        elif player_key == 'Candy Harris':
            player = self.find_player('Alonzo Harris')
        elif player_key == 'Jose Baez':
            player = self.find_player('Jose Báez')
        elif player_key == 'Puchy Delgado':
            player = self.find_player('Luis Delgado')
        elif player_key == 'Tony Pena':
            player = self.find_player('Tony Peña')
        elif player_key == 'Jose Alvarez':
            player = self.find_player('José Álvarez')
        elif player_key == 'Victor Rodriguez':
            player = self.find_player('Victor Rodríguez')
        elif player_key == 'Eddie Tucker':
            player = self.find_player('Scooter Tucker')
        elif player_key == 'Wily Mo Pena':
            player = self.find_player('Wily Mo Peña')
        elif player_key == 'Carlos Hernandez':
            player = self.find_player('Carlos Hernández')
        elif player_key == 'Oliver Perez':
            player = self.find_player('Oliver Pérez')
        elif player_key == 'Einar Diaz':
            player = self.find_player('Einar Díaz')
        elif player_key == 'Adrian Beltre':
            player = self.find_player('Adrian Beltré')
        elif player_key == 'Carlos Beltran':
            player = self.find_player('Carlos Beltrán')
        elif player_key == 'Javier Lopez':
            player = self.find_player('Javier López')
        elif player_key == 'Eddie Perez':
            player = self.find_player('Eddie Pérez')
        elif player_key == 'Adrian Gonzalez':
            player = self.find_player('Adrián González')
        elif player_key == 'Robinson Cano':
            player = self.find_player('Robinson Canó')
        elif player_key == 'Brayan Pena':
            player = self.find_player('Brayan Peña')
        elif player_key == 'Edwin Encarnacion':
            player = self.find_player('Edwin Encarnación')
        elif player_key == 'Francisco Rodriguez':
            player = self.find_player('Francisco Rodríguez')
        elif player_key == 'Mendy Lopez':
            player = self.find_player('Mendy López')
        elif player_key == 'Jeremy Pena':
            player = self.find_player('Jeremy Peña')
        elif player_key == 'Jonathan Sanchez':
            player = self.find_player('Jonathan Sánchez')
        elif player_key == 'Jonathan Bermudez':
            player = self.find_player('Jonathan Bermúdez')
        elif player_key == 'Andrew Suarez':
            player = self.find_player('Andrew Suárez')
        elif player_key == 'Omar Narvaez':
            player = self.find_player('Omar Narváez')
        elif player_key == 'Eloy Jimenez':
            player = self.find_player('Eloy Jiménez')
        elif player_key == 'Moises Gomez':
            player = self.find_player('Moisés Gómez')
        elif player_key == 'Jason Garcia':
            player = self.find_player('Jason García')
        elif player_key == 'Francisco Mejia':
            player = self.find_player('Francisco Mejía')
        elif player_key == 'Carlos Rodon':
            player = self.find_player('Carlos Rodón')
        elif player_key == 'Michael Harris':
            player = self.find_player('Michael Harris II')
        elif player_key == 'Zach McKinstry':
            player = self.find_player('Zach McKinstry')
        elif player_key == 'Allen Cordoba':
            player = self.find_player('Allen Córdoba')
        elif player_key == 'Ronaldo Hernandez':
            player = self.find_player('Ronaldo Hernández')
        elif player_key == 'Ricardo Sanchez':
            player = self.find_player('Ricardo Sánchez')
        elif player_key == 'Matt Pare':
            player = self.find_player('Matt Paré')
        elif player_key == 'Miguel Gonzalez':
            player = self.find_player('Miguel González')
        elif player_key == 'Felix Pena':
            player = self.find_player('Félix Peña')
        elif player_key == 'Yohander Mendez':
            player = self.find_player('Yohander Méndez')
        elif player_key == 'Dom Nunez':
            player = self.find_player('Dom Nuñez')
        elif player_key == 'Randy Vasquez':
            player = self.find_player('Randy Vásquez')
        elif player_key == 'Angel Rondon':
            player = self.find_player('Angel Rondón')
        elif player_key == 'Yandy Diaz':
            player = self.find_player('Yandy Díaz')
        elif player_key == 'Edwin Diaz':
            player = self.find_player('Edwin Díaz')
        elif player_key == 'Jose De Leon':
            player = self.find_player('José De León')
        elif player_key == 'Angel Martinez':
            player = self.find_player('Angel Martínez')
        elif player_key == 'Adeiny Hechavarria':
            player = self.find_player('Adeiny Hechavarría')
        elif player_key == 'Adeiny HechavarrÃa':
            player = self.find_player('Adeiny Hechavarría')
        elif player_key == 'Jan Vazquez':
            player = self.find_player('Jan Vázquez')
        elif player_key == 'Neil Ramirez':
            player = self.find_player('Neil Ramírez')
        elif player_key == 'Chris Alleyne':
            player = self.find_player('Chris Alleyne')
        elif player_key == 'Bruce Rondon':
            player = self.find_player('Bruce Rondón')
        elif player_key == 'Anibal Sanchez':
            player = self.find_player('Aníbal Sánchez')
        elif player_key == 'Pedro Florimon':
            player = self.find_player('Pedro Florimón')
        elif player_key == 'Eury Perez':
            player = self.find_player('Eury Pérez')
        elif player_key == 'Yasmany Tomas':
            player = self.find_player('Yasmany Tomás')
        elif player_key == 'Roel Ramirez':
            player = self.find_player('Roel Ramírez')
        elif player_key == 'Yennsy Diaz':
            player = self.find_player('Yennsy Díaz')
        elif player_key == 'David Banuelos':
            player = self.find_player('David Bañuelos')
        elif player_key == 'Wenceel Perez':
            player = self.find_player('Wenceel Pérez')
        elif player_key == 'Aneury Tavarez':
            player = self.find_player('Aneury Tavárez')
        elif player_key == 'Marcos Castanon':
            player = self.find_player('Marcos Castañon')
        elif player_key == 'Dariel Alvarez':
            player = self.find_player('Dariel Álvarez')
        elif player_key == 'Jose Rondon':
            player = self.find_player('José Rondón')
        elif player_key == 'Miguel Diaz':
            player = self.find_player('Miguel Díaz')
        elif player_key == 'Arismendy Alcantara':
            player = self.find_player('Arismendy Alcántara')
        elif player_key == 'Ubaldo Jimenez':
            player = self.find_player('Ubaldo Jiménez')
        elif player_key == 'Dario Alvarez':
            player = self.find_player('Dario Álvarez')
        elif player_key == 'Sergio Alcantara':
            player = self.find_player('Sergio Alcántara')
        elif player_key == 'Jonathan Guzman':
            player = self.find_player('Jonathan Guzmán')
        elif player_key == 'Ozzie Martinez':
            player = self.find_player('Osvaldo Martínez')
        elif player_key == 'Carlos Perez':
            player = self.find_player('Carlos Pérez')
        elif player_key == 'Jonathan Hernandez':
            player = self.find_player('Jonathan Hernández')
        elif player_key == 'Hector Gomez':
            player = self.find_player('Héctor Gómez')
        elif player_key == 'Michael De Leon':
            player = self.find_player('Michael De León')
        elif player_key == 'Kristopher Negron':
            player = self.find_player('Kristopher Negrón')
        elif player_key == 'Deivi Garcia':
            player = self.find_player('Deivi García')
        elif player_key == 'Erick Pena':
            player = self.find_player('Erick Peña')
        elif player_key == 'Manuel Rodriguez':
            player = self.find_player('Manuel Rodríguez')
        elif player_key == 'Lewin Diaz':
            player = self.find_player('Lewin Díaz')
        elif player_key == 'Hernan Perez':
            player = self.find_player('Hernán Pérez')
        elif player_key == 'Edwin O Diaz':
            player = self.find_player('Edwin Díaz')
        elif player_key == 'Alex Ramirez':
            player = self.find_player('Alex Ramírez')
        elif player_key == 'Ranger Suarez':
            player = self.find_player('Ranger Suárez')
        elif player_key == 'Guillermo Zuniga':
            player = self.find_player('Guillermo Zuñiga')
        elif player_key == 'Luis Frias':
            player = self.find_player('Luis Frías')
        elif player_key == 'Michael Perez':
            player = self.find_player('Michael Pérez')
        elif player_key == 'Jose Berrios':
            player = self.find_player('José Berríos')
        elif player_key == 'Jerar Encarnacion':
            player = self.find_player('Jerar Encarnación')
        elif player_key == 'Julian Fernandez':
            player = self.find_player('Julian Fernández')
        elif player_key == 'Darwinzon Hernandez':
            player = self.find_player('Darwinzon Hernández')
        elif player_key == 'Vidal Brujan':
            player = self.find_player('Vidal Bruján')
        elif player_key == 'Emilio Pagan':
            player = self.find_player('Emilio Pagán')
        elif player_key == 'Teoscar Hernandez':
            player = self.find_player('Teoscar Hernández')
        elif player_key == 'Francisco Perez':
            player = self.find_player('Francisco Pérez')
        elif player_key == 'Willy Garcia':
            player = self.find_player('Willy García')
        elif player_key == 'Julio Urias':
            player = self.find_player('Julio Urías')
        elif player_key == 'Joe Colon':
            player = self.find_player('Joe Colón')
        elif player_key == 'Yoendrys Gomez':
            player = self.find_player('Yoendrys Gómez')
        elif player_key == 'Joe JimÃ©nez':
            player = self.find_player('Joe Jiménez')
        elif player_key == 'Joe Jimenez':
            player = self.find_player('Joe Jiménez')
        elif player_key == 'Jesus Sanchez':
            player = self.find_player('Jesús Sánchez')
        elif player_key == 'Rene Garcia':
            player = self.find_player('René García')
        elif player_key == 'Andres Munoz':
            player = self.find_player('Andrés Muñoz')
        elif player_key == 'Ismael Guillon':
            player = self.find_player('Ismael Guillón')
        elif player_key == 'Yacksel Rios':
            player = self.find_player('Yacksel Ríos')
        elif player_key == 'Yoan Lopez':
            player = self.find_player('Yoan López')
        elif player_key == 'Jorge Lopez':
            player = self.find_player('Jorge López')
        elif player_key == 'Kelvin Gutierrez':
            player = self.find_player('Kelvin Gutiérrez')
        elif player_key == 'Andy Ibanez':
            player = self.find_player('Andy Ibáñez')
        elif player_key == 'Robel Garcia':
            player = self.find_player('Robel García')
        elif player_key == 'Ronny Rodriguez':
            player = self.find_player('Ronny Rodríguez')
        elif player_key == 'Ricardo Genoves':
            player = self.find_player('Ricardo Genovés')
        elif player_key == 'Victor Gonzalez':
            player = self.find_player('Victor González')
        elif player_key == 'Eliezer Alvarez':
            player = self.find_player('Eliezer Álvarez')
        elif player_key == 'Gary Sanchez':
            player = self.find_player('Gary Sánchez')
        elif player_key == 'Yairo Munoz':
            player = self.find_player('Yairo Muñoz')
        elif player_key == 'Endy Rodriguez':
            player = self.find_player('Endy Rodríguez')
        elif player_key == 'Yefry Ramirez':
            player = self.find_player('Yefry Ramírez')
        elif player_key == 'Rafael Marchan':
            player = self.find_player('Rafael Marchán')
        elif player_key == 'Vimael Machin':
            player = self.find_player('Vimael Machín')
        elif player_key == 'Ronald Bolanos':
            player = self.find_player('Ronald Bolaños')
        elif player_key == 'Deivy Grullon':
            player = self.find_player('Deivy Grullón')
        elif player_key == 'Cristopher Sanchez':
            player = self.find_player('Cristopher Sánchez')
        elif player_key == 'Carlos Estevez':
            player = self.find_player('Carlos Estévez')
        elif player_key == 'Jonathan Rodriguez':
            player = self.find_player('Jonathan Rodríguez')
        elif player_key == 'Leandro Cedeno':
            player = self.find_player('Leandro Cedeño')
        elif player_key == 'Albert Suarez':
            player = self.find_player('Albert Suárez')
        elif player_key == 'Yefri Perez':
            player = self.find_player('Yefri Pérez')
        elif player_key == 'Edgar Garcia':
            player = self.find_player('Edgar García')
        elif player_key == 'Miguel Gomez':
            player = self.find_player('Miguel Gómez')
        elif player_key == 'Rafael Martin':
            player = self.find_player('Rafael Martín')
        elif player_key == 'Humberto Mejia':
            player = self.find_player('Humberto Mejía')
        elif player_key == 'D\'Arby Myers':
            player = self.find_player('Johnni Turbo')
        elif player_key == 'Oscar Hernandez':
            player = self.find_player('Óscar Hernández')
        elif player_key == 'Yusniel Diaz':
            player = self.find_player('Yusniel Díaz')
        elif player_key == 'Eugenio Suarez':
            player = self.find_player('Eugenio Suárez')
        elif player_key == 'Julio Rodriguez':
            player = self.find_player('Julio Rodríguez')
        elif player_key == 'Nerwilian Cedeno':
            player = self.find_player('Nerwilian Cedeño')
        elif player_key == 'Marcel Renteria':
            player = self.find_player('Marcel Rentería')
        elif player_key == 'Roberto Perez':
            player = self.find_player('Roberto Pérez')
        elif player_key == 'Dayan Diaz':
            player = self.find_player('Dayan Díaz')
        elif player_key == 'Michael Harris':
            player = self.find_player('Michael Harris II')
        elif player_key == 'Luis Garcia':
            player = self.find_player('Luis García')
        elif player_key == 'Renato Nunez':
            player = self.find_player('Renato Núñez')
        elif player_key == 'Santiago Chavez':
            player = self.find_player('Santiago Chávez')
        elif player_key == 'Rodolfo Duran':
            player = self.find_player('Rodolfo Durán')
        elif player_key == 'Sandy Baez':
            player = self.find_player('Sandy Báez')
        elif player_key == 'Jose A.   Valdez':
            player = self.find_player('José A. Váldez')
        elif player_key == 'Wilderd Patino':
            player = self.find_player('Wilderd Patiño')
        elif player_key == 'Miguel Sanchez':
            player = self.find_player('Miguel Sánchez')
        elif player_key == 'Jonathan Loaisiga':
            player = self.find_player('Jonathan Loáisiga')
        elif player_key == 'Randy Rodriguez':
            player = self.find_player('Randy Rodríguez')
        elif player_key == 'Alexis Diaz':
            player = self.find_player('Alexis Díaz')
        elif player_key == 'Elias Diaz':
            player = self.find_player('Elias Díaz')
        elif player_key == 'Erik Gonzalez':
            player = self.find_player('Erik González')
        elif player_key == 'Omar Estevez':
            player = self.find_player('Omar Estévez')
        elif player_key == 'Carlos Corporan':
            player = self.find_player('Carlos Corporán')
        elif player_key == 'Ramon Vazquez':
            player = self.find_player('Ramón Vázquez')
        elif player_key == 'Xavier Cedeno':
            player = self.find_player('Xavier Cedeño')
        elif player_key == 'Hector Sanchez':
            player = self.find_player('Héctor Sánchez')
        elif player_key == 'Marco Hernandez':
            player = self.find_player('Marco Hernández')
        elif player_key == 'Jose Briceno':
            player = self.find_player('José Briceño')
        elif player_key == 'Pedro Araujo':
            player = self.find_player('Pedro Araújo')
        elif player_key == 'Luis Gonzalez':
            player = self.find_player('Luis González')
        elif player_key == 'Paco Rodriguez':
            player = self.find_player('Paco Rodríguez')
        elif player_key == 'Luis Avilan':
            player = self.find_player('Luis Avilán')
        elif player_key == 'Luis Urias':
            player = self.find_player('Luis Urías')
        elif player_key == 'Carlos Frias':
            player = self.find_player('Carlos Frías')
        elif player_key == 'Alfredo Gonzalez':
            player = self.find_player('Alfredo González')
        elif player_key == 'MoisÃ©s GÃ³mez':
            player = self.find_player('Moisés Gómez')
        elif player_key == 'Victor Alcantara':
            player = self.find_player('Victor Alcántara')
        elif player_key == 'Ricardo Rodriguez':
            player = self.find_player('Ricardo Rodríguez')
        elif player_key == 'Emilio Bonifacio':
            player = self.find_player('Emilio Bonifácio')
        elif player_key == 'Reynaldo Lopez':
            player = self.find_player('Reynaldo López')
        elif player_key == 'Yohan Ramirez':
            player = self.find_player('Yohan Ramírez')
        elif player_key == 'Hector Noesi':
            player = self.find_player('Hector Noesí')
        elif player_key == 'Jose Manuel Fernandez':
            player = self.find_player('José Manuel Fernández')
        elif player_key == 'Cionel Perez':
            player = self.find_player('Cionel Pérez')
        elif player_key == 'Jose Fermin':
            player = self.find_player('José Fermín')
        elif player_key == 'Andres Gimenez':
            player = self.find_player('Andrés Giménez')
        elif player_key == 'Aderlin Rodriguez':
            player = self.find_player('Aderlin Rodríguez')
        elif player_key == 'Anthony Garcia':
            player = self.find_player('Anthony García')
        elif player_key == 'Angel Sanchez':
            player = self.find_player('Angel Sánchez')
        elif player_key == 'Daniel Alvarez':
            player = self.find_player('Daniel Álvarez')
        elif player_key == 'Richard Rodriguez':
            player = self.find_player('Richard Rodríguez')
        elif player_key == 'Adrian Martinez':
            player = self.find_player('Adrián Martínez')
        elif player_key == 'Yerry Rodriguez':
            player = self.find_player('Yerry Rodríguez')
        elif player_key == 'Sean Rodriguez':
            player = self.find_player('Sean Rodríguez')
        elif player_key == 'Jhan Marinez':
            player = self.find_player('Jhan Mariñez')
        elif player_key == 'Gorkys Hernandez':
            player = self.find_player('Gorkys Hernández')
        elif player_key == 'Jhoulys Chacin':
            player = self.find_player('Jhoulys Chacín')
        elif player_key == 'Angel Pagan':
            player = self.find_player('Ángel Pagán')
        elif player_key == 'Richard RodrÃ­guez':
            player = self.find_player('Richard Rodríguez')
        elif player_key == 'Roenis Elias':
            player = self.find_player('Roenis Elías')
        elif player_key == 'Felipe VÃ¡zquez':
            player = self.find_player('Felipe Vázquez')
        elif player_key == 'Felipe Vazquez':
            player = self.find_player('Felipe Vázquez')
        elif player_key == 'Javier Baez':
            player = self.find_player('Javier Báez')
        elif player_key == 'Javier BÃ¡ez':
            player = self.find_player('Javier Báez')
        elif player_key == 'Cesar Hernandez':
            player = self.find_player('César Hernández')
        elif player_key == 'Ramon Urias':
            player = self.find_player('Ramón Urías')
        elif player_key == 'Audry Perez':
            player = self.find_player('Audry Pérez')
        elif player_key == 'Nasim Nunez':
            player = self.find_player('Nasim Nuñez')
        elif player_key == 'Jesmuel Valentin':
            player = self.find_player('Jesmuel Valentín')
        elif player_key == 'Jonathan Arauz':
            player = self.find_player('Jonathan Araúz')
        elif player_key == 'Yoelqui Cespedes':
            player = self.find_player('Yoelqui Céspedes')
        elif player_key == 'Pedro Leon':
            player = self.find_player('Pedro León')
        elif player_key == 'Oscar Colas':
            player = self.find_player('Oscar Colás')
        elif player_key == 'Chi Chi Gonzalez':
            player = self.find_player('Chi Chi González')
        elif player_key == 'Yolmer Sanchez':
            player = self.find_player('Yolmer Sánchez')
        elif player_key == 'Derian Gonzalez':
            player = self.find_player('Derian González')
        elif player_key == 'Roberto Pena':
            player = self.find_player('Roberto Peña')
        elif player_key == 'Luis Marte':
            player = self.find_player('Luis Marté')
        elif player_key == 'Hector Rondon':
            player = self.find_player('Héctor Rondón')
        elif player_key == 'Xavier Fernandez':
            player = self.find_player('Xavier Fernández')
        elif player_key == 'Jose Lopez':
            player = self.find_player('José López')
        elif player_key == 'Kevin Alcantara':
            player = self.find_player('Kevin Alcántara')
        elif player_key == 'Arodys Vizcaino':
            player = self.find_player('Arodys Vizcaíno')
        elif player_key == 'Christian Colon':
            player = self.find_player('Christian Colón')
        elif player_key == 'Aledmys Diaz':
            player = self.find_player('Aledmys Díaz')
        elif player_key == 'David Garcia':
            player = self.find_player('David García')
        elif player_key == 'Samir Duenez':
            player = self.find_player('Samir Dueñez')
        elif player_key == 'Edinson Vólquez':
            player = self.find_player('Edinson Volquez')
        elif player_key == 'Avisail Garcia':
            player = self.find_player('Avisaíl García')
        elif player_key == 'AvisaÃl GarcÃa':
            player = self.find_player('Avisaíl García')
        elif player_key == 'Adolis Garcia':
            player = self.find_player('Adolis García')
        elif player_key == 'Jose J.   De Los Santos':
            player = self.find_player('Jose De Los Santos')
        elif player_key == 'Dedniel Nunez':
            player = self.find_player('Dedniel Núñez')
        elif player_key == 'Elieser Hernandez':
            player = self.find_player('Elieser Hernández')
        elif player_key == 'Joely Rodriguez':
            player = self.find_player('Joely Rodríguez')
        elif player_key == 'Jairo Diaz':
            player = self.find_player('Jairo Díaz')
        elif player_key == 'Sixto Sanchez':
            player = self.find_player('Sixto Sánchez')
        elif player_key == 'Erasmo Ramirez':
            player = self.find_player('Erasmo Ramírez')
        elif player_key == 'Jaime Garcia':
            player = self.find_player('Jaime García')
        elif player_key == 'Jose Dominguez':
            player = self.find_player('José Domínguez')
        elif player_key == 'Jasson Dominguez':
            player = self.find_player('Jasson Domínguez')
        elif player_key == 'Jose Martinez':
            player = self.find_player('José Martínez')
        elif player_key == 'Williams Perez':
            player = self.find_player('Williams Pérez')
        elif player_key == 'Rayan Gonzalez':
            player = self.find_player('Rayan González')
        elif player_key == 'JC Ramirez':
            player = self.find_player('JC Ramírez')
        elif player_key == 'Yonny Hernandez':
            player = self.find_player('Yonny Hernández')
        elif player_key == 'Jose Yepez':
            player = self.find_player('José Yépez')
        elif player_key == 'Jose Ramirez':
            player = self.find_player('José Ramírez')
        elif player_key == 'Wilking Rodriguez':
            player = self.find_player('Wilking Rodríguez')
        elif player_key == 'Darien Nunez':
            player = self.find_player('Darien Núñez')
        elif player_key == 'Rony Garcia':
            player = self.find_player('Rony García')
        elif player_key == 'Cam Schlitter':
            player = self.find_player('Cam Schlittler')
        elif player_key == 'Pedro Pages':
            player = self.find_player('Pedro Pagés')
        elif player_key == 'Pedro Baez':
            player = self.find_player('Pedro Báez')
        elif player_key == 'Carlos Gomez':
            player = self.find_player('Carlos Gómez')
        elif player_key == 'Domingo German':
            player = self.find_player('Domingo Germán')
        elif player_key == 'Pablo Lopez':
            player = self.find_player('Pablo López')
        elif player_key == 'Andy Gonzalez':
            player = self.find_player('Andy González')
        elif player_key == 'Keinner Pina':
            player = self.find_player('Keinner Piña')
        elif player_key == 'Alex Colome':
            player = self.find_player('Alex Colomé')
        elif player_key == 'Enrique Hernandez':
            player = self.find_player('Enrique Hernández')
        elif player_key == 'Jhon Nunez':
            player = self.find_player('Jhon Nuñez')
        elif player_key == 'Ariel Pena':
            player = self.find_player('Ariel Peña')
        elif player_key == 'Ofreidy Gomez':
            player = self.find_player('Ofreidy Gómez')
        elif player_key == 'Yacksel RÃ­os':
            player = self.find_player('Yacksel Ríos')
        elif player_key == 'Hector Velazquez':
            player = self.find_player('Hector Velázquez')
        elif player_key == 'Andrew Perez':
            player = self.find_player('Andrew Pérez')
        elif player_key == 'Jorge Guzman':
            player = self.find_player('Jorge Guzmán')
        elif player_key == 'Jarlin Garcia':
            player = self.find_player('Jarlín García')
        elif player_key == 'Jonny Deluca':
            player = self.find_player('Jonny DeLuca')
        elif player_key == 'Mauricio Dubon':
            player = self.find_player('Mauricio Dubón')
        elif player_key == 'Jeison Guzman':
            player = self.find_player('Jeison Guzmán')
        elif player_key == 'Dom NuÃ±ez':
            player = self.find_player('Dom Nuñez')
        elif player_key == 'Manny Pina':
            player = self.find_player('Manny Piña')
        elif player_key == 'Jose Urena':
            player = self.find_player('José Ureña')
        elif player_key == 'Edwin Rios':
            player = self.find_player('Edwin Ríos')
        elif player_key == 'Roberto Gomez':
            player = self.find_player('Roberto Gómez')
        elif player_key == 'Felix Hernandez':
            player = self.find_player('Félix Hernández')
        elif player_key == 'Yoenis Céspedes':
            player = self.find_player('Yoenis Cespedes')
        elif player_key == 'Ronald Guzman':
            player = self.find_player('Ronald Guzmán')
        elif player_key == 'Jose Hernandez':
            player = self.find_player('José Hernández')
        elif player_key == 'Jose Butto':
            player = self.find_player('José Buttó')
        elif player_key == 'Vidal Nuno':
            player = self.find_player('Vidal Nuño')
        elif player_key == 'Randy Cesar':
            player = self.find_player('Randy César')
        elif player_key == 'Kevin Vicuna':
            player = self.find_player('Kevin Vicuña')
        elif player_key == 'Aaron Munoz':
            player = self.find_player('Aaron Muñoz')
        elif player_key == 'Leury Garcia':
            player = self.find_player('Leury García')
        elif player_key == 'Bengie Gonzalez':
            player = self.find_player('Bengie González')
        elif player_key == 'Jose Rodriguez':
            player = self.find_player('José Rodríguez')
        elif player_key == 'Manny Banuelos':
            player = self.find_player('Manny Bañuelos')
        elif player_key == 'Oscar Mercado':
            player = self.find_player('Óscar Mercado')
        elif player_key == 'Gio Gonzalez':
            player = self.find_player('Gio González')
        elif player_key == 'Sammy Solis':
            player = self.find_player('Sammy Solís')
        elif player_key == 'Yimi Garcia':
            player = self.find_player('Yimi García')
        elif player_key == 'Dereck Rodriguez':
            player = self.find_player('Dereck Rodríguez')
        elif player_key == 'Sandy Leon':
            player = self.find_player('Sandy León')
        elif player_key == 'Martin Perez':
            player = self.find_player('Martín Pérez')
        elif player_key == 'Adalberto Mejia':
            player = self.find_player('Adalberto Mejía')
        elif player_key == 'Luisangel Acuna':
            player = self.find_player('Luisangel Acuña')
        elif player_key == 'Isan Diaz':
            player = self.find_player('Isan Díaz')
        elif player_key == 'Anyelo Gomez':
            player = self.find_player('Anyelo Gómez')
        elif player_key == 'Ali Sanchez':
            player = self.find_player('Ali Sánchez')
        elif player_key == 'Carlos Gonzalez':
            player = self.find_player('Carlos González')
        elif player_key == 'Melvin Adon':
            player = self.find_player('Melvin Adón')
        elif player_key == 'Harol Gonzalez':
            player = self.find_player('Harol González')
        elif player_key == 'Harold Ramirez':
            player = self.find_player('Harold Ramírez')
        elif player_key == 'Dany Jimenez':
            player = self.find_player('Dany Jiménez')
        elif player_key == 'Francisco Pena':
            player = self.find_player('Francisco Peña')
        elif player_key == 'Seranthony Dominguez':
            player = self.find_player('Seranthony Domínguez')
        elif player_key == 'Jose Fernandez':
            player = self.find_player('José Fernández')
        elif player_key == 'David Rodriguez':
            player = self.find_player('David Rodríguez')
        elif player_key == 'Jose Sanchez':
            player = self.find_player('José Sánchez')
        elif player_key == 'Luis Patino':
            player = self.find_player('Luis Patiño')
        elif player_key == 'Joe Jimenez':
            player = self.find_player('Joe Jimenez')
        elif player_key == 'Ariel Hernandez':
            player = self.find_player('Ariel Hernández')
        elif player_key == 'Marcos Diplan':
            player = self.find_player('Marcos Diplán')
        elif player_key == 'Jeanmar Gomez':
            player = self.find_player('Jeanmar Gómez')
        elif player_key == 'Sergio AlcÃ¡ntara':
            player = self.find_player('Sergio Alcántara')
        elif player_key == 'Jack Lopez':
            player = self.find_player('Jack López')
        elif player_key == 'Delvin Perez':
            player = self.find_player('Delvin Pérez')
        elif player_key == 'Severino Gonzalez':
            player = self.find_player('Severino González')
        elif player_key == 'Eduardo Jimenez':
            player = self.find_player('Eduardo Jiménez')
        elif player_key == 'Buddy Reed':
            player = self.find_player('Michael Reed')
        elif player_key == 'Juan Gamez':
            player = self.find_player('Juan Gámez')
        elif player_key == 'Jumbo Diaz':
            player = self.find_player('Jumbo Díaz')
        elif player_key == 'Jorge Ona':
            player = self.find_player('Jorge Oña')
        elif player_key == 'Raul Alcantara':
            player = self.find_player('Raúl Alcántara')
        elif player_key == 'Adonis Garcia':
            player = self.find_player('Adonis García')
        elif player_key == 'Miguel Sano':
            player = self.find_player('Miguel Sanó')
        elif player_key == 'Eduardo Nunez':
            player = self.find_player('Eduardo Núñez')
        elif player_key == 'J.  P. Martinez':
            player = self.find_player('J.P. Martínez')
        elif player_key == 'JP Martinez':
            player = self.find_player('J.P. Martínez')
        elif player_key == 'J. C. Mejia':
            player = self.find_player('J.C. Mejía')
        elif player_key == 'Junior Fernandez':
            player = self.find_player('Junior Fernández')
        elif player_key == 'Jean Carlos Mejia':
            player = self.find_player('J.C. Mejía')
        elif player_key == 'German Marquez':
            player = self.find_player('Germán Márquez')
        elif player_key == 'Jose Miguel Fernandez':
            player = self.find_player('José Miguel Fernández')
        elif player_key == 'Ronald Acuna':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'J.  C. Mejia':
            player = self.find_player('J.C. Mejía')
        elif player_key == 'Nelson Velazquez':
            player = self.find_player('Nelson Velázquez')
        elif player_key == 'Ronald Acuna Jr.':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'Ronald Acuna Jr':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'Christian Vazquez':
            player = self.find_player('Christian Vázquez')
        elif player_key == 'Julio Pablo Martinez':
            player = self.find_player('J.P. Martínez')
        elif player_key == 'Jake Gatewood':
            player = self.find_player('Henry Gatewood')
        elif player_key == 'Ronald AcuÃ±a Jr.':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'Yender Caramo':
            player = self.find_player('Yender Cáramo')
        elif player_key == 'Ivan de Jesus':
            player = self.find_player('Iván De Jesús Jr.')
        elif player_key == 'Ivan De Jesus':
            player = self.find_player('Iván De Jesús Jr.')
        elif player_key == 'Bryant Elliott':
            player = self.find_player('Bryant Elliot')
        elif player_key == 'Carlos Martinez':
            player = self.find_player('Carlos Martínez')
        elif player_key == 'Carlos Martínez':
            player = self.find_player('Carlos Martinez')
        elif player_key == 'Joe Jimenez':
            player = self.find_player('Joe Jimenez')
        elif player_key == 'Jhon NuÃ±ez':
            player = self.find_player('Jhon Nuñez')
        elif player_key == 'Ronald Pena':
            player = self.find_player('Ronald Peña')
        elif player_key == 'CÃ©sar HernÃ¡ndez':
            player = self.find_player('César Hernández')
        elif player_key == 'Franklin Perez':
            player = self.find_player('Franklin Pérez')
        elif player_key == 'Jonathan LoÃ¡isiga':
            player = self.find_player('Jonathan Loáisiga')
        elif player_key == 'Daysbel Hernandez':
            player = self.find_player('Daysbel Hernández')
        elif player_key == 'Michael Harris':
            player = self.find_player('Michael Harris II')
        elif player_key == 'Raffi Vizcaino':
            player = self.find_player('Raffi Vizcaíno')
        elif player_key == 'Raffi VizcaÃno':
            player = self.find_player('Raffi Vizcaíno')
        elif player_key == 'BJ Lopez':
            player = self.find_player('B.J. López')
        elif player_key == 'B.  J. Lopez':
            player = self.find_player('B.J. López')
        elif player_key == 'B. J. Lopez':
            player = self.find_player('B.J. López')
        elif player_key == 'Julio Eusebio':
            player = self.find_player('Ricky Eusebio')
        elif player_key == 'Miller Diaz':
            player = self.find_player('Miller Díaz')
        elif player_key == 'Danny De La Calle':
            player = self.find_player('Daniel De La Calle')
        elif player_key == 'Gary SÃ¡nchez':
            player = self.find_player('Gary Sánchez')
        elif player_key == 'Chris Alleyne':
            player = self.find_player('Bubba Alleyne')
        elif player_key == 'Kike Hernandez':
            player = self.find_player('Enrique Hernández')
        elif player_key == 'Robert Zarate':
            player = self.find_player('Robert Zárate')
        elif player_key == 'FÃ©lix PeÃ±a':
            player = self.find_player('Félix Peña')
        elif player_key == 'Norel Gonzalez':
            player = self.find_player('Norel González')
        elif player_key == 'Mandy Alvarez':
            player = self.find_player('Armando Alvarez')
        elif player_key == 'Jose A.   Valdez':
            player = self.find_player('José A. Váldez')
        elif player_key == 'Jose A. Valdez':
            player = self.find_player('José A. Váldez')
        elif player_key == 'Alexander Vizcaino':
            player = self.find_player('Alexander Vizcaíno')
        elif player_key == 'Ramon Rodriguez':
            player = self.find_player('Ramón Rodríguez')
        elif player_key == 'Jonathan Rodriguez':
            player = self.find_player('Johnathan Rodriguez')
        elif player_key == 'Eric Marinez':
            player = self.find_player('Eric Mariñez')
        elif player_key == 'Bryant Elliott':
            player = self.find_player('Bryant Elliot')
        elif player_key == 'Angel Lopez Alvarez':
            player = self.find_player('Angel Lopez')
        elif player_key == 'Norwith Gudino':
            player = self.find_player('Norwith Gudiño')
        elif player_key == 'Carlos Sanchez':
            player = self.find_player('Yolmer Sánchez')
        elif player_key == 'Jack Lopez':
            player = self.find_player('Jack López')
        elif player_key == 'Jack LÃ³pez':
            player = self.find_player('Jack López')
        elif player_key == 'Roddery Munoz':
            player = self.find_player('Roddery Muñoz')
        elif player_key == 'Gerardo Concepcion':
            player = self.find_player('Gerardo Concepción')
        elif player_key == 'Danuerys De La Cruz':
            player = self.find_player('Daneurys De La Cruz')
        elif player_key == 'Jose Lopez':
            player = self.find_player('José Lopez')
        elif player_key == 'Jimmy CrooksI':
            player = self.find_player('Jimmy Crooks')
        elif player_key == 'Li-Jen Chu':
            player = self.find_player('Kungkuan Giljegiljaw')
        elif player_key == 'Reshard Munroe':
            player = self.find_player('Shard Munroe')
        elif player_key == 'Andres Nunez':
            player = self.find_player('Andrés Núñez')
        elif player_key == 'Elniery Garcia':
            player = self.find_player('Elniery García')
        elif player_key == 'Malcom Nunez':
            player = self.find_player('Malcom Nuñez')
        elif player_key == 'Jose Garcia':
            player = self.find_player('Jose Barrero')
        elif player_key == 'Richelson Pena':
            player = self.find_player('Richelson Peña')
        elif player_key == 'Ignacio Alvarez':
            player = self.find_player('Nacho Alvarez Jr.')
        elif player_key == 'Nelson VelÃ¡zquez':
            player = self.find_player('Nelson Velázquez')
        elif player_key == 'Nelson Velazquez':
            player = self.find_player('Nelson Velázquez')
        elif player_key == 'J.P. Martinez':
            player = self.find_player('J.P. Martínez')
        elif player_key == 'Luis GarcÃa':
            player = self.find_player('Luis García')
        elif player_key == 'Luis Garcia Jr.':
            player = self.find_player('Luis García Jr.')
        elif player_key == 'J. P. Martinez':
            player = self.find_player('J.P. Martínez')
        elif player_key == 'Ronald Acuna Jr. ':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'Ronald Acuna Jr.':
            player = self.find_player('Ronald Acuña Jr.')
        elif player_key == 'Michael Harris':
            player = self.find_player('Michael Harris II')
        elif player_key == 'JT Realmuto':
            player = self.find_player('J.T. Realmuto')
        elif player_key == 'Yariel Rodriguez':
            player = self.find_player('Yariel Rodríguez')
        elif player_key == 'Josue Briceno':
            player = self.find_player('Josue Briceño')

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


class Game:
    def __init__(self, home_team, away_team, location, game_date_str):
        self.home_team = home_team
        self.away_team = away_team
        self.location = location or ''
        self.game_date_str = game_date_str

        self.start_datetime = None
        self.end_datetime = None
        self.inning_list = []
        self.away_batter_box_score_dict = None
        self.home_batter_box_score_dict = None
        self.away_pitcher_box_score_dict = None
        self.home_pitcher_box_score_dict = None
        self.away_team_stats = None
        self.home_team_stats = None
        self.attendance = None
        self.temp = None
        self.weather = None
        self.expected_start_datetime = None
        self.timezone_str = EASTERN_TIMEZONE_STR
        self.is_postponed = False
        self.is_suspended = False
        self.is_doubleheader = False
        self.is_today = True

    def json(self):
        return dumps(self._asdict())

    @staticmethod
    def denormalize_box_score_dict(box_score_dict):
        tuple_list = []
        for x, y in box_score_dict.items():
            if isinstance(x, str):
                value = x
            elif isinstance(x, Player):
                value = x._asdict()
            else:
                raise ValueError('Wrong type.')

            tuple_list.append((value, y._asdict()))

        return tuple_list

    def _asdict(self):
        return (
            {'home_team': self.home_team._asdict(),
             'away_team': self.away_team._asdict(),
             'location': self.location,
             'game_date_str': self.game_date_str,
             'start_datetime': str(self.start_datetime),
             'end_datetime': str(self.end_datetime),
             'inning_list': [x._asdict() for x in self.inning_list],
             'away_batter_box_score_dict': self.denormalize_box_score_dict(
                 self.away_batter_box_score_dict
             ),
             'home_batter_box_score_dict': self.denormalize_box_score_dict(
                 self.home_batter_box_score_dict
             ),
             'away_pitcher_box_score_dict': self.denormalize_box_score_dict(
                 self.away_pitcher_box_score_dict
             ),
             'home_pitcher_box_score_dict': self.denormalize_box_score_dict(
                 self.home_pitcher_box_score_dict
             ),
             'away_team_stats': self.away_team_stats._asdict(),
             'home_team_stats': self.home_team_stats._asdict(),
             'attendance': self.attendance,
             'temp': self.temp,
             'weather': self.weather,
             'expected_start_datetime': str(self.expected_start_datetime),
             'timezone_str': self.timezone_str}
        )

    def get_svg_str(self):
        return get_game_svg_str(self)

    def set_gametimes(self):
        for ballpark, this_timezone in STADIUM_TIMEZONE_DICT.items():
            if ballpark in self.location:
                self.timezone_str = this_timezone

        if not self.start_datetime:
            if self.inning_list:
                if self.inning_list[0].top_half_appearance_list:
                    self.start_datetime = (
                        self.inning_list[0].top_half_appearance_list[0].end_datetime
                    )

        if not self.end_datetime:
            if self.inning_list:
                last_inning_half_appearance_list = (
                    self.inning_list[-1].bottom_half_appearance_list or
                    self.inning_list[-1].top_half_appearance_list
                )

                if last_inning_half_appearance_list:
                    self.end_datetime = (
                        last_inning_half_appearance_list[-1].end_datetime
                    )

    def set_pitching_box_score_dict(self):
        self.away_pitcher_box_score_dict = OrderedDict([])
        self.home_pitcher_box_score_dict = OrderedDict([])

        tuple_list = [
            (self.away_pitcher_box_score_dict, self.away_team, 'bottom'),
            (self.home_pitcher_box_score_dict, self.home_team, 'top'),
        ]

        for box_score_dict, team, inning_half_str in tuple_list:
            for pitcher_appearance in team.pitcher_list:
                pitcher = pitcher_appearance.player_obj
                box_score_dict[pitcher] = (
                    get_all_pitcher_stats(self, team, pitcher, inning_half_str)
                )

    def set_batting_box_score_dict(self):
        self.away_batter_box_score_dict = OrderedDict([])
        self.home_batter_box_score_dict = OrderedDict([])

        tuple_list = [
            (self.away_batter_box_score_dict, self.away_team, 'top'),
            (self.home_batter_box_score_dict, self.home_team, 'bottom'),
        ]

        for box_score_dict, team, inning_half_str in tuple_list:
            for batting_order_list in team.batting_order_list_list:
                for batter_appearance in batting_order_list:
                    batter = batter_appearance.player_obj
                    if batter not in box_score_dict:
                        box_score_dict[batter] = (
                            get_all_batter_stats(self, batter, inning_half_str)
                        )

            box_score_dict['TOTAL'] = get_box_score_total(box_score_dict)

    def set_team_stats(self):
        self.away_team_stats = get_team_stats(self, 'top')
        self.home_team_stats = get_team_stats(self, 'bottom')

    def __repr__(self):
        return_str = '{}\n'.format(self.location)
        if self.start_datetime and self.end_datetime:
            start_str = self.start_datetime.astimezone(
                timezone(self.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p')

            end_str = self.end_datetime.astimezone(
                timezone(self.timezone_str)
            ).strftime(' - %-I:%M %p %Z')

            return_str += '{}{}\n\n'.format(start_str, end_str)
        else:
            return_str += '{}\n\n'.format(self.game_date_str)

        dict_list = [self.away_batter_box_score_dict,
                     self.away_pitcher_box_score_dict,
                     self.home_batter_box_score_dict,
                     self.home_pitcher_box_score_dict]

        for this_dict in dict_list:
            for name, tup in this_dict.items():
                return_str += '{!s:20s} {}\n'.format(name, str(tup))

            return_str += '\n'

        return_str += 'Away Team ({}): {}\nHome Team ({}): {}\n'.format(
            self.away_batter_box_score_dict['TOTAL'].R,
            str(self.away_team_stats),
            self.home_batter_box_score_dict['TOTAL'].R,
            str(self.home_team_stats)
        )

        return_str += '{}AT\n\n{}'.format(
            self.away_team,
            self.home_team
        )

        for i, inning in enumerate(self.inning_list):
            inning_number = i + 1
            return_str += (
                (' ' * 33) + '############\n' +
                (' ' * 33) + '# INNING {} #\n' +
                (' ' * 33) + '############\n\n{}\n\n'
            ).format(
                inning_number,
                inning
            )

        return return_str


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
