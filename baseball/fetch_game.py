from copy import deepcopy
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
from baseball.process_game_xml import (MLB_TEAM_CODE_DICT,
                                       MLB_REVERSE_TEAM_CODE_DICT)

EASTERN_TIMEZONE_STR = 'America/New_York'
NUM_PROCESS_SUBLISTS = 3
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
INNING_SUFFIX = 'inning/inning_all.xml'

ALL_GAMES_URL = ('http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1'
                     '&startDate={year:04d}-{month:02d}-{day:02d}'
                     '&endDate={year:04d}-{month:02d}-{day:02d}')

GAME_URL_TEMPLATE = 'http://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'

MLB_URL_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                   'month_{month}/day_{day}/gid_{year}_{month}_{day}_'
                   '{away_mlb_code}mlb_{home_mlb_code}mlb_{game_number}/')

HTML_INDEX_PAGE = (
    '<html>'
    '<head>'
    '<meta http-equiv="Pragma" content="no-cache">'
    '<meta http-equiv="Expires" content="0">'
    '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">'
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
    '<link rel="icon" type="image/png" href="/team_logos/baseball-fairy-161.png" />'
    '<meta name="viewport" content="width=device-width, initial-scale=0.35">'
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
    'window.location = "/{yesterday_html}";'
    '}}'
    '</script>'
    '<script>'
    'function goforwardone() {{'
    'window.location = "/{tomorrow_html}";'
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
    'window.location = "/" + document.getElementById("year").value +'
    ' "-" + document.getElementById("month").value + "-" +'
    ' document.getElementById("day").value + ".html";'
    '}}'
    'function setdelay() {{'
    'if (typeof window.location.href.split(\'/\')[4] !== \'undefined\') {{'
    'document.getElementById("delay").innerHTML = "Current time delay: " + '
    'secondsToHms(window.location.href.split(\'/\')[4]);'
    '}}'
    '}}'
    'function applydelay() {{'
    'var sec_delay = Math.ceil(document.getElementById("delay_seconds").value / 5) * 5; '
    'if (sec_delay > 1800) {{ sec_delay = 1800; }}'
    'window.location = "/delay/" + sec_delay + "/index.html"; ' 
    '}}'
    'function secondsToHms(d) {{'
    'd = Number(d);'
    'var h = Math.floor(d / 3600);'
    'var m = Math.floor(d % 3600 / 60);'
    'var s = Math.floor(d % 3600 % 60);'
    'var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";'
    'var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";'
    'var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";'
    'var return_str = hDisplay + mDisplay + sDisplay;'
    'return_str = return_str.trim();'
    'if (return_str.charAt(return_str.length - 1) === \',\') {{'
    'return_str = return_str.slice(0, -1); '
    '}}'
    'return return_str; }}'
    '</script>'
    '<title>Live Baseball Scorecards</title>'
    '</head>'
    '<body style="background-color:black;" onload="setdelay()">'
    '<div id="delay-header" style="width:100%; background:#282828; '
    'margin:0 auto; text-align: left;">'
    '<font size="4" color="white">Set time delay (seconds): '
    '<input type="text" id="delay_seconds" name="delay_seconds">'
    '<input type="submit" value="Apply" onclick="applydelay()">'
    '<input type="submit" value="Reset" '
    'onclick="window.location = \'https://livebaseballscorecards.com\';">'
    '<div id="delay"></div>'
    '</font>'
    '</div>'
    '<br />'
    '<div id="header" style="width:1160px; margin:0 auto; '
    'text-align: center;">'
    '<img src="/team_logos/baseball-fairy-bat-250.png" height="250"><br />'
    '<font size="7" color="white">'
    'LiveBaseballScorecards.com'
    '</font><br />'
    '<font size="5" color="white">'
    'Contact us at '
    '<a href="mailto:livebaseballscorecards@gmail.com" '
    'style="color:lightblue">livebaseballscorecards@gmail.com</a>'
    '<br />'
    'For abbreviation definitions, hover your mouse over the scorecard '
    'text or click <a style="color:lightblue" href="/abbreviations.html">'
    'here</a>.'
    '<br>Download a PDF of any season for any team from the '
    '<a style="color:lightblue" href="/archive.html">Scorebook PDF Archive</a>.'
    '<br />'
    '<br />'
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
    '<option {year_list[2029]} value="2029">2029</option>'
    '<option {year_list[2028]} value="2028">2028</option>'
    '<option {year_list[2027]} value="2027">2027</option>'
    '<option {year_list[2026]} value="2026">2026</option>'
    '<option {year_list[2025]} value="2025">2025</option>'
    '<option {year_list[2024]} value="2024">2024</option>'
    '<option {year_list[2023]} value="2023">2023</option>'
    '<option {year_list[2022]} value="2022">2022</option>'
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
    '<option {year_list[2009]} value="2009">2009</option>'
    '<option {year_list[2008]} value="2008">2008</option>'
    '<option {year_list[2007]} value="2007">2007</option>'
    '<option {year_list[2006]} value="2006">2006</option>'
    '<option {year_list[2005]} value="2005">2005</option>'
    '<option {year_list[2004]} value="2004">2004</option>'
    '<option {year_list[2003]} value="2003">2003</option>'
    '<option {year_list[2002]} value="2002">2002</option>'
    '<option {year_list[2001]} value="2001">2001</option>'
    '<option {year_list[2000]} value="2000">2000</option>'
    '<option {year_list[1999]} value="1999">1999</option>'
    '<option {year_list[1998]} value="1998">1998</option>'
    '<option {year_list[1997]} value="1997">1997</option>'
    '<option {year_list[1996]} value="1996">1996</option>'
    '<option {year_list[1995]} value="1995">1995</option>'
    '<option {year_list[1994]} value="1994">1994</option>'
    '<option {year_list[1993]} value="1993">1993</option>'
    '<option {year_list[1992]} value="1992">1992</option>'
    '<option {year_list[1991]} value="1991">1991</option>'
    '<option {year_list[1990]} value="1990">1990</option>'
    '<option {year_list[1989]} value="1989">1989</option>'
    '<option {year_list[1988]} value="1988">1988</option>'
    '<option {year_list[1987]} value="1987">1987</option>'
    '<option {year_list[1986]} value="1986">1986</option>'
    '<option {year_list[1985]} value="1985">1985</option>'
    '<option {year_list[1984]} value="1984">1984</option>'
    '<option {year_list[1983]} value="1983">1983</option>'
    '<option {year_list[1982]} value="1982">1982</option>'
    '<option {year_list[1981]} value="1981">1981</option>'
    '<option {year_list[1980]} value="1980">1980</option>'
    '<option {year_list[1979]} value="1979">1979</option>'
    '<option {year_list[1978]} value="1978">1978</option>'
    '<option {year_list[1977]} value="1977">1977</option>'
    '<option {year_list[1976]} value="1976">1976</option>'
    '<option {year_list[1975]} value="1975">1975</option>'
    '<option {year_list[1974]} value="1974">1974</option>'
    '<option {year_list[1973]} value="1973">1973</option>'
    '<option {year_list[1972]} value="1972">1972</option>'
    '<option {year_list[1971]} value="1971">1971</option>'
    '<option {year_list[1970]} value="1970">1970</option>'
    '<option {year_list[1969]} value="1969">1969</option>'
    '<option {year_list[1968]} value="1968">1968</option>'
    '<option {year_list[1967]} value="1967">1967</option>'
    '<option {year_list[1966]} value="1966">1966</option>'
    '<option {year_list[1965]} value="1965">1965</option>'
    '<option {year_list[1964]} value="1964">1964</option>'
    '<option {year_list[1963]} value="1963">1963</option>'
    '<option {year_list[1962]} value="1962">1962</option>'
    '<option {year_list[1961]} value="1961">1961</option>'
    '<option {year_list[1960]} value="1960">1960</option>'
    '<option {year_list[1959]} value="1959">1959</option>'
    '<option {year_list[1958]} value="1958">1958</option>'
    '<option {year_list[1957]} value="1957">1957</option>'
    '<option {year_list[1956]} value="1956">1956</option>'
    '<option {year_list[1955]} value="1955">1955</option>'
    '<option {year_list[1954]} value="1954">1954</option>'
    '<option {year_list[1953]} value="1953">1953</option>'
    '<option {year_list[1952]} value="1952">1952</option>'
    '<option {year_list[1951]} value="1951">1951</option>'
    '<option {year_list[1950]} value="1950">1950</option>'
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
    '<meta http-equiv="Pragma" content="no-cache">'
    '<meta http-equiv="Expires" content="0">'
    '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">'
    '<title>{title}</title>'
    '<link rel="icon" type="image/png" href="/team_logos/baseball-fairy-161.png" />'
    '<script>'
    'function setdelay() {{'
    'if (typeof window.location.href.split(\'/\')[4] !== \'undefined\') {{'
    'document.getElementById("delay").innerHTML = "Current time delay: " + '
    'secondsToHms(window.location.href.split(\'/\')[4]);'
    '}}'
    '}}'
    'function applydelay() {{'
    'var sec_delay = Math.ceil(document.getElementById("delay_seconds").value / 5) * 5; '
    'if (sec_delay > 1800) {{ sec_delay = 1800; }}'
    'url_array = window.location.href.split(\'/\'); '
    'file_name = url_array.slice(-1)[0]; '
    'window.location = "/delay/" + sec_delay + "/" + file_name; ' 
    '}}'
    'function resetdelay() {{'
    'url_array = window.location.href.split(\'/\'); '
    'file_name = url_array.slice(-1)[0];'
    'window.location = \'https://livebaseballscorecards.com/\' + file_name; '
    '}}'
    'function secondsToHms(d) {{'
    'd = Number(d);'
    'var h = Math.floor(d / 1800);'
    'var m = Math.floor(d % 1800 / 60);'
    'var s = Math.floor(d % 1800 % 60);'
    'var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";'
    'var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";'
    'var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";'
    'var return_str = hDisplay + mDisplay + sDisplay;'
    'return_str = return_str.trim();'
    'if (return_str.charAt(return_str.length - 1) === \',\') {{'
    'return_str = return_str.slice(0, -1); '
    '}}'
    'return return_str; }}'
    '</script>'
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
    '<body style="background-color:black;" onload="setdelay()">'
    '<div id="delay-header" style="width:100%; background:#282828; '
    'margin:0 auto; text-align: left;">'
    '<font size="4" color="white">'#Set time delay (seconds): '
    #'<input type="text" id="delay_seconds" name="delay_seconds">'
    #'<input type="submit" value="Apply" onclick="applydelay()">'
    #'<input type="submit" value="Reset" '
    #'onclick="resetdelay()">'
    '<div id="delay"></div>'
    '</font>'
    '</div>'
    '<div align="center">'
    '<object id="{title}"></object>'
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

def get_object_html_str(game_html_id_tuple_list):
    object_html_str = ''
    list_index = 0
    for i, (game_html_id, game) in enumerate(game_html_id_tuple_list):
        if i > 0:
            look_behind_id, _ = game_html_id_tuple_list[i-1]
        else:
            look_behind_id = None

        if (not game) or (not game.is_today) or (look_behind_id == game_html_id):
            continue

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
                    (not (est_time.hour == 0 and est_time.minute == 0)) and
                    (not (game.is_suspended and not game.is_today))):
                title_str += '{}'.format(
                    start_datetime.strftime('%-I:%M %p %Z')
                )

                subtitle_flag = True

            if game.is_doubleheader:
                if subtitle_flag:
                    title_str += ' - '

                title_str += 'Game {}'.format(game.game_date_str[-1])
                subtitle_flag = True

            if game.is_suspended:
                if subtitle_flag:
                    title_str += ' - '

                title_str += 'Suspended'
                subtitle_flag = True
            elif game.is_postponed:
                if subtitle_flag:
                    title_str += ' - '

                title_str += 'Postponed'
                subtitle_flag = True
        if list_index % 2 == 0:
            object_html_str += '<tr>'

        object_html_str += OBJECT_ENTRY_TEMPLATE.format(
            title_str=title_str,
            game_id_str=game_html_id
        )

        if list_index % 2 == 1:
            object_html_str += '</tr>'

        list_index += 1

    return object_html_str

