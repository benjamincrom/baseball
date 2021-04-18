from datetime import timedelta, datetime
from json import loads
from multiprocessing import Pool
from os import listdir, makedirs, mkdir
from os.path import isdir, isfile, exists, abspath, join
from sys import exc_info
from traceback import format_exception
from xml.etree.ElementTree import fromstring

from dateutil.parser import parse
from pytz import timezone
from requests import get

import baseball.process_game_json
from baseball.process_game_xml import MLB_TEAM_CODE_DICT

EASTERN_TIMEZONE_STR = 'America/New_York'
NUM_PROCESS_SUBLISTS = 3
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
INNING_SUFFIX = 'inning/inning_all.xml'

ALL_GAMES_URL = ('http://gdx.mlb.com/components/game/mlb/year_{year:04d}/'
                 'month_{month:02d}/day_{day:02d}/miniscoreboard.json')

GAME_URL_TEMPLATE = 'http://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'

MLB_URL_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                   'month_{month}/day_{day}/gid_{year}_{month}_{day}_'
                   '{away_mlb_code}mlb_{home_mlb_code}mlb_{game_number}/')

HTML_INDEX_PAGE = (
    '<html>'
    '<head>'
    '<style>'
    '.clickme'
    '{{'
    'cursor: pointer;'
    'display: inline; padding-left: 10px; padding-right: 10px;'
    '}}'
    '.arrow {{'
    'border: solid white;'
    'border-width: 0 3px 3px 0;'
    'display: inline-block;'
    'padding: 3px;'
    '}}'
    '.right {{'
    'transform: rotate(-45deg);'
    '-webkit-transform: rotate(-45deg);'
    '}}'
    '.left {{'
    'transform: rotate(135deg);'
    '-webkit-transform: rotate(135deg);'
    '}}'
    '.up {{'
    'transform: rotate(-135deg);'
    '-webkit-transform: rotate(-135deg);'
    '}}'
    '.down {{'
    'transform: rotate(45deg);'
    '-webkit-transform: rotate(45deg);'
    '}}'
    '</style>'
    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/'
    'jquery.min.js"></script>'
    '<link rel="icon" type="image/png" href="baseball-fairy-161.png" />'
    '<meta name="viewport" content="width=device-width, initial-scale=0.1">'
    '<meta http-equiv="cache-control" content="no-cache">'
    '<!-- Global site tag (gtag.js) - Google Analytics -->'
    '<script async src="https://www.googletagmanager.com/gtag/js'
    '?id=UA-108577160-1"></script>'
    '<script>'
    'window.dataLayer = window.dataLayer || [];'
    'function gtag(){{dataLayer.push(arguments);}}'
    'gtag("js", new Date());'
    'gtag("config", "UA-108577160-1");'
    '</script>'
    '<script>'
    'function gobackone() {{'
    'window.location = "./{yesterday_html}";'
    '}}'
    '</script>'
    '<script>'
    'function goforwardone() {{'
    'window.location = "./{tomorrow_html}";'
    '}}'
    '</script>'
    '<script>'
    '(function(h,o,u,n,d) {{ '
    'h=h[d]=h[d]||{{q:[],onReady:function(c){{h.q.push(c)}}}} \n'
    'd=o.createElement(u);d.async=1;d.src=n \n'
    'n=o.getElementsByTagName(u)[0];n.parentNode.insertBefore(d,n) '
    '}})(window,document,\'script\',\'https://www.datadoghq-browser-agent.com/'
    'datadog-rum.js\',\'DD_RUM\')\n'
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
    '<script>'
    'function gotogame() {{'
    'window.location = "./" + document.getElementById("year").value +'
    ' "-" + document.getElementById("month").value + "-" +'
    ' document.getElementById("day").value + ".html";'
    '}}'
    '</script>'
    '<title>Live Baseball Scorecards</title>'
    '</head>'
    '<body style="background-color:black;">'
    '<div id="header" style="width:1160px; margin:0 auto; '
    'text-align: center;">'
    '<img src="baseball-fairy-bat-250.png" height="250"><br />'
    '<font size="7" color="white">'
    'LiveBaseballScorecards.com'
    '</font><br />'
    '<font size="5" color="white">'
    'Contact us at '
    '<a href="mailto:livebaseballscorecards@gmail.com" '
    'style="color:lightblue">livebaseballscorecards@gmail.com</a>'
    '<br />'
    'For abbreviation definitions, hover your mouse over the scorecard '
    'text or just click <a style="color:lightblue" href="abbreviations.html">'
    'here</a>.'
    '<br /><br />'
    '<font size="6" color="white">Select a date</font>'
    '<br />'
    '<div class="clickme" onclick="gobackone()"><i class="arrow left"></i>'
    '</div>'
    '<select name="month" id="month">'
    '<option {month_list[0]} value="01">January</option>'
    '<option {month_list[1]} value="02">February</option>'
    '<option {month_list[2]} value="03">March</option>'
    '<option {month_list[3]} value="04">April</option>'
    '<option {month_list[4]} value="05">May</option>'
    '<option {month_list[5]} value="06">June</option>'
    '<option {month_list[6]} value="07">July</option>'
    '<option {month_list[7]} value="08">August</option>'
    '<option {month_list[8]} value="09">September</option>'
    '<option {month_list[9]} value="10">October</option>'
    '<option {month_list[10]} value="11">November</option>'
    '<option {month_list[11]} value="12">December</option>'
    '</select>'
    '<select name="day" id="day">'
    '<option {day_list[0]} value="01">1</option>'
    '<option {day_list[1]} value="02">2</option>'
    '<option {day_list[2]} value="03">3</option>'
    '<option {day_list[3]} value="04">4</option>'
    '<option {day_list[4]} value="05">5</option>'
    '<option {day_list[5]} value="06">6</option>'
    '<option {day_list[6]} value="07">7</option>'
    '<option {day_list[7]} value="08">8</option>'
    '<option {day_list[8]} value="09">9</option>'
    '<option {day_list[9]} value="10">10</option>'
    '<option {day_list[10]} value="11">11</option>'
    '<option {day_list[11]} value="12">12</option>'
    '<option {day_list[12]} value="13">13</option>'
    '<option {day_list[13]} value="14">14</option>'
    '<option {day_list[14]} value="15">15</option>'
    '<option {day_list[15]} value="16">16</option>'
    '<option {day_list[16]} value="17">17</option>'
    '<option {day_list[17]} value="18">18</option>'
    '<option {day_list[18]} value="19">19</option>'
    '<option {day_list[19]} value="20">20</option>'
    '<option {day_list[20]} value="21">21</option>'
    '<option {day_list[21]} value="22">22</option>'
    '<option {day_list[22]} value="23">23</option>'
    '<option {day_list[23]} value="24">24</option>'
    '<option {day_list[24]} value="25">25</option>'
    '<option {day_list[25]} value="26">26</option>'
    '<option {day_list[26]} value="27">27</option>'
    '<option {day_list[27]} value="28">28</option>'
    '<option {day_list[28]} value="29">29</option>'
    '<option {day_list[29]} value="30">30</option>'
    '<option {day_list[30]} value="31">31</option>'
    '</select>'
    '<select name="year" id="year">'
    '<option {year_list[2021]} value="2021">2021</option>'
    '<option {year_list[2020]} value="2020">2020</option>'
    '<option {year_list[2019]} value="2019">2019</option>'
    '<option {year_list[2018]} value="2018">2018</option>'
    '<option {year_list[2017]} value="2017">2017</option>'
    '<option {year_list[2016]} value="2016">2016</option>'
    '<option {year_list[2015]} value="2015">2015</option>'
    '<option {year_list[2014]} value="2014">2014</option>'
    '<option {year_list[2013]} value="2013">2013</option>'
    '<option {year_list[2012]} value="2012">2012</option>'
    '<option {year_list[2011]} value="2011">2011</option>'
    '<option {year_list[2010]} value="2010">2010</option>'
    '</select>'
    '<div class="clickme" onclick="goforwardone()"><i class="arrow right"></i>'
    '</div>'
    '<br />'
    '<button onclick="gotogame()">Select Date</button>'
    '<br /><br />'
    '<font size="6" color="white">{today_str}</font>'
    '</div>'
    '<br />'
    '<table cellpadding="10" style="width:1160px" align="center">'
    '{result_object_list_str}'
    '</table>'
    '</body>'
    '</html>'
)

