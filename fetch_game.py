import datetime
import multiprocessing
import os
import sys
import xml.etree.ElementTree

import requests
import dateutil.parser

import constants
import process_game_xml


def get_list_of_lists(this_list, size):
    if len(this_list) % size:
        size -= 1

    chunk_size = len(this_list) // size
    return [this_list[i:i+chunk_size]
            for i in range(0, len(this_list), chunk_size)]

def get_filename_list(start_date_str, end_date_str, input_path):
    filename_list = []
    start_date = dateutil.parser.parse(start_date_str)
    end_date = dateutil.parser.parse(end_date_str)
    day_delta = datetime.timedelta(days=1)
    this_date = start_date
    while this_date < end_date + day_delta:
        year = str(this_date.year)
        month = str(this_date.month).zfill(2)
        day = str(this_date.day).zfill(2)
        filename = '{}/{}/month_{}/day_{}/'.format(input_path, year, month, day)
        if os.path.isdir(filename):
            file_list = os.listdir(filename)
            if file_list:
                for subfile in file_list:
                    if subfile.startswith('gid_'):
                        away_code, home_code, game_num = subfile.split('_')[-3:]
                        away_code = away_code[:-3]
                        home_code = home_code[:-3]
                        away_team, home_team = None, None
                        for key, value in constants.MLB_TEAM_CODE_DICT.items():
                            if value == away_code:
                                away_team = key

                            if value == home_code:
                                home_team = key

                        if away_team and home_team:
                            output_name = (
                                '-'.join([year, month, day, away_team,
                                          home_team, game_num])
                            )

                            subfolder_name = filename + subfile + '/'
                            if os.listdir(subfolder_name):
                                boxscore_filename = (
                                    subfolder_name + 'boxscore.xml'
                                )
                                player_filename = subfolder_name + 'players.xml'
                                inning_filename = (
                                    subfolder_name + 'inning/inning_all.xml'
                                )

                                filename_list.append((output_name,
                                                      boxscore_filename,
                                                      player_filename,
                                                      inning_filename))

        this_date += day_delta

    return filename_list

def get_game_sublist(filename_list, return_queue):
    game_sublist = []
    for filename, boxscore, player, inning in filename_list:
        if (os.path.isfile(boxscore) and
                os.path.isfile(player) and
                os.path.isfile(inning)):
            boxscore_raw = open(boxscore, 'r', encoding='utf-8').read()
            boxscore_xml = xml.etree.ElementTree.fromstring(boxscore_raw)
            player_raw = open(player, 'r', encoding='utf-8').read()
            player_xml = xml.etree.ElementTree.fromstring(player_raw)
            inning_raw = open(inning, 'r', encoding='utf-8').read()
            inning_xml = xml.etree.ElementTree.fromstring(inning_raw)
            this_game = process_game_xml.get_game_obj(
                boxscore_xml, player_xml, inning_xml
            )
            print('Processed: {}'.format(filename))

            game_sublist.append((filename, this_game))

    return_queue.put(game_sublist)

def get_game_list_from_files(start_date_str, end_date_str, input_dir):
    if not os.path.exists(input_dir):
        raise ValueError('Invalid input directory')

    input_path = os.path.abspath(input_dir)
    manager = multiprocessing.Manager()
    return_queue = manager.Queue()
    filename_list = get_filename_list(start_date_str, end_date_str, input_path)
    list_of_filename_lists = get_list_of_lists(filename_list,
                                               constants.NUM_SUBLISTS)

    job_list = []
    for filename_list in list_of_filename_lists:
        process = multiprocessing.Process(
            target=get_game_sublist,
            args=(filename_list, return_queue)
        )

        job_list.append(process)
        process.start()

    for job in job_list:
        job.join()

    game_list = []
    while not return_queue.empty():
        game_list.extend(return_queue.get())

    return game_list

def generate_from_files(start_date_str, end_date_str, input_dir):
    game_list = get_game_list_from_files(start_date_str,
                                         end_date_str,
                                         input_dir)

    for filename, game in game_list:
        print(filename)
        print(game)

def get_formatted_date_str(input_date_str):
    this_date = dateutil.parser.parse(input_date_str)
    this_date_str = '{}-{}-{}'.format(str(this_date.year),
                                      str(this_date.month).zfill(2),
                                      str(this_date.day).zfill(2))

    return this_date_str

def get_game_xml_data(date, away_team_code, home_team_code, game_number):
    request_url_base = constants.MLB_URL_PATTERN.format(
        year=date.year,
        month=str(date.month).zfill(2),
        day=str(date.day).zfill(2),
        away_mlb_code=constants.MLB_TEAM_CODE_DICT[away_team_code],
        home_mlb_code=constants.MLB_TEAM_CODE_DICT[home_team_code],
        game_number=game_number
    )

    boxscore_request_text = requests.get(
        request_url_base + constants.BOXSCORE_SUFFIX
    ).text

    if boxscore_request_text == 'GameDay - 404 Not Found':
        boxscore_raw_xml, team_raw_xml, game_raw_xml = None, None, None
    else:
        boxscore_raw_xml = xml.etree.ElementTree.fromstring(
            boxscore_request_text
        )

        team_raw_xml = xml.etree.ElementTree.fromstring(
            requests.get(request_url_base + constants.PLAYERS_SUFFIX).text
        )

        game_raw_xml = xml.etree.ElementTree.fromstring(
            requests.get(request_url_base + constants.GAME_SUFFIX).text
        )

    return boxscore_raw_xml, team_raw_xml, game_raw_xml

def get_game_from_url(date_str, away_code, home_code, game_num):
    formatted_date_str = get_formatted_date_str(date_str)
    game_id = '-'.join(
        [formatted_date_str, away_code, home_code, str(game_num)]
    )

    date = dateutil.parser.parse(formatted_date_str)
    boxscore_xml, team_xml, game_xml = get_game_xml_data(date,
                                                         away_code,
                                                         home_code,
                                                         game_num)

    if boxscore_xml:
        this_game = process_game_xml.get_game_obj(boxscore_xml, team_xml, game_xml)
    else:
        this_game = None

    return game_id, this_game

def generate_from_url(date_str, away_code, home_code, game_num):
    game_id, this_game = get_game_from_url(
        date_str, away_code, home_code, game_num
    )

    if this_game:
        print(game_id)
        print(this_game)
        status = True
    else:
        print('No data found for {} {} {} {}'.format(date_str,
                                                     away_code,
                                                     home_code,
                                                     game_num))

        status = False

    return status

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(constants.GET_XML_USAGE_STR)
        exit()
    if sys.argv[1] == 'files' and len(sys.argv) == 5:
        generate_from_files(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'url' and len(sys.argv) == 6:
        generate_from_url(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print(constants.GET_XML_USAGE_STR)