def write_games_for_date(this_datetime, output_dir, write_game_html=False,
                         write_date_html=False, write_index_html=False):
    generate_game_svgs_for_datetime(this_datetime, output_dir,
                                    write_game_html, write_date_html,
                                    write_index_html)

def generate_game_svgs_for_datetime(this_datetime, output_dir,
                                    write_game_html, write_date_html,
                                    write_index_html):
    if not exists(output_dir):
        mkdir(output_dir)

    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year
    date_str = '{}-{}-{}'.format(year, month, day)
    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    if len(all_games_dict['dates']) == 0:
        game_dict_list = []
        game_tuple_list = []
    else:
        game_tuple_list = [(None, x['gamePk'])
                           for x in all_games_dict['dates'][0]['games']]

        game_dict_list = [get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
                          for _, game_pk in game_tuple_list]

    game_html_id_tuple_list = []
    for i, game_dict in enumerate(game_dict_list):
        try:
            is_doubleheader = game_is_doubleheader(i, game_dict, game_dict_list)
            both_teams_players_id_list = get_both_teams_players(game_dict['liveData']['boxscore']['teams'])
            list_len = len(both_teams_players_id_list)
            if both_teams_players_id_list and list_len <= 6:
                binary_str_list = [
                    '{:0{width}b}'.format(k, width=list_len) for k in range(2 ** list_len)
                ]
                for this_str in binary_str_list:
                    game_dict_copy = deepcopy(game_dict)
                    for i, this_char in enumerate(this_str):
                        this_player_id = both_teams_players_id_list[i]
                        if this_char == '1':
                            del(game_dict_copy['liveData']['boxscore']['teams']['home']['players'][this_player_id])
                        elif this_char == '0':
                            del(game_dict_copy['liveData']['boxscore']['teams']['away']['players'][this_player_id])
                        else:
                            raise Exception("Should be binary string")

                    try:
                        game = baseball.process_game_json.get_game_obj(game_dict_copy,
                                                                       is_doubleheader)
                    except:
                        exc_type, exc_value, exc_traceback = exc_info()
                        lines = format_exception(exc_type, exc_value, exc_traceback)
                        exception_str = ' '.join(lines)
                        print('{} {{} {}'.format(datetime.utcnow(),
                                                 date_str,
                                                 exception_str))

                        continue

                    break


            else:
                game = baseball.process_game_json.get_game_obj(game_dict,
                                                               is_doubleheader)

            set_game_status(game, this_datetime)

            if len(game.game_date_str.split('-')) == 6:
                game_html_id_tuple_list.append((game.game_date_str, game))
            else:
                game.game_date_str = '{:04d}-{:02d}-{:02d}-{}'.format(
                    year, month, day, game.game_date_str
                )

                if len(game.game_date_str.split('-')) == 6:
                    game_html_id_tuple_list.append((game.game_date_str, game))

            write_game_svg_and_html(game.game_date_str, game, output_dir,
                                    write_game_html)
        except:
            exc_type, exc_value, exc_traceback = exc_info()
            lines = format_exception(exc_type, exc_value, exc_traceback)
            exception_str = ' '.join(lines)
            if 'gameData' in game_dict:
                print('{} {} {}'.format(datetime.utcnow(),
                                        game_dict['gameData']['game']['id'],
                                        exception_str))
            else:
                print('{} {} {}'.format(datetime.utcnow(),
                                        "gameData not in game_dict",
                                        exception_str))

    object_html_str = get_object_html_str(game_html_id_tuple_list)

    write_game_index(object_html_str, this_datetime, output_dir,
                     write_date_html, write_index_html)

