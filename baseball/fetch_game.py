from datetime import timedelta, datetime
from multiprocessing import Pool
from os import listdir, makedirs, mkdir
from os.path import isdir, isfile, exists, abspath, join
from re import search, sub
from sys import exc_info
from traceback import format_exception
from xml.etree.ElementTree import fromstring

from dateutil.parser import parse
from pytz import timezone
from requests import get

import baseball
from baseball.baseball_events import (AUTOMATIC_BALL_POSITION, Pitch, Pickoff,
                                      RunnerAdvance)

from baseball.process_game_xml import (
    MLB_TEAM_CODE_DICT, get_game_obj, get_datetime, get_sub_switch_steal_flags,
    parse_substitution, process_substitution, parse_switch_description,
    process_switch, fix_description
)

NUM_PROCESS_SUBLISTS = 3
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
INNING_SUFFIX = 'inning/inning_all.xml'

ALL_GAMES_2020_URL = ('http://gdx.mlb.com/components/game/mlb/year_{year:04d}/'
                      'month_{month:02d}/day_{day:02d}/miniscoreboard.json')

GAME_URL_2020_TEMPLATE = ('http://statsapi.mlb.com/api/v1.1/game/{game_pk}'
                          '/feed/live')


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
    '<meta name="viewport" content="width=device-width, initial-scale=0.35">'
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

ALL_GAMES_URL = ('http://gdx.mlb.com/components/game/mlb/year_{year:04d}/'
                 'month_{month:02d}/day_{day:02d}/miniscoreboard.json')

GAME_URL_TEMPLATE = 'http://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'

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
    '<a href="./{game_id_str}.html" style="text-decoration:none">'
    '<div align="center">'
    '<object id="{game_id_str}"></object>'
    '</div>'
    '</a>'
    '</div>'
    '</td>'
)

MLB_URL_BASE_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                        'month_{month}/day_{day}')

GET_TODAY_GAMES_USAGE_STR = (
    'Usage:\n'
    '  - ./get_today_games.py [OUTPUT DIRECTORY]\n'
)

def parse_name(batter_name):
    if search(r'\w\s+[A-Z]\.\s+', batter_name):
        batter_name = sub(r'\s[A-Z]\.\s+', ' ', batter_name)

    player_first_name, player_last_name = batter_name.split(' ', 1)

    return player_first_name, player_last_name

def set_player_list(team_dict, gamedata_dict, team):
    digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for player_id, this_player_dict in team_dict['players'].items():
        gamedata_player_dict = gamedata_dict['players'][player_id]
        jersey_number = ''
        if ('jerseyNumber' in this_player_dict and
                this_player_dict.get('jerseyNumber')):
            if all([character in digit_list
                    for character in this_player_dict.get('jerseyNumber')]):
                jersey_number = int(this_player_dict.get('jerseyNumber'))

        (first_name, last_name) = parse_name(
            this_player_dict['person']['fullName']
        )

        new_player = baseball.Player(
            last_name,
            first_name,
            this_player_dict['person']['id'],
            float(this_player_dict['seasonStats']['batting']['obp']),
            float(this_player_dict['seasonStats']['batting']['slg']),
            jersey_number
        )

        new_player.pitch_hand = gamedata_player_dict['pitchHand']['code']
        new_player.bat_side = gamedata_player_dict['batSide']['code']

        if this_player_dict['seasonStats']['pitching']['era'] != '-.--':
            this_era = float(this_player_dict['seasonStats']['pitching']['era'])
            if this_era != 0.0:
                new_player.era = this_era
            else:
                new_player.era = ''
        else:
            new_player.era = ''


        team.append(new_player)

def initialize_team(team_gamedata_dict, team_livedata_dict, full_gamedata_dict):
    team = baseball.Team(
        team_gamedata_dict['name'],
        team_gamedata_dict['abbreviation']
    )

    set_player_list(team_livedata_dict, full_gamedata_dict, team)
    if team_livedata_dict.get('pitchers'):
        team.pitcher_list = [
            baseball.PlayerAppearance(
                team[team_livedata_dict['pitchers'][0]], 1, 1, 'top', 1
            )
        ]
    else:
        team.pitcher_list = []

    for _, player_dict in team_livedata_dict['players'].items():
        if player_dict.get('battingOrder'):
            batting_order = int(player_dict['battingOrder'])
            position = player_dict['allPositions'][0]['code']

            if batting_order % 100 == 0:
                batting_index = int((batting_order / 100) - 1)
                team.batting_order_list_list[batting_index] = [
                    baseball.PlayerAppearance(
                        team[int(player_dict['person']['id'])],
                        position,
                        1,
                        'top',
                        1
                    )
                ]

    return team

