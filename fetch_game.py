from datetime import timedelta
from math import ceil
from multiprocessing import Process, Manager
from os import listdir
from os.path import isdir, isfile, exists, abspath
from sys import argv
from xml.etree.ElementTree import fromstring

from dateutil.parser import parse
from requests import get

from process_game_xml import MLB_TEAM_CODE_DICT, get_game_obj


NUM_PROCESS_SUBLISTS = 16
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
GAME_SUFFIX = 'inning/inning_all.xml'

MLB_URL_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                   'month_{month}/day_{day}/gid_{year}_{month}_{day}_'
                   '{away_mlb_code}mlb_{home_mlb_code}mlb_{game_number}/')

GET_XML_USAGE_STR = ('Usage:\n'
                     '  - ./fetch_game.py url [DATE] [AWAY CODE] [HOME CODE] '
                     '[GAME NUMBER]\n'
                     '  - ./fetch_game.py files [START DATE] [END DATE] '
                     '[INPUT DIRECTORY]\n')


def get_formatted_date_str(input_date_str):
    this_date = parse(input_date_str)
    this_date_str = '{}-{}-{}'.format(str(this_date.year),
                                      str(this_date.month).zfill(2),
                                      str(this_date.day).zfill(2))

    return this_date_str

def get_list_of_lists(this_list, num_lists):
    chunk_size = int(ceil(len(this_list) / float(num_lists)))
    return [this_list[i:i+chunk_size]
            for i in range(0, len(this_list), chunk_size)]

def get_filename_list(start_date_str, end_date_str, input_path):
    filename_list = []
    start_date = parse(start_date_str)
    end_date = parse(end_date_str)
    day_delta = timedelta(days=1)
    this_date = start_date
    while this_date < end_date + day_delta:
        year = str(this_date.year)
        month = str(this_date.month).zfill(2)
        day = str(this_date.day).zfill(2)
        filename = '{}/{}/month_{}/day_{}/'.format(input_path, year, month, day)
        if isdir(filename):
            file_list = listdir(filename)
            if file_list:
                for subfile in file_list:
                    if subfile.startswith('gid_'):
                        away_code, home_code, game_num = subfile.split('_')[-3:]
                        away_code = away_code[:-3]
                        home_code = home_code[:-3]
                        away_team, home_team = None, None
                        for key, value in MLB_TEAM_CODE_DICT.items():
                            if value == away_code:
                                away_team = key

                            if value == home_code:
                                home_team = key

                        if away_team and home_team:
                            output_name = '-'.join([year, month, day, away_team,
                                                    home_team, game_num])

                            subfolder_name = filename + subfile + '/'
                            if listdir(subfolder_name):
                                player_filename = subfolder_name + 'players.xml'
                                boxscore_filename = (subfolder_name +
                                                     'boxscore.xml')

                                inning_filename = (subfolder_name +
                                                   'inning/inning_all.xml')

                                filename_list.append((output_name,
                                                      boxscore_filename,
                                                      player_filename,
                                                      inning_filename))

        this_date += day_delta

    return filename_list

def get_input_path(input_dir):
    if not exists(input_dir):
        raise ValueError('Invalid input directory')

    input_path = abspath(input_dir)

    return input_path

def get_game_from_files(boxscore_file, player_file, inning_file):
    this_game = None
    if (isfile(boxscore_file) and isfile(player_file) and isfile(inning_file)):
        boxscore_raw = open(boxscore_file, 'r', encoding='utf-8').read()
        boxscore_xml = fromstring(boxscore_raw)
        player_raw = open(player_file, 'r', encoding='utf-8').read()
        player_xml = fromstring(player_raw)
        inning_raw = open(inning_file, 'r', encoding='utf-8').read()
        inning_xml = fromstring(inning_raw)
        this_game = get_game_obj(boxscore_xml, player_xml, inning_xml)

    return this_game