HTML_WRAPPER = (
    '<html>'
    '<head>'
    '<meta name="viewport" content="width=device-width, initial-scale=0.1">'
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
    '}})(window,document,\'script\',\'https://www.datadoghq-browser-agent.com/'
    'datadog-rum.js\',\'DD_RUM\')\n'
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

OBJECT_ENTRY_TEMPLATE = (
    '<script>'
    '$(document).ready(function() {{'
    '$.get(\'{game_id_str}.svg\', function (data) {{'
    'document.getElementById("{game_id_str}").innerHTML = new XMLSerializer().'
    'serializeToString(data.documentElement).replace(\'height="2256" \','
    ' \'height="735" \');'
    '}});'
    'setInterval(function() {{'
    '$.get(\'{game_id_str}.svg\', function (data) {{'
    'document.getElementById("{game_id_str}").innerHTML = new XMLSerializer().'
    'serializeToString(data.documentElement).replace(\'height="2256" \','
    ' \'height="735" \');'
    '}});'
    '}}, 10000);'
    '}});'
    '</script>'
    '<td valign="top"><div align="center">'
    '<a>'
    '<font size="5"><a style="color:lightblue; text-decoration: none;" '
    'href="{game_id_str}.html">{title_str}</a></font>'
    '</div>'
    '<br />'
    '<div align="center">'
    '<div align="center">'
    '<a href="./{game_id_str}.html" style="text-decoration:none">'
    '<object id="{game_id_str}"></object>'
    '</a>'
    '</div>'
    '</div>'
    '</td>'
)

GET_TODAY_GAMES_USAGE_STR = (
    'Usage:\n'
    '  - ./get_today_games.py [OUTPUT DIRECTORY]\n'
)

def get_today_date_str(this_datetime):
    today_date_str = '{}-{}-{}'.format(this_datetime.year,
                                       str(this_datetime.month).zfill(2),
                                       str(this_datetime.day).zfill(2))

    return today_date_str

def get_generated_html_id_list(game_id_list, today_date_str, output_dir,
                               write_game_html):
    if not exists(output_dir):
        makedirs(output_dir)

    output_path = abspath(output_dir)
    game_html_id_tuple_list = []

    for game_id in game_id_list:
        away_mlb_code = game_id.split('_')[-3][:3]
        home_mlb_code = game_id.split('_')[-2][:3]
        game_num_str = game_id.split('_')[-1]

        if (away_mlb_code in MLB_TEAM_CODE_DICT.values() and
                home_mlb_code in MLB_TEAM_CODE_DICT.values()):
            away_code = [key for key, val in MLB_TEAM_CODE_DICT.items()
                         if val == away_mlb_code][0]
            home_code = [key for key, val in MLB_TEAM_CODE_DICT.items()
                         if val == home_mlb_code][0]

            game_id, game = get_game_from_url(today_date_str,
                                              away_code,
                                              home_code,
                                              game_num_str)

            if game:
                write_game_svg_and_html(game_id, game, output_path,
                                        write_game_html)

                game_html_id_tuple_list.append(
                    ('{}-{}-{}-{}'.format(today_date_str,
                                          away_code,
                                          home_code,
                                          game_num_str),
                     game)
                )

    return game_html_id_tuple_list

def get_date_lists(this_datetime):
    year = this_datetime.year
    year_list = []
    for index in range(2500):
        if index == year:
            year_list.append('selected')
        else:
            year_list.append('')

    month = this_datetime.month
    month_list = []
    for index in range(12):
        if index == month - 1:
            month_list.append('selected')
        else:
            month_list.append('')

    day = this_datetime.day
    day_list = []
    for index in range(32):
        if index == day - 1:
            day_list.append('selected')
        else:
            day_list.append('')

    return year_list, month_list, day_list

def generate_game_svgs_for_old_datetime(this_datetime, output_dir,
                                        write_game_html=False,
                                        write_date_html=False,
                                        write_index_html=False):
    if not exists(output_dir):
        mkdir(output_dir)

    today_date_str = get_today_date_str(this_datetime)
    month = int(this_datetime.month)
    day = int(this_datetime.day)
    year = int(this_datetime.year)
    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    if isinstance(all_games_dict['data']['games'].get('game', []), dict):
        all_games_dict['data']['games']['game'] = [
            all_games_dict['data']['games']['game']
        ]

    game_id_list = [
        game_dict['id'].replace('-', '_').replace('/', '_')
        for game_dict in all_games_dict['data']['games'].get('game', [])
    ]

    game_html_id_tuple_list = get_generated_html_id_list(game_id_list,
                                                         today_date_str,
                                                         output_dir,
                                                         write_game_html)

    object_html_str = get_object_html_str(game_html_id_tuple_list)

    write_game_index(object_html_str, this_datetime, output_dir,
                     write_date_html, write_index_html)

def get_object_html_str(game_html_id_tuple_list):
    object_html_str = ''
    for i, (game_html_id, game) in enumerate(game_html_id_tuple_list):
        if i < (len(game_html_id_tuple_list) - 1):
            look_ahead_id, _ = game_html_id_tuple_list[i+1]
            if look_ahead_id[:-1] == game_html_id[:-1]:
                game.is_doubleheader = True

        look_behind_id, _ = game_html_id_tuple_list[i-1]
        if look_behind_id[:-1] == game_html_id[:-1]:
            game.is_doubleheader = True

        start_datetime = (
            game.start_datetime if game.start_datetime
            else game.expected_start_datetime
        )

        title_str = '{} @ {}<br />'.format(game.away_team.name,
                                           game.home_team.name)

        if start_datetime:
            start_datetime = start_datetime.astimezone(
                timezone(game.timezone_str)
            )

            est_time = start_datetime.astimezone(timezone(EASTERN_TIMEZONE_STR))

            subtitle_flag = False
            if ((not (est_time.hour == 23 and est_time.minute == 33)) and
                    (not (est_time.hour == 0 and est_time.minute == 0))):
                title_str += '{}'.format(
                    start_datetime.strftime('%-I:%M %p %Z')
                )

                subtitle_flag = True

            if game.is_doubleheader:
                if subtitle_flag:
                    title_str += ' - '

                title_str += 'Game {}'.format(game.game_date_str[-1])
                subtitle_flag = True
            elif game.is_postponed:
                if subtitle_flag:
                    title_str += ' - '

                title_str += 'Postponed'
                subtitle_flag = True

        if i % 2 == 0:
            object_html_str += '<tr>'

        object_html_str += OBJECT_ENTRY_TEMPLATE.format(
            title_str=title_str,
            game_id_str=game_html_id
        )

        if i % 2 == 1:
            object_html_str += '</tr>'

    return object_html_str

def write_games_for_date(this_datetime, output_dir, write_game_html=False,
                         write_date_html=False, write_index_html=False):
    if this_datetime.year >= 2019:
        generate_game_svgs_for_new_datetime(this_datetime, output_dir,
                                            write_game_html, write_date_html,
                                            write_index_html)
    else:
        generate_game_svgs_for_old_datetime(this_datetime, output_dir,
                                            write_game_html, write_date_html,
                                            write_index_html)

def generate_game_svgs_for_new_datetime(this_datetime, output_dir,
                                        write_game_html, write_date_html,
                                        write_index_html):
    if not exists(output_dir):
        mkdir(output_dir)

    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year
    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    if isinstance(all_games_dict['data']['games'].get('game', []), dict):
        all_games_dict['data']['games']['game'] = [
            all_games_dict['data']['games']['game']
        ]

    game_tuple_list = [(x['id'], x['game_pk'])
                       for x in all_games_dict['data']['games'].get('game', [])]

    game_dict_list = [get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
                      for _, game_pk in game_tuple_list]

    game_html_id_tuple_list = []
    for i, game_dict in enumerate(game_dict_list):
        try:
            game = baseball.process_game_json.get_game_obj(game_dict)
            if len(game.game_date_str.split('-')) == 6:
                game_html_id_tuple_list.append((game.game_date_str, game))
            else:
                game.game_date_str = '{:04d}-{:02d}-{:02d}-{}'.format(
                    year, month, day, game.game_date_str
                )

                if len(game.game_date_str.split('-')) == 6:
                    game_html_id_tuple_list.append((game.game_date_str, game))

            if game.expected_start_datetime.astimezone(
                    timezone(game.timezone_str)).day != day:
                game.is_postponed = True

            game_set_doubleheader(i, game_dict, game_dict_list, game)
            write_game_svg_and_html(game.game_date_str, game, output_dir,
                                    write_game_html)
        except:
            exc_type, exc_value, exc_traceback = exc_info()
            lines = format_exception(exc_type, exc_value, exc_traceback)
            exception_str = ' '.join(lines)
            print('{} {} {}'.format(datetime.utcnow(),
                                    game_dict['gameData']['game']['id'],
                                    exception_str))

    object_html_str = get_object_html_str(game_html_id_tuple_list)

    write_game_index(object_html_str, this_datetime, output_dir,
                     write_date_html, write_index_html)

def game_set_doubleheader(i, game_dict, game_dict_list, game):
    if i < (len(game_dict_list) - 1):
        look_ahead_id = game_dict_list[i+1]['gameData']['game']['id']
        if look_ahead_id[:-2] == game_dict['gameData']['game']['id'][:-2]:
            game.is_doubleheader = True

    look_behind_id = game_dict_list[i-1]['gameData']['game']['id']
    if look_behind_id[:-2] == game_dict['gameData']['game']['id'][:-2]:
        game.is_doubleheader = True

def write_game_index(object_html_str, this_datetime, output_dir,
                     write_date_html, write_index_html):
    year_list, month_list, day_list = get_date_lists(this_datetime)
    today_str = '{} {}, {}'.format(this_datetime.strftime("%B"),
                                   this_datetime.day,
                                   this_datetime.year)

    yesterday = this_datetime - timedelta(days=1)
    tomorrow = this_datetime + timedelta(days=1)
    yesterday_html = '{:04d}-{:02d}-{:02d}.html'.format(int(yesterday.year),
                                                        int(yesterday.month),
                                                        int(yesterday.day))

    tomorrow_html = '{:04d}-{:02d}-{:02d}.html'.format(int(tomorrow.year),
                                                       int(tomorrow.month),
                                                       int(tomorrow.day))

    output_filename = '/{:04d}-{:02d}-{:02d}.html'.format(
        int(this_datetime.year),
        int(this_datetime.month),
        int(this_datetime.day)
    )

    output_html = HTML_INDEX_PAGE.format(result_object_list_str=object_html_str,
                                         month_list=month_list,
                                         day_list=day_list,
                                         year_list=year_list,
                                         yesterday_html=yesterday_html,
                                         tomorrow_html=tomorrow_html,
                                         today_str=today_str,
                                         output_filename=output_filename)

    if object_html_str or not exists(output_dir + output_filename):
        if write_date_html:
            write_location = output_dir + output_filename
            with open(write_location, 'w', encoding='utf-8') as fh:
                fh.write(output_html)

        if write_index_html:
            write_location = output_dir + '/index.html'
            with open(write_location, 'w', encoding='utf-8') as fh:
                fh.write(output_html)

def get_game_from_date(this_datetime, this_away_code, this_home_code,
                       this_game_number):
    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year
    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    game_tuple_list = [
        (x['id'], x['game_pk'])
        for x in all_games_dict['data']['games'].get('game', [])
    ]

    game_dict_list = [get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
                      for _, game_pk in game_tuple_list]

    game = None
    for i, game_dict in enumerate(game_dict_list):
        away_code = (
            game_dict.get('gameData', {}).get('teams', {}).get(
                'away', {}).get('abbreviation', {})
        )

        home_code = (
            game_dict.get('gameData', {}).get('teams', {}).get(
                'home', {}).get('abbreviation', {})
        )

        game_number_is_match = (
            this_game_number == game_dict.get('gameData', {}).get(
                'game', {}).get('gameNumber', {})
        )

        if ((away_code and home_code) and (away_code == this_away_code) and
                (home_code == this_home_code) and game_number_is_match):
            game = baseball.process_game_json.get_game_obj(game_dict)
            game_set_doubleheader(i, game_dict, game_dict_list, game)

    return game

def get_formatted_date_str(input_date_str):
    this_date = parse(input_date_str)
    this_date_str = '{}-{}-{}'.format(str(this_date.year),
                                      str(this_date.month).zfill(2),
                                      str(this_date.day).zfill(2))

    return this_date_str

def write_game_svg_and_html(game_id, game, output_path, write_html=False):
    svg_filename = game_id + '.svg'
    html_filename = game_id + '.html'

    svg_text = game.get_svg_str()
    html_text = HTML_WRAPPER.format(title=game_id, filename=svg_filename)

    output_svg_path = join(output_path, svg_filename)
    output_html_path = join(output_path, html_filename)

    with open(output_svg_path, 'w') as filehandle:
        filehandle.write(svg_text)

    if write_html:
        with open(output_html_path, 'w') as filehandle:
            filehandle.write(html_text)

def get_game_from_files_new(live_json_file):
    this_game = None

    try:
        if isfile(live_json_file):
            live_raw = open(live_json_file, 'r', encoding='utf-8').read()
            game_dict = loads(live_raw)
            this_game = baseball.process_game_json.get_game_obj(game_dict)
    except:
        exc_type, exc_value, exc_traceback = exc_info()
        lines = format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ' '.join(lines)
        print('{} ({}) {}'.format(datetime.utcnow(),
                                  live_json_file,
                                  exception_str))

    return this_game

def get_game_from_files_old(boxscore_file, player_file, inning_file):
    this_game = None

    try:
        if (isfile(boxscore_file) and isfile(player_file) and
                isfile(inning_file)):
            boxscore_raw = open(boxscore_file, 'r', encoding='utf-8').read()
            boxscore_xml = fromstring(boxscore_raw)
            player_raw = open(player_file, 'r', encoding='utf-8').read()
            player_xml = fromstring(player_raw)
            inning_raw = open(inning_file, 'r', encoding='utf-8').read()
            inning_xml = fromstring(inning_raw)
            this_game = baseball.process_game_xml.get_game_obj(boxscore_xml,
                                                               player_xml,
                                                               inning_xml)
    except:
        exc_type, exc_value, exc_traceback = exc_info()
        lines = format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ' '.join(lines)
        print('{} ({} {} {}) {}'.format(datetime.utcnow(),
                                        boxscore_file,
                                        player_file,
                                        inning_file,
                                        exception_str))

    return this_game

def get_game_from_filename_tuple(filename_tuple):
    game_id, boxscore_file, player_file, inning_file, live_file = filename_tuple
    year = int(game_id.split('-', 1)[0])
    if year < 2019:
        game = get_game_from_files_old(boxscore_file, player_file, inning_file)
    else:
        game = get_game_from_files_new(live_file)

    return game_id, game

def get_game_generator(filename_list):
    for filename_tuple in filename_list:
        game_id, this_game = get_game_from_filename_tuple(filename_tuple)
        if this_game:
            yield game_id, this_game

def write_game_svg_html_from_filename_tuple(filename_output_path_tuple,
                                            write_game_html=False):
    filename_tuple, output_path = filename_output_path_tuple
    game_id, game = get_game_from_filename_tuple(filename_tuple)
    if game:
        write_game_svg_and_html(game_id, game, output_path, write_game_html)

def get_game_from_xml_strings(boxscore_raw_xml, players_raw_xml,
                              inning_raw_xml):
    this_game = None
    if (boxscore_raw_xml and players_raw_xml and inning_raw_xml and
            boxscore_raw_xml != '{"message": "Internal server error"}' and
            players_raw_xml != '{"message": "Internal server error"}' and
            inning_raw_xml != '{"message": "Internal server error"}'):
        boxscore_xml_obj = fromstring(boxscore_raw_xml)
        players_xml_obj = fromstring(players_raw_xml)
        inning_xml_obj = fromstring(inning_raw_xml)
        this_game = baseball.process_game_xml.get_game_obj(boxscore_xml_obj,
                                                           players_xml_obj,
                                                           inning_xml_obj)

    return this_game

def write_svg_from_file_range(start_date_str, end_date_str, input_dir,
                              output_dir, write_game_html=False,
                              write_date_html=False):
    if not exists(output_dir):
        makedirs(output_dir)

    output_path = abspath(output_dir)
    filename_output_path_tuple_list = [
        (filename_tuple, output_path)
        for filename_tuple in get_filename_list(start_date_str,
                                                end_date_str,
                                                input_dir)
    ]

    game_html_id_tuple_list = []
    this_year = this_month = this_day = None
    for tup in filename_output_path_tuple_list:
        filename_tuple, _ = tup
        game_id = filename_tuple[0]
        year_str, month_str, day_str, _, _, _  = game_id.split('-')
        if not (year_str == this_year and month_str == this_month and
                day_str == this_day):
            this_datetime = parse(
                '{}-{}-{}'.format(this_year, this_month, this_day)
            )

            object_html_str = get_object_html_str(game_html_id_tuple_list)
            write_game_index(object_html_str, this_datetime, output_dir,
                             write_date_html, False)

            year_str = this_year
            month_str = this_month
            day_str = this_day
            game_html_id_tuple_list = []

        write_game_svg_html_from_filename_tuple(tup, write_game_html)
        game_html_id_tuple_list.append(
            get_game_from_filename_tuple(filename_tuple)
        )

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

                                live_filename = (subfolder_name + 'live')

                                filename_list.append((output_name,
                                                      boxscore_filename,
                                                      player_filename,
                                                      inning_filename,
                                                      live_filename))

        this_date += day_delta

    return filename_list

def get_game_list_from_file_range(start_date_str, end_date_str, input_dir,
                                    ):
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

    write_game_svg_and_html(game_id, game, output_path, False)

def get_game_dict_from_url(date_str, away_code, home_code, game_number):
    formatted_date_str = get_formatted_date_str(date_str)
    this_datetime = parse(formatted_date_str)
    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year

    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    game_tuple_list = [(x['id'], x['game_pk'])
                       for x in all_games_dict['data']['games'].get('game', [])]

    game_dict_list = [get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
                      for _, game_pk in game_tuple_list]

    return_dict = {}
    game_id = None
    for game_dict in game_dict_list:
        this_away_code = (
            game_dict.get('gameData', {}).get('teams', {}).get(
                'away', {}).get('abbreviation', {})
        )

        this_home_code = (
            game_dict.get('gameData', {}).get('teams', {}).get(
                'home', {}).get('abbreviation', {})
        )

        game_number_is_match = (
            game_number == game_dict.get('gameData', {}).get(
                'game', {}).get('gameNumber', {})
        )

        if ((this_away_code and this_home_code) and
                (away_code == this_away_code) and
                (home_code == this_home_code) and
                game_number_is_match):

            game_id = '-'.join(
                [formatted_date_str, away_code, home_code, str(game_number)]
            )

            return_dict = game_dict
            break

    return game_id, return_dict

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

def get_game_from_url_new(date_str, this_date, away_code, home_code,
                          game_number):
    this_game = get_game_from_date(this_date, away_code, home_code,
                                   game_number)

    formatted_date_str = get_formatted_date_str(date_str)
    game_id = '-'.join(
        [formatted_date_str, away_code, home_code, str(game_number)]
    )

    if not this_game:
        print('No data found for {} {} {} {}'.format(date_str,
                                                     away_code,
                                                     home_code,
                                                     game_number))

    return game_id, this_game

def get_game_from_url_old(date_str, away_code, home_code, game_number):
    (game_id,
     boxscore_raw_xml,
     players_raw_xml,
     inning_raw_xml) = get_game_xml_from_url(date_str,
                                             away_code,
                                             home_code,
                                             game_number)

    this_game = get_game_from_xml_strings(boxscore_raw_xml,
                                          players_raw_xml,
                                          inning_raw_xml)

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

def get_game_from_url(date_str, away_code, home_code, game_number):
    this_game = None
    game_id = None
    try:
        this_date = parse(date_str)
        if int(this_date.year) >= 2019:
            game_id, this_game = get_game_from_url_new(
                date_str, this_date, away_code, home_code, game_number
            )
        else:
            game_id, this_game = get_game_from_url_old(
                date_str, away_code, home_code, game_number
            )
    except:
        exc_type, exc_value, exc_traceback = exc_info()
        lines = format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ' '.join(lines)
        print('{} ({}-{}-{}-{}) {}'.format(datetime.utcnow(),
                                           date_str,
                                           away_code,
                                           home_code,
                                           game_number,
                                           exception_str))

    return game_id, this_game

def generate_today_game_svgs(output_dir, write_game_html=False,
                             write_date_html=False, write_index_html=False):
    time_shift = timedelta(hours=7)
    today_datetime = datetime.utcnow() - time_shift
    try:
        write_games_for_date(
            today_datetime.astimezone(timezone('America/New_York')),
            output_dir,
            write_game_html,
            write_date_html,
            write_index_html
        )
    except:
        exc_type, exc_value, exc_traceback = exc_info()
        lines = format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ' '.join(lines)
        print('{} ({}) {}'.format(datetime.utcnow(),
                                  str(today_datetime),
                                  exception_str))
