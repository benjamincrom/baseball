import datetime
import os
import re
import sys

import requests

import constants
import generate_svg

def get_page(today):
    page = requests.get(
        constants.MLB_URL_BASE_PATTERN.format(year=today.year,
                                              month=str(today.month).zfill(2),
                                              day=str(today.day).zfill(2))
    )

    return page

def get_today_date_str(today):
    today_date_str = '{}-{}-{}'.format(today.year,
                                       str(today.month).zfill(2),
                                       str(today.day).zfill(2))

    return today_date_str

def get_html_id_list(game_id_list, today_date_str, output_dir):
    game_html_id_list = []
    for game_id in game_id_list:
        away_mlb_code = game_id.split('_')[-3][:3]
        home_mlb_code = game_id.split('_')[-2][:3]
        game_num_str = game_id.split('_')[-1]

        if (away_mlb_code in constants.MLB_TEAM_CODE_DICT.values() and
                home_mlb_code in constants.MLB_TEAM_CODE_DICT.values()):
            away_code = [key for key, val in constants.MLB_TEAM_CODE_DICT.items()
                         if val == away_mlb_code][0]
            home_code = [key for key, val in constants.MLB_TEAM_CODE_DICT.items()
                         if val == home_mlb_code][0]

            success = generate_svg.generate_from_url(today_date_str,
                                                     away_code,
                                                     home_code,
                                                     game_num_str,
                                                     output_dir)

            if success:
                game_html_id_list.append(
                    '{}-{}-{}-{}'.format(today_date_str,
                                         away_code,
                                         home_code,
                                         game_num_str)
                )

    return game_html_id_list

def get_object_html_str(game_html_id_list):
    object_html_str = ''
    for game_html_id in game_html_id_list:
        game_id_element_list = game_html_id.split('-')
        title_str = '{} @ {} ({}-{}-{}, {})'.format(
            game_id_element_list[3],
            game_id_element_list[4],
            game_id_element_list[0],
            game_id_element_list[1],
            game_id_element_list[2],
            game_id_element_list[5]
        )
        object_html_str += constants.OBJECT_ENTRY_TEMPLATE.format(
            title_str=title_str,
            game_id_str=game_html_id
        )

    return object_html_str

def get_today_games(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    time_shift = datetime.timedelta(hours=11)
    today = datetime.datetime.utcnow() - time_shift

    today_date_str = get_today_date_str(today)
    page = get_page(today)

    game_id_list = re.findall(r'>\s*(gid\_\w+)/<', page.text)
    game_html_id_list = get_html_id_list(game_id_list, today_date_str,
                                         output_dir)

    object_html_str = get_object_html_str(game_html_id_list)
    output_html = constants.HTML_INDEX_PAGE.format(
        result_object_list_str=object_html_str
    )

    if object_html_str or not os.path.exists(output_dir + '/index.html'):
        with open(output_dir + '/index.html', 'w', encoding='utf-8') as filehandle:
            filehandle.write(output_html)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(constants.GET_TODAY_GAMES_USAGE_STR)
    else:
        get_today_games(sys.argv[1])