def get_game_generator(filename_list):
    for game_id, boxscore_file, player_file, inning_file in filename_list:
        this_game = get_game_from_files(boxscore_file, player_file, inning_file)
        if this_game:
            yield game_id, this_game

def get_game_sublist(filename_list, return_queue):
    game_sublist = [game_tup for game_tup in get_game_generator(filename_list)]
    return_queue.put(game_sublist)

def get_game_list_from_file_range(start_date_str, end_date_str, input_dir):
    input_path = get_input_path(input_dir)
    filename_list = get_filename_list(start_date_str, end_date_str, input_path)

    manager = Manager()
    return_queue = manager.Queue()
    list_of_filename_lists = get_list_of_lists(filename_list,
                                               NUM_PROCESS_SUBLISTS)

    job_list = []
    for filename_list in list_of_filename_lists:
        process = Process(target=get_game_sublist,
                          args=(filename_list, return_queue))

        job_list.append(process)
        process.start()

    for job in job_list:
        job.join()

    game_tuple_list = []
    while not return_queue.empty():
        game_tuple_list.extend(return_queue.get())

    return game_tuple_list

def get_game_generator_from_file_range(start_date_str, end_date_str, input_dir):
    input_path = get_input_path(input_dir)
    filename_list = get_filename_list(start_date_str, end_date_str, input_path)
    for game_id, game in get_game_generator(filename_list):
        yield game_id, game

def print_list_from_file_range(start_date_str, end_date_str, input_dir):
    game_generator = get_game_generator_from_file_range(start_date_str,
                                                        end_date_str,
                                                        input_dir)

    for game_id, game in game_generator:
        print(game_id)
        print(game)

def get_game_xml_data(date, away_team_code, home_team_code, game_number):
    request_url_base = MLB_URL_PATTERN.format(
        year=date.year,
        month=str(date.month).zfill(2),
        day=str(date.day).zfill(2),
        away_mlb_code=MLB_TEAM_CODE_DICT[away_team_code],
        home_mlb_code=MLB_TEAM_CODE_DICT[home_team_code],
        game_number=game_number
    )

    boxscore_request_text = get(request_url_base + BOXSCORE_SUFFIX).text

    if boxscore_request_text == 'GameDay - 404 Not Found':
        boxscore_raw_xml, team_raw_xml, game_raw_xml = None, None, None
    else:
        boxscore_raw_xml = fromstring(boxscore_request_text)
        team_raw_xml = fromstring(
            get(request_url_base + PLAYERS_SUFFIX).text
        )

        game_raw_xml = fromstring(
            get(request_url_base + GAME_SUFFIX).text
        )

    return boxscore_raw_xml, team_raw_xml, game_raw_xml

def get_game_from_url(date_str, away_code, home_code, game_num):
    formatted_date_str = get_formatted_date_str(date_str)
    game_id = '-'.join(
        [formatted_date_str, away_code, home_code, str(game_num)]
    )

    date = parse(formatted_date_str)
    boxscore_xml, team_xml, game_xml = get_game_xml_data(date,
                                                         away_code,
                                                         home_code,
                                                         game_num)

    if boxscore_xml:
        this_game = get_game_obj(boxscore_xml, team_xml, game_xml)
    else:
        this_game = None
        print('No data found for {} {} {} {}'.format(date_str,
                                                     away_code,
                                                     home_code,
                                                     game_num))

    return game_id, this_game

def print_from_url(date_str, away_code, home_code, game_num):
    game_id, this_game = get_game_from_url(
        date_str, away_code, home_code, game_num
    )

    if this_game:
        print(game_id)
        print(this_game)

if __name__ == '__main__':
    if len(argv) < 3:
        print(GET_XML_USAGE_STR)
        exit()
    if argv[1] == 'files' and len(argv) == 5:
        print_list_from_file_range(argv[2], argv[3], argv[4])
    elif argv[1] == 'url' and len(argv) == 6:
        print_from_url(argv[2], argv[3], argv[4], argv[5])
    else:
        print(GET_XML_USAGE_STR)