def game_is_doubleheader(i, game_dict, game_dict_list):
    is_doubleheader = False
    this_id = game_dict['gameData']['game']['id'].split('/')[-1]
    if i < (len(game_dict_list) - 1):
        next_id = game_dict_list[i+1]['gameData']['game']['id'].split('/')[-1]
        if next_id[:-2] == this_id[:-2] and next_id != this_id:
            is_doubleheader = True

    look_behind_id = game_dict_list[i-1]['gameData']['game']['id'].split('/')[-1]
    if look_behind_id[:-2] == this_id[:-2] and look_behind_id != this_id:
        is_doubleheader = True

    return is_doubleheader

def set_game_status(game, this_datetime):
    now_date = this_datetime.date()
    est_date = (game.start_datetime if game.start_datetime
                else game.expected_start_datetime).astimezone(
                    timezone(game.timezone_str)
                ).date()

    if est_date != now_date:
        game.is_today = False
        if est_date > now_date:
            game.is_postponed = True

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

def get_both_teams_players(teams_dict):
    home_player_key_list = teams_dict['home']['players'].keys()
    away_player_key_list = teams_dict['away']['players'].keys()
    duplicate_key_list = list(set(home_player_key_list) & set(away_player_key_list))
    return duplicate_key_list

def get_game_from_date(this_datetime, this_away_code, this_home_code,
                           this_game_number):
    month = this_datetime.month
    day = this_datetime.day
    year = this_datetime.year
    all_games_dict = get(
        ALL_GAMES_URL.format(month=month, day=day, year=year)
    ).json()

    game_list = []
    for x in all_games_dict['dates']:
        for y in x['games']:
            game_list.append(y['gamePk'])

    game_dict_list = [get(GAME_URL_TEMPLATE.format(game_pk=game_pk)).json()
                      for game_pk in game_list]

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
            is_doubleheader = game_is_doubleheader(i, game_dict, game_dict_list)

            game = baseball.process_game_json.get_game_obj(game_dict,
                                                           is_doubleheader)

            set_game_status(game, this_datetime)

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

    old_svg_text = ''
    if exists(output_svg_path):
        with open(output_svg_path, 'r') as filehandle:
            old_svg_text = filehandle.read()

    if old_svg_text != svg_text:
        with open(output_svg_path, 'w') as filehandle:
            filehandle.write(svg_text)

        if write_html:
            with open(output_html_path, 'w') as filehandle:
                filehandle.write(html_text)

