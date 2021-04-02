from datetime import timedelta, datetime
from multiprocessing import Pool
from os import listdir, makedirs
from os.path import isdir, isfile, exists, abspath, join
from xml.etree.ElementTree import fromstring

from dateutil.parser import parse
from requests import get

from baseball.process_game_xml import MLB_TEAM_CODE_DICT, get_game_obj


NUM_PROCESS_SUBLISTS = 3
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
INNING_SUFFIX = 'inning/inning_all.xml'

MLB_URL_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                   'month_{month}/day_{day}/gid_{year}_{month}_{day}_'
                   '{away_mlb_code}mlb_{home_mlb_code}mlb_{game_number}/')

HTML_WRAPPER = (
    '<html>'
    '<head>'
    '<title>{title}</title>'
    '<link rel="icon" type="image/png" href="baseball-fairy-161.png" />'
    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/'
    'jquery.min.js"></script>'
    '<!-- Global site tag (gtag.js) - Google Analytics -->'
    '<script async src="https://www.googletagmanager.com/gtag/js?'
    'id=UA-108577160-1"></script>'
    '<script>'
    'window.dataLayer = window.dataLayer || [];function gtag()'
    '{{dataLayer.push(arguments);}}gtag(\'js\', new Date());gtag'
    '(\'config\', \'UA-108577160-1\');'
    '</script>'
    '<script>'
    '$(document).ready(function() {{'
    '$.get(\'{filename}\', function (data) {{'
    'document.getElementById("{title}").innerHTML = '
    'new XMLSerializer().serializeToString(data.documentElement);'
    '}});'
    'setInterval(function() {{'
    '$.get(\'{filename}\', function (data) {{'
    'document.getElementById("{title}").innerHTML = '
    'new XMLSerializer().serializeToString(data.documentElement);'
    '}});'
    '}}, 3000); '
    '}});'
    '</script>'
    '<script>'
    '(function(h,o,u,n,d) {{ '
    'h=h[d]=h[d]||{{q:[],onReady:function(c){{h.q.push(c)}}}} \n'
    'd=o.createElement(u);d.async=1;d.src=n \n'
    'n=o.getElementsByTagName(u)[0];n.parentNode.insertBefore(d,n) '
    '}})(window,document,\'script\',\'https://www.datadoghq-browser-agent.com/datadog-rum.js\',\'DD_RUM\')\n'
    'DD_RUM.onReady(function() {{ '
    'DD_RUM.init({{ '
    'clientToken: \'pubddae1190ff21ff570dd36eaffc141c4d\', '
    'applicationId: \'8d72601e-b047-42da-af09-1ab422e756fa\', '
    'site: \'datadoghq.com\', '
    'service:\'get-todays-games\', '
    'env:\'none\', '
    'sampleRate: 100, '
    'trackInteractions: true, '
    '}})'
    '}})'
    '</script>'
    '</head>'
    '<body style="background-color:black;">'
    '<div align="center">'
    '<object width="1160px" id="{title}"></object>'
    '</div>'
    '</body>'
    '</html>'
)

HTML_WRAPPER_OLD = (
    '<html>'
    '<head>'
    '<meta http-equiv="refresh" content="45">'
    '<meta name="viewport" content="width=device-width, initial-scale=0.35">'
    '<link rel="icon" type="image/png" href="baseball-fairy-161.png" />'
    '<!-- Global site tag (gtag.js) - Google Analytics -->'
    '<script async '
    'src="https://www.googletagmanager.com/gtag/js?id=UA-108577160-1"></script>'
    '<script>'
    'window.dataLayer = window.dataLayer || [];'
    'function gtag(){{dataLayer.push(arguments);}}'
    'gtag(\'js\', new Date());'
    'gtag(\'config\', \'UA-108577160-1\');'
    '</script>'
    '<title>{title}</title>'
    '</head>'
    '<body style="background-color:black;">'
    '<div align="center">'
    '<object width="1160px" data="{filename}" type="image/svg+xml">'
    '</div>'
    '</body>'
    '</html>'
)


def get_formatted_date_str(input_date_str):
    this_date = parse(input_date_str)
    this_date_str = '{}-{}-{}'.format(str(this_date.year),
                                      str(this_date.month).zfill(2),
                                      str(this_date.day).zfill(2))

    return this_date_str

def write_game_svg_and_html(game_id, game, output_path):
    svg_filename = game_id + '.svg'
    html_filename = game_id + '.html'

    svg_text = game.get_svg_str()
    html_text = HTML_WRAPPER.format(title=game_id, filename=svg_filename)

    output_svg_path = join(output_path, svg_filename)
    output_html_path = join(output_path, html_filename)

    with open(output_svg_path, 'w') as filehandle:
        filehandle.write(svg_text)

    with open(output_html_path, 'w') as filehandle:
        filehandle.write(html_text)

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

def get_game_from_filename_tuple(filename_tuple):
    game_id, boxscore_file, player_file, inning_file = filename_tuple
    game = get_game_from_files(boxscore_file, player_file, inning_file)

    return game_id, game

def get_game_generator(filename_list):
    for filename_tuple in filename_list:
        game_id, this_game = get_game_from_filename_tuple(filename_tuple)
        if this_game:
            yield game_id, this_game