def initialize_game(this_game, attendance_str, temperature_str, weather_str):
    away_team = initialize_team(
        this_game['gameData']['teams']['away'],
        this_game['liveData']['boxscore']['teams']['away'],
        this_game['gameData'],
    )

    home_team = initialize_team(
        this_game['gameData']['teams']['home'],
        this_game['liveData']['boxscore']['teams']['home'],
        this_game['gameData']
    )

    location = '{}, {}, {}'.format(
        this_game['gameData']['venue']['name'],
        this_game['gameData']['venue']['location']['city'],
        this_game['gameData']['venue']['location']['stateAbbrev']
    )

    start_date = None
    end_date = None
    if this_game['liveData']['plays'].get('allPlays'):
        first_play = this_game['liveData']['plays']['allPlays'][0]
        for play_event in first_play['playEvents']:
            if play_event['type'] == 'pitch':
                start_date = get_datetime(
                    play_event['startTime']
                )
                break

        end_date = get_datetime(
            this_game['liveData']['plays']['allPlays'][-1]['about']['endTime']
        )

    if start_date:
        game_str = '{:04d}-{:02d}-{:02d}-{}-{}{}'.format(
            int(start_date.astimezone(timezone('America/New_York')).year),
            int(start_date.astimezone(timezone('America/New_York')).month),
            int(start_date.astimezone(timezone('America/New_York')).day),
            away_team.abbreviation,
            home_team.abbreviation,
            this_game['gameData']['game']['id'][-2:]
        )
    else:
        game_str = '{}-{}{}'.format(
            away_team.abbreviation,
            home_team.abbreviation,
            this_game['gameData']['game']['id'][-2:]
        )

    game_obj = baseball.Game(
        home_team,
        away_team,
        location,
        game_str,
        start_date,
        end_date,
        None
    )

    if attendance_str:
        game_obj.attendance = int(attendance_str)

    if temperature_str:
        game_obj.temp = int(temperature_str)

    if weather_str:
        game_obj.weather = weather_str

    return game_obj

def get_inning_dict_list(game_dict):
    inning_dict_list = []
    inning_num = 1
    inning_half = 'top'

    while True:
        play_dict_list = []
        for this_play_dict in game_dict['liveData']['plays']['allPlays']:
            if (this_play_dict['about']['inning'] == inning_num and
                    this_play_dict['about']['halfInning'] == inning_half):
                play_dict_list.append(this_play_dict)

        if play_dict_list and inning_half == 'top':
            inning_dict_list.append({'top': play_dict_list})
            inning_half = 'bottom'
        elif play_dict_list and inning_half == 'bottom':
            inning_dict_list[-1]['bottom'] = play_dict_list
            inning_num += 1
            inning_half = 'top'
        elif play_dict_list:
            raise Exception('Invalid inning half value')
        else:
            break

    return inning_dict_list

def process_pitch(event):
    pitch_description = event['details']['call']['description']
    if event['details'].get('type'):
        pitch_type = event['details']['type']['code']
    else:
        pitch_type = ''

    pitch_datetime = get_datetime(event['startTime'])

    if (not event['pitchData']['coordinates'].get('x') or
            not event['pitchData']['coordinates'].get('y') or
            event['pitchData']['coordinates'].get('x') == 'None' or
            event['pitchData']['coordinates'].get('y') == 'None'):
        (pitch_x, pitch_y) = AUTOMATIC_BALL_POSITION
    else:
        pitch_x = float(event['pitchData']['coordinates'].get('x'))
        pitch_y = float(event['pitchData']['coordinates'].get('y'))

    pitch_position = (pitch_x, pitch_y)

    if event['pitchData'].get('startSpeed'):
        pitch_speed = float(event['pitchData'].get('startSpeed'))
    else:
        pitch_speed = None

    pitch_obj = Pitch(
        pitch_datetime,
        pitch_description,
        pitch_type,
        pitch_speed,
        pitch_position
    )

    return pitch_obj

def process_pickoff(event):
    pickoff_description = event['details'].get('description')
    pickoff_base = pickoff_description.split()[-1]

    if (pickoff_description.split()[1] == 'Attempt' or
            pickoff_description.split()[1] == 'Error'):
        pickoff_was_successful = False
    elif len(pickoff_description.split()) == 2:
        pickoff_was_successful = True
    else:
        raise ValueError('Bad Pickoff description.')

    pickoff_obj = Pickoff(
        pickoff_description,
        pickoff_base,
        pickoff_was_successful
    )

    return pickoff_obj