def get_game_from_file(live_json_file):
    this_game = None

    try:
        if isfile(live_json_file):
            live_raw = open(live_json_file, 'r', encoding='utf-8').read()
            game_dict = loads(live_raw)
            this_game = baseball.process_game_json.get_game_obj(game_dict)
            if this_game and len(this_game.game_date_str) < 16:
                this_game.game_date_str = f"{live_json_file.split('/')[-1][0:10]}-{this_game.game_date_str}"
    except:
        exc_type, exc_value, exc_traceback = exc_info()
        lines = format_exception(exc_type, exc_value, exc_traceback)
        exception_str = ' '.join(lines)
        print('{} ({}) {}'.format(datetime.utcnow(),
                                  live_json_file,
                                  exception_str))

    if this_game:
        return_str = this_game.game_date_str
    else:
        return_str = ''

    return return_str, this_game

def get_game_generator(filename_list):
    for filename in filename_list:
        game_id, this_game = get_game_from_file(filename)
        if this_game:
            yield game_id, this_game

def write_game_svg_html_from_filename(filename_output_path_tuple,
                                      write_game_html=False):
    filename, output_path = filename_output_path_tuple
    game_id, game = get_game_from_file(filename)
    if game:
        write_game_svg_and_html(game_id, game, output_path, write_game_html)