def write_game_svg_html_from_filename_tuple(filename_output_path_tuple):
    filename_tuple, output_path = filename_output_path_tuple
    game_id, game = get_game_from_filename_tuple(filename_tuple)
    if game:
        print(game_id)
        write_game_svg_and_html(game_id, game, output_path)

def get_game_from_xml_strings(boxscore_raw_xml, players_raw_xml, inning_raw_xml):
    this_game = None
    if (boxscore_raw_xml and players_raw_xml and inning_raw_xml and 
            boxscore_raw_xml != '{"message": "Internal server error"}' and
            players_raw_xml != '{"message": "Internal server error"}' and
            inning_raw_xml != '{"message": "Internal server error"}'):
        boxscore_xml_obj = fromstring(boxscore_raw_xml)
        players_xml_obj = fromstring(players_raw_xml)
        inning_xml_obj = fromstring(inning_raw_xml)
        this_game = get_game_obj(boxscore_xml_obj,
                                 players_xml_obj,
                                 inning_xml_obj)

    return this_game

def write_svg_from_file_range(start_date_str, end_date_str, input_dir, output_dir):
    if not exists(output_dir):
        makedirs(output_dir)

    output_path = abspath(output_dir)
    filename_output_path_tuple_list = [
        (filename_tuple, output_path)
        for filename_tuple in get_filename_list(start_date_str,
                                                end_date_str,
                                                input_dir)
    ]

    for tup in filename_output_path_tuple_list:
        write_game_svg_html_from_filename_tuple(tup)

def get_filename_list(start_date_str, end_date_str, input_dir):
    filename_list = []
    input_path = abspath(input_dir)
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

def get_game_list_from_file_range(start_date_str, end_date_str, input_dir):
    filename_list = get_filename_list(start_date_str, end_date_str, input_dir)
    process_pool = Pool(NUM_PROCESS_SUBLISTS)
    #game_tuple_list = process_pool.map(get_game_from_filename_tuple,
    #                                   filename_list)
    game_tuple_list = [get_game_from_filename_tuple(filename_tuple)
                       for filename_tuple in filename_list]

    return game_tuple_list

def get_game_generator_from_file_range(start_date_str, end_date_str, input_dir):
    filename_list = get_filename_list(start_date_str, end_date_str, input_dir)

    return get_game_generator(filename_list)

def write_svg_from_url(date_str, away_code, home_code, game_number, output_dir):
    if not exists(output_dir):
        makedirs(output_dir)

    output_path = abspath(output_dir)
    game_id, game = get_game_from_url(date_str, away_code, home_code,
                                      game_number)

    write_game_svg_and_html(game_id, game, output_path)

def get_game_xml_from_url(date_str, away_code, home_code, game_number):
    formatted_date_str = get_formatted_date_str(date_str)
    date = parse(formatted_date_str)

    game_id = '-'.join(
        [formatted_date_str, away_code, home_code, str(game_number)]
    )

    request_url_base = MLB_URL_PATTERN.format(
        year=date.year,
        month=str(date.month).zfill(2),
        day=str(date.day).zfill(2),
        away_mlb_code=MLB_TEAM_CODE_DICT[away_code],
        home_mlb_code=MLB_TEAM_CODE_DICT[home_code],
        game_number=game_number
    )

    boxscore_request_text = get(request_url_base + BOXSCORE_SUFFIX).text
    if boxscore_request_text == 'GameDay - 404 Not Found':
        boxscore_raw_xml, players_raw_xml, inning_raw_xml = None, None, None
    else:
        boxscore_raw_xml = boxscore_request_text
        players_raw_xml = get(request_url_base + PLAYERS_SUFFIX).text
        inning_raw_xml = get(request_url_base + INNING_SUFFIX).text

    return game_id, boxscore_raw_xml, players_raw_xml, inning_raw_xml

def get_game_from_url(date_str, away_code, home_code, game_number):
    (game_id,
     boxscore_raw_xml,
     players_raw_xml,
     inning_raw_xml) = get_game_xml_from_url(date_str,
                                             away_code,
                                             home_code,
                                             game_number)

    try:
        this_game = get_game_from_xml_strings(boxscore_raw_xml,
                                              players_raw_xml,
                                              inning_raw_xml)
    except:
        prefix = '/var/log/baseball/xml-{}-'.format(
            '-'.join(str(datetime.now()).split())
        )
        with open(prefix + 'boxscore.xml', 'w') as fh:
            fh.write(boxscore_raw_xml)
        with open(prefix + 'players.xml', 'w') as fh:
            fh.write(players_raw_xml)
        with open(prefix + 'inning_all.xml', 'w') as fh:
            fh.write(inning_raw_xml)
        raise

    if not this_game:
        print('No data found for {} {} {} {}'.format(date_str,
                                                     away_code,
                                                     home_code,
                                                     game_number))

        prefix = '/var/log/baseball/no-data-{}-'.format(
            '-'.join(str(datetime.now()).split())
        )
        with open(prefix + 'boxscore.xml', 'w') as fh:
            fh.write(boxscore_raw_xml)
        with open(prefix + 'players.xml', 'w') as fh:
            fh.write(players_raw_xml)
        with open(prefix + 'inning_all.xml', 'w') as fh:
            fh.write(inning_raw_xml)

    return game_id, this_game