def process_plate_appearance(plate_appearance, inning_half_str, inning_num,
                             next_batter_num, game_obj):
    event_list = []
    scoring_runners_list = []
    runners_batted_in_list = []
    for event in plate_appearance['playEvents']:
        if event['type'] == 'pitch':
            pitch_obj = process_pitch(event)
            event_list.append(pitch_obj)
        elif event['type'] == 'pickoff':
            pickoff_obj = process_pickoff(event)
            event_list.append(pickoff_obj)
        elif event['type'] == 'action':
            event_description = event['details']['description']
            event_summary = event['details'].get('event', '')
            event_datetime = get_datetime(event['startTime'])

            substitution_flag, switch_flag, _ = get_sub_switch_steal_flags(
                event_summary,
                event_description
            )

            if substitution_flag:
                (substituting_team,
                 substitution_obj) = parse_substitution(event_datetime,
                                                        event_description,
                                                        event_summary,
                                                        inning_half_str,
                                                        game_obj)

                event_list.append(substitution_obj)
                process_substitution(substitution_obj, inning_num,
                                     inning_half_str, next_batter_num,
                                     substituting_team)

            elif switch_flag:
                (switch_obj,
                 switching_team) = parse_switch_description(event_datetime,
                                                            event_description,
                                                            event_summary,
                                                            game_obj,
                                                            inning_half_str)

                event_list.append(switch_obj)
                process_switch(switch_obj, inning_num, inning_half_str,
                               next_batter_num, switching_team)
        elif event['type'] == 'no_pitch':
            pass
        else:
            raise Exception('Invalid event type')

    for runner_event in plate_appearance['runners']:
        runner_id = int(runner_event['details']['runner']['id'])

        if runner_id in game_obj.away_team:
            runner = game_obj.away_team[runner_id]
        elif runner_id in game_obj.home_team:
            runner = game_obj.home_team[runner_id]
        else:
            raise ValueError('Runner ID not in player dict')

        start_base = runner_event['movement'].get('start') or ''
        end_base = runner_event['movement'].get('end', '') or ''
        run_description = runner_event['details'].get('event')
        runner_scored = (runner_event['movement'].get('end') == 'score')
        run_earned = runner_event['details'].get('earned')
        is_rbi = runner_event['details'].get('rbi')

        runner_advance_obj = RunnerAdvance(
            run_description,
            runner,
            start_base,
            end_base,
            runner_scored,
            run_earned,
            is_rbi
        )

        if runner_advance_obj.runner_scored:
            scoring_runners_list.append(runner_advance_obj.runner)

            if runner_advance_obj.is_rbi:
                runners_batted_in_list.append(runner_advance_obj.runner)

        event_list.append(runner_advance_obj)

    return event_list, scoring_runners_list, runners_batted_in_list

def process_at_bat(plate_appearance, event_list, game_obj,
                   inning_half_str, inning_num, next_batter_num):
    (new_event_list,
     scoring_runners_list,
     runners_batted_in_list) = process_plate_appearance(plate_appearance,
                                                        inning_half_str,
                                                        inning_num,
                                                        next_batter_num,
                                                        game_obj)

    event_list += new_event_list
    if plate_appearance['result'].get('description'):
        plate_appearance_desc = fix_description(
            plate_appearance['result'].get('description')
        )
    else:
        plate_appearance_desc = ''

    pitcher_id = int(plate_appearance['matchup']['pitcher']['id'])
    inning_outs = int(plate_appearance['count']['outs'])

    pitcher = None
    for this_team in [game_obj.home_team, game_obj.away_team]:
        if pitcher_id in this_team:
            pitcher = this_team[pitcher_id]

    if not pitcher:
        raise ValueError('Batter ID not in player_dict')

    batter_id = int(plate_appearance['matchup']['batter']['id'])
    if batter_id in game_obj.home_team:
        batter = game_obj.home_team[batter_id]
        batting_team = game_obj.home_team
    elif batter_id in game_obj.away_team:
        batter = game_obj.away_team[batter_id]
        batting_team = game_obj.away_team
    else:
        raise ValueError('Batter ID not in player_dict')

    start_datetime = get_datetime(plate_appearance['about']['startTime'])
    end_datetime = get_datetime(plate_appearance['about']['endTime'])
    plate_appearance_summary = (
        plate_appearance['result'].get('event', '').strip()
    )

    plate_appearance_obj = baseball.PlateAppearance(start_datetime,
                                                    end_datetime,
                                                    batting_team,
                                                    plate_appearance_desc,
                                                    plate_appearance_summary,
                                                    pitcher,
                                                    batter,
                                                    inning_outs,
                                                    scoring_runners_list,
                                                    runners_batted_in_list,
                                                    event_list)

    return plate_appearance_obj