def write_svg_from_file_range(start_date_str, end_date_str, input_dir,
                              output_dir, write_game_html=False,
                              write_date_html=False):
    if not exists(output_dir):
        makedirs(output_dir)

    output_path = abspath(output_dir)
    filename_output_path_tuple_list = [
        (filename, output_path)
        for filename in get_filename_list(start_date_str, end_date_str, input_dir)
    ]

    start_datetime = parse(start_date_str)
    end_datetime = parse(end_date_str)
    day_interval = timedelta(days=1)
    this_datetime = start_datetime
    while this_datetime <= end_datetime:
        try:
            game_html_id_tuple_list = []
            for tup in filename_output_path_tuple_list:
                filename, _ = tup
                if str(this_datetime).split()[0] in filename:
                    write_game_svg_html_from_filename(tup, write_game_html)
                    game_html_id_tuple_list.append(get_game_from_file(filename))

            object_html_str = get_object_html_str(game_html_id_tuple_list)
            write_game_index(object_html_str, this_datetime, output_dir,
                             write_date_html, False)
        except:
            exc_type, exc_value, exc_traceback = exc_info()
            lines = format_exception(exc_type, exc_value, exc_traceback)
            exception_str = ' '.join(lines)
        #    print('{} ({}) {}'.format(datetime.utcnow(),
        #                              str(this_datetime),
        #                              exception_str))

        this_datetime += day_interval

def get_filename_list(start_date_str, end_date_str, input_dir):
    return_filename_list = []
    input_path = abspath(input_dir)
    input_dir_file_list = listdir(input_path)
    start_date = parse(start_date_str)
    end_date = parse(end_date_str)
    day_delta = timedelta(days=1)
    this_date = start_date
    while this_date < end_date + day_delta:
        year = str(this_date.year)
        month = str(this_date.month).zfill(2)
        day = str(this_date.day).zfill(2)
        this_date_str = '{}-{}-{}-'.format(year, month, day)
        file_list = [this_filename
                     for this_filename in input_dir_file_list
                     if this_date_str in this_filename]

        for this_file in file_list:
            return_filename_list.append('{}/{}'.format(input_path, this_file))

        this_date += day_delta

    return return_filename_list

def get_game_list_from_file_range(start_date_str, end_date_str, input_dir,
                                    ):
    filename_list = get_filename_list(start_date_str, end_date_str, input_dir)
    process_pool = Pool(NUM_PROCESS_SUBLISTS)
    #game_tuple_list = process_pool.map(get_game_from_file,
    #                                   filename_list)
    game_tuple_list = [get_game_from_file(filename)
                       for filename in filename_list]

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

def get_game_from_url(date_str, away_code, home_code,
                      game_number):
    this_date = parse(date_str)
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

def generate_today_game_svgs(output_dir, write_game_html=False,
                             write_date_html=False, write_index_html=False):
    time_shift = timedelta(minutes=545)
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