def set_pitcher_wls_codes(game_dict, game):
    teams_dict = game_dict['liveData']['boxscore']['teams']
    away_wls_dict = {
        x['person']['id']: x['stats']['pitching']['note'][1]
        for _, x in teams_dict['away']['players'].items()
        if x['stats']['pitching'].get('note')
    }

    home_wls_dict = {
        x['person']['id']: x['stats']['pitching']['note'][1]
        for _, x in teams_dict['home']['players'].items()
        if x['stats']['pitching'].get('note')
    }

    for pitcher_appearance in game.away_team.pitcher_list:
        pitcher_id = pitcher_appearance.player_obj.mlb_id
        if pitcher_id in away_wls_dict:
            pitcher_appearance.pitcher_credit_code = (
                away_wls_dict[pitcher_id]
            )
        else:
            pitcher_appearance.pitcher_credit_code = ''


    for pitcher_appearance in game.home_team.pitcher_list:
        pitcher_id = pitcher_appearance.player_obj.mlb_id
        if pitcher_id in home_wls_dict:
            pitcher_appearance.pitcher_credit_code = (
                home_wls_dict[pitcher_id]
            )
        else:
            pitcher_appearance.pitcher_credit_code = ''

def process_half_inning(plate_appearance_dict_list, inning_half_str, game_obj):
    if inning_half_str not in ('top', 'bottom'):
        raise ValueError('Invalid inning half str.')

    plate_appearance_list = []
    inning_num = len(game_obj.inning_list) + 1
    next_batter_num = 1
    for plate_appearance_dict in plate_appearance_dict_list:
        event_list = []
        if plate_appearance_dict['result'].get('event') == 'Game Advisory':
            continue

        plate_appearance_list.append(
            process_at_bat(
                plate_appearance_dict,
                event_list,
                game_obj,
                inning_half_str,
                inning_num,
                next_batter_num
            )
        )

        next_batter_num += 1

    return plate_appearance_list

def process_inning(baseball_inning, game_obj):
    top_half_appearance_list = process_half_inning(
        baseball_inning['top'],
        'top',
        game_obj
    ) or []

    if baseball_inning.get('bottom'):
        bottom_half_appearance_list = process_half_inning(
            baseball_inning['bottom'],
            'bottom',
            game_obj
        )
    else:
        bottom_half_appearance_list = []

    if top_half_appearance_list and top_half_appearance_list[-1] is None:
        del top_half_appearance_list[-1]
    if bottom_half_appearance_list and bottom_half_appearance_list[-1] is None:
        del bottom_half_appearance_list[-1]

    this_inning_obj = baseball.Inning(top_half_appearance_list,
                                      bottom_half_appearance_list)

    return this_inning_obj

def set_game_inning_list(inning_dict_list, game_obj):
    for _, inning_dict in enumerate(inning_dict_list):
        game_obj.inning_list.append(process_inning(inning_dict, game_obj))

def get_object_html_str(game_html_id_list):
    object_html_str = ''
    for i, game_html_id in enumerate(game_html_id_list):
        game_id_element_list = game_html_id.split('-')
        title_str = '{} @ {} ({:04d}-{:02d}-{:02d}, {})'.format(
            game_id_element_list[3],
            game_id_element_list[4],
            int(game_id_element_list[0]),
            int(game_id_element_list[1]),
            int(game_id_element_list[2]),
            game_id_element_list[5]
        )

        if i % 2 == 0:
            object_html_str += '<tr>'

        object_html_str += OBJECT_ENTRY_TEMPLATE.format(
            title_str=title_str,
            game_id_str=game_html_id
        )

        if i % 2 == 1:
            object_html_str += '</tr>'

    return object_html_str

def write_games_for_date(this_datetime, output_dir, write_game_html,
                         write_date_html, write_index_html):
    if not exists(output_dir):
        mkdir(output_dir)

    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year
    all_games_dict = get(
        ALL_GAMES_2020_URL.format(month=month, day=day, year=year)
    ).json()

    game_tuple_list = [(x['id'], x['game_pk'])
                       for x in all_games_dict['data']['games'].get('game', [])]

    game_dict_list = [get(GAME_URL_2020_TEMPLATE.format(game_pk=game_pk)).json()
                      for _, game_pk in game_tuple_list]

    game_html_id_list = []
    for game_dict in game_dict_list:
        try:
            game = initialize_game(
                game_dict,
                game_dict.get('gameData', {}).get('gameInfo', {}).get('attendance', ''),
                game_dict.get('gameData', {}).get('weather', {}).get('temp', ''),
                game_dict.get('gameData', {}).get('weather', {}).get('condition', '')
            )

            inning_dict_list = get_inning_dict_list(game_dict)
            set_game_inning_list(inning_dict_list, game)
            set_pitcher_wls_codes(game_dict, game)

            if game.home_team.batting_order_list_list[0] is None:
                game.home_team.batting_order_list_list = [[]] * 9

            if game.away_team.batting_order_list_list[0] is None:
                game.away_team.batting_order_list_list = [[]] * 9

            game.set_batting_box_score_dict()
            game.set_pitching_box_score_dict()
            game.set_team_stats()
            game.set_gametimes()

            if len(game.game_date_str.split('-')) == 6:
                game_html_id_list.append(game.game_date_str)
            else:
                game.game_date_str = '{:04d}-{:02d}-{:02d}-{}'.format(
                    year, month, day, game.game_date_str
                )

                if len(game.game_date_str.split('-')) == 6:
                    game_html_id_list.append(game.game_date_str)

            write_game_svg_and_html(game.game_date_str, game, output_dir,
                                    write_game_html)
        except:
            exc_type, exc_value, exc_traceback = exc_info()
            lines = format_exception(exc_type, exc_value, exc_traceback)
            exception_str = ' '.join(lines)
            print('{} {} {}'.format(datetime.utcnow(),
                                    game_dict['gameData']['game']['id'],
                                    exception_str))

    object_html_str = get_object_html_str(game_html_id_list)
    month_list = []
    for index in range(12):
        if index == month - 1:
            month_list.append('selected')
        else:
            month_list.append('')

    day_list = []
    for index in range(32):
        if index == day - 1:
            day_list.append('selected')
        else:
            day_list.append('')

    year_list = []
    for index in range(2500):
        if index == year:
            year_list.append('selected')
        else:
            year_list.append('')

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
        int(year), int(month), int(day)
    )

    output_html = HTML_INDEX_PAGE.format(
        result_object_list_str=object_html_str,
        month_list=month_list,
        day_list=day_list,
        year_list=year_list,
        yesterday_html=yesterday_html,
        tomorrow_html=tomorrow_html,
        today_str=today_str,
        output_filename=output_filename
    )

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
    for game_dict in game_dict_list:
        away_code = (
            game_dict.get('gameData', {}).get('teams', {}).get('away', {}).get('abbreviation', {})
        )

        home_code = (
            game_dict.get('gameData', {}).get('teams', {}).get('home', {}).get('abbreviation', {})
        )

        game_number_is_match = (
            this_game_number == game_dict.get('gameData', {}).get('game', {}).get('gameNumber', {})
        )

        if ((away_code and home_code) and (away_code == this_away_code) and
                (home_code == this_home_code) and game_number_is_match):
            game = initialize_game(game_dict, '', '', '')
            set_game_inning_list(get_inning_dict_list(game_dict), game)
            set_pitcher_wls_codes(game_dict, game)
            game.set_batting_box_score_dict()
            game.set_pitching_box_score_dict()
            game.set_team_stats()
            game.set_gametimes()

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
        write_game_svg_and_html(game_id, game, output_path, True)

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
        this_game = get_game_obj(boxscore_xml_obj,
                                 players_xml_obj,
                                 inning_xml_obj)

    return this_game

def write_svg_from_file_range(start_date_str, end_date_str, input_dir,
                              output_dir):
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

    write_game_svg_and_html(game_id, game, output_path, False)

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

def get_game_from_url_2020(date_str, this_date, away_code, home_code,
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

def get_game_from_url_2019(date_str, away_code, home_code, game_number):
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

def get_game_from_url(date_str, away_code, home_code, game_number):
    this_date = parse(date_str)
    if int(this_date.year) >= 2020:
        game_id, this_game = get_game_from_url_2020(
            date_str, this_date, away_code, home_code, game_number
        )
    else:
        game_id, this_game = get_game_from_url_2019(
            date_str, away_code, home_code, game_number
        )

    return game_id, this_game

def generate_today_game_svgs(output_dir, write_game_html=False,
                             write_date_html=False, write_index_html=False):
    time_shift = timedelta(hours=7)
    for i in range(0, 1):
        today_datetime = datetime.utcnow() - time_shift - timedelta(days=i)
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
