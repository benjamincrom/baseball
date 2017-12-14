from collections import OrderedDict, namedtuple

InningStatsTuple = namedtuple('InningStatsTuple', 'S P BB K LOB E H R')
BatterBoxScore = namedtuple('BatterBoxScore', 'AB R H RBI BB SO LOB')

PitcherBoxScore = namedtuple(
    'PitcherBoxScore',
    'IP WLS BF H R ER SO BB IBB HBP BLK WP HR S P ERA WHIP'
)

TeamBoxScore = namedtuple(
    'TeamBoxScore',
    'B1 B2 B3 HR SF SAC DP HBP WP PB SB CS PA'
)

FakePlateAppearance = namedtuple(
    'FakePlateAppearance',
    'scorecard_summary batter plate_appearance_description'
)

HEIGHT = 4513
WIDTH = 3192
BOX_WIDTH = 266
BOX_HEIGHT = 200
EXTRA_COLUMNS = 3

NUM_MINIMUM_INNINGS = 9
LEN_BATTING_LIST = 9
AUTOMATIC_BALL_POSITION = (1.0, 1.0)
AUTOMATIC_BALL_COORDINATE = (300, 300)
PITCH_X_MAX = 57
PITCH_Y_MIN = 107
PITCH_MAX_COORD = 250.0
PITCH_BOX_WIDTH = 50
PITCH_BOX_HEIGHT = 90
PITCH_TYPE_X_OFFSET = 16
PITCH_SPEED_X_OFFSET = 39
FIRST_PITCH_X_VAL = 3
FIRST_PITCH_Y_VAL = 15
PITCHER_LARGE_FONT_SIZE = 20
PITCHER_SMALL_FONT_SIZE = 13
PITCHER_STATS_LARGE_FONT_SIZE = 15
PITCHER_STATS_SMALL_FONT_SIZE = 10
PITCHER_BOX_SCORE_LARGE_Y = 70
PITCHER_BOX_SCORE_SMALL_Y = 56
PITCHER_BOX_SCORE_X_INCREMENT = 70
PITCHER_BOX_SCORE_LARGE_Y_INCREMENT = 40
PITCHER_BOX_SCORE_SMALL_Y_INCREMENT = 26
PITCHER_BOX_STATS_LARGE_Y_OFFSET = 73
PITCHER_BOX_STATS_SMALL_Y_OFFSET = 67
SMALL_CHUNK_SIZE = 5
LARGE_CHUNK_SIZE = 8
PITCH_Y_LIMIT = 132
PITCH_X_OFFSET = 67
PITCH_Y_OFFSET = 14
PITCH_ROW_2_Y_VAL = FIRST_PITCH_Y_VAL + PITCH_Y_OFFSET
OUT_CIRCLE_Y_VAL = 11
OUT_TEXT_Y_OFFSET = 5
OUT_CIRCLE_Y_OFFSET = 19
RUNNER_SUMMARY_Y_VAL = 155
RUNNER_SUMMARY_Y_OFFSET = 20
PITCHER_Y = 150
PITCHER_X = 166
CATCHER_Y = 180
FIRST_BASE_Y = 115
FIRST_BASE_X = 220
SECOND_BASE_Y = 80
SECOND_BASE_X = 186
THIRD_BASE_X = 112
SHORTSTOP_Y = 100
SHORTSTOP_X = 140
LEFT_FIELDER_Y = 58
LEFT_FIELDER_X = 105
CENTER_FIELDER_Y = 35
RIGHT_FIELDER_X = 225
BATTER_FONT_SIZE_BIG = 20
BATTER_FONT_SIZE_MED = 15
BATTER_FONT_SIZE_SMALL = 10
BATTER_SPACE_BIG = 38
BATTER_SPACE_MED = 22
BATTER_SPACE_SMALL = 15
BATTER_STATS_OFFSET_BIG = 15
BATTER_STATS_OFFSET_MED = 10
BATTER_STATS_OFFSET_SMALL = 6
BATTER_STATS_SPACES_BIG = 4
BATTER_STATS_SPACES_MED = 6
BATTER_STATS_SPACES_SMALL = 10
BATTER_INITIAL_Y_POS = 25

RED_COLOR = '#c10000'
BLUE_COLOR = 'blue'
DARK_GREEN_COLOR = 'darkgreen'
BLACK_COLOR = 'black'
BOXSCORE_SUFFIX = 'boxscore.xml'
PLAYERS_SUFFIX = 'players.xml'
GAME_SUFFIX = 'inning/inning_all.xml'

INCREMENT_BASE_DICT = {'1st': '2nd',
                       '2nd': '3rd',
                       '3rd': 'home'}

MLB_TEAM_CODE_DICT = {'LAA': 'ana',
                      'SEA': 'sea',
                      'BAL': 'bal',
                      'CLE': 'cle',
                      'CIN': 'cin',
                      'NYM': 'nyn',
                      'COL': 'col',
                      'LAD': 'lan',
                      'DET': 'det',
                      'TOR': 'tor',
                      'HOU': 'hou',
                      'OAK': 'oak',
                      'MIA': 'mia',
                      'ATL': 'atl',
                      'MIL': 'mil',
                      'CHC': 'chn',
                      'MIN': 'min',
                      'KC': 'kca',
                      'NYY': 'nya',
                      'TEX': 'tex',
                      'PHI': 'phi',
                      'WSH': 'was',
                      'PIT': 'pit',
                      'STL': 'sln',
                      'SD': 'sdn',
                      'ARI': 'ari',
                      'SF': 'sfn',
                      'CHW': 'cha',
                      'TB': 'tba',
                      'BOS': 'bos'}

GET_TODAY_GAMES_USAGE_STR = (
    'Usage:\n'
    '  - ./get_today_games.py [OUTPUT DIRECTORY]\n'
)

GENERATE_SVG_USAGE_STR = (
    'Usage:\n'
    '  - ./generate_svg.py url [DATE] [AWAY CODE] [HOME CODE] '
    '[GAME NUMBER] [OUTPUT DIRECTORY]\n'
    '  - ./generate_svg.py files [START DATE] [END DATE] '
    '[OUTPUT DIRECTORY] [INPUT DIRECTORY]\n'
)

GET_XML_USAGE_STR = ('Usage:\n'
                     '  - ./get_xml_data.py url [DATE] [AWAY CODE] [HOME CODE] '
                     '[GAME NUMBER]\n'
                     '  - ./get_xml_data.py files [START DATE] [END DATE] '
                     '[INPUT DIRECTORY]\n')

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
    'Oriole Park at Camden Yards': 'America/New_York',
    'Nationals Park': 'America/New_York',
    'Champion Stadium': 'America/New_York',
    'SunTrust Park': 'America/New_York',
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
    'Globe Life Park in Arlington': 'America/Chicago',
    'Minute Maid Park': 'America/Chicago',
    'Kauffman Stadium': 'America/Chicago',
    'Coors Field': 'America/Denver',
    'Chase Field': 'America/Denver',
    'Safeco Field': 'America/Los_Angeles',
    'AT&T Park': 'America/Los_Angeles',
    'Oakland-Alameda County Coliseum': 'America/Los_Angeles',
    'Oakland Coliseum': 'America/Los_Angeles',
    'Angel Stadium of Anaheim': 'America/Los_Angeles',
    'Dodger Stadium': 'America/Los_Angeles',
    'Petco Park': 'America/Los_Angeles'
}

PLAY_CODE_ORDERED_DICT = OrderedDict([('picks off', 'PO'),
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
                                      ('sacrifice bunt', 'SB'),
                                      ('walks', 'BB'),
                                      ('intentionally walks', 'IBB'),
                                      ('called out on strikes', 'ꓘ'),
                                      ('strikes out', 'K'),
                                      ('choice', 'FC')])

POSITION_CODE_DICT = {'pitcher': 1,
                      'catcher': 2,
                      'first': 3,
                      'second': 4,
                      'third': 5,
                      'shortstop': 6,
                      'left': 7,
                      'center': 8,
                      'right': 9,
                      'designated': 10}

PITCH_TYPE_DESCRIPTION = {'Ball': 'B',
                          'Ball In Dirt': 'D',
                          'Called Strike': 'C',
                          'Automatic Strike': 'C',
                          'Swinging Strike': 'S',
                          'Strike': 'S',
                          'Swinging Pitchout': 'S',
                          'Foul': 'F',
                          'Foul Tip': 'T',
                          'Pitchout': 'P',
                          'Foul Pitchout': 'P',
                          'Balk': 'N',
                          'Hit By Pitch': 'H',
                          'Automatic Ball': 'I',
                          'Intent Ball': 'I',
                          'Foul Bunt': 'L',
                          'Missed Bunt': 'M',
                          'In play, run(s)': 'X',
                          'In play, out(s)': 'X',
                          'In play, no out': 'X'}

POSITION_ABBREV_DICT = {'P': 1,
                        'C': 2,
                        '1B': 3,
                        '2B': 4,
                        '3B': 5,
                        'SS': 6,
                        'LF': 7,
                        'CF': 8,
                        'RF': 9,
                        'DH': 10}

ON_BASE_SUMMARY_DICT = {'Single': '1B',
                        'Double': '2B',
                        'Triple': '3B',
                        'Hit By Pitch': 'HBP',
                        'Home Run': 'HR',
                        'Walk': 'BB',
                        'Intent Walk': 'IBB'}

NO_HIT_CODE_LIST = ['K', 'ꓘ', 'BB', 'IBB']
NOT_AT_BAT_CODE_LIST = ['SB', 'SF', 'BB', 'CI', 'FI', 'IBB', 'HBP', 'CS', 'PO']
HIT_CODE_LIST = ['1B', '2B', '3B', 'HR']

MLB_URL_BASE_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                        'month_{month}/day_{day}/')

MLB_URL_PATTERN = ('http://gd2.mlb.com/components/game/mlb/year_{year}/'
                   'month_{month}/day_{day}/gid_{year}_{month}_{day}_'
                   '{away_mlb_code}mlb_{home_mlb_code}mlb_{game_number}/')

HALF_SCALE_HEADER = '<g transform="scale(0.5)">'
HALF_SCALE_FOOTER = '</g>'

HTML_INDEX_PAGE = (
    '<html>'
      '<head>'
        '<link rel="icon" type="image/png" href="baseball-fairy-161.png" />'
        '<meta http-equiv="refresh" content="30">'
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
        '<title>Live Baseball Scorecards</title>'
      '</head>'
      '<body style="background-color:black;">'
        '<div id="header" style="width:1160px; margin:0 auto; '
        'text-align: center;">'
          '<img src="baseball-fairy-bat-250.png" height="250"><br />'
          '<font size="7" color="white">'
          'LiveBaseballScorecards.com'
          '</font><br /><br />'
          '<font size="6" color="white">Select a game</font>'
          '<br />'
          '<font size="3" color="white">'
            'Currently in beta testing.  Send error reports to '
            '<a href="mailto:livebaseballscorecards@gmail.com" '
            'style="color:lightblue">livebaseballscorecards@gmail.com</a>.'
            '<br /> '
          '<br />'
          '<br />'
          '<select name="away" id="away">'
            '<option value="">Away Team</option>'
            '<option value="ARI">Arizona Diamondbacks</option>'
            '<option value="ATL">Atlanta Braves</option>'
            '<option value="BAL">Baltimore Orioles,</option>'
            '<option value="BOS">Boston Red Sox</option>'
            '<option value="CHC">Chicago Cubs</option>'
            '<option value="CHW">Chicago White Sox</option>'
            '<option value="CIN">Cincinnati Reds</option>'
            '<option value="CLE">Cleveland Indians</option>'
            '<option value="COL">Colorado Rockies</option>'
            '<option value="DET">Detroit Tigers</option>'
            '<option value="HOU">Houston Astros</option>'
            '<option value="KC">Kansas City Royals</option>'
            '<option value="LAA">Los Angeles Angels</option>'
            '<option value="LAD">Los Angeles Dodgers</option>'
            '<option value="MIA">Miami Marlins</option>'
            '<option value="MIL">Milwaukee Brewers</option>'
            '<option value="MIN">Minnesota Twins</option>'
            '<option value="NYM">New York Mets</option>'
            '<option value="NYY">New York Yankees</option>'
            '<option value="OAK">Oakland A\'s</option>'
            '<option value="PHI">Philadephia Phillies</option>'
            '<option value="PIT">Pittsburgh Pirates</option>'
            '<option value="SEA">Seattle Mariners</option>'
            '<option value="SD">San Diego Padres</option>'
            '<option value="SF">San Francisco Giants</option>'
            '<option value="STL">St. Louis Cardinals</option>'
            '<option value="TB">Tampa Bay Rays</option>'
            '<option value="TEX">Texas Rangers</option>'
            '<option value="TOR">Toronto Blue Jays</option>'
            '<option value="WSH">Washington Nationals</option>'
          '</select>'
          '<font color="white">@</font>'
          '<select name="home" id="home">'
            '<option value="">Home Team</option>'
            '<option value="ARI">Arizona Diamondbacks</option>'
            '<option value="ATL">Atlanta Braves</option>'
            '<option value="BAL">Baltimore Orioles,</option>'
            '<option value="BOS">Boston Red Sox</option>'
            '<option value="CHC">Chicago Cubs</option>'
            '<option value="CHW">Chicago White Sox</option>'
            '<option value="CIN">Cincinnati Reds</option>'
            '<option value="CLE">Cleveland Indians</option>'
            '<option value="COL">Colorado Rockies</option>'
            '<option value="DET">Detroit Tigers</option>'
            '<option value="HOU">Houston Astros</option>'
            '<option value="KC">Kansas City Royals</option>'
            '<option value="LAA">Los Angeles Angels</option>'
            '<option value="LAD">Los Angeles Dodgers</option>'
            '<option value="MIA">Miami Marlins</option>'
            '<option value="MIL">Milwaukee Brewers</option>'
            '<option value="MIN">Minnesota Twins</option>'
            '<option value="NYM">New York Mets</option>'
            '<option value="NYY">New York Yankees</option>'
            '<option value="OAK">Oakland A\'s</option>'
            '<option value="PHI">Philadephia Phillies</option>'
            '<option value="PIT">Pittsburgh Pirates</option>'
            '<option value="SEA">Seattle Mariners</option>'
            '<option value="SD">San Diego Padres</option>'
            '<option value="SF">San Francisco Giants</option>'
            '<option value="STL">St. Louis Cardinals</option>'
            '<option value="TB">Tampa Bay Rays</option>'
            '<option value="TEX">Texas Rangers</option>'
            '<option value="TOR">Toronto Blue Jays</option>'
            '<option value="WSH">Washington Nationals</option>'
          '</select>'
          '<br />'
          '<br />'
          '<select name="month" id="month">'
            '<option value="01">January</option>'
            '<option value="02">February</option>'
            '<option value="03">March</option>'
            '<option value="04">April</option>'
            '<option value="05">May</option>'
            '<option value="06">June</option>'
            '<option value="07">July</option>'
            '<option value="08">August</option>'
            '<option value="09">September</option>'
            '<option value="10">October</option>'
            '<option value="11">November</option>'
            '<option value="12">December</option>'
          '</select>'
          '<select name="day" id="day">'
            '<option value="01">1</option>'
            '<option value="02">2</option>'
            '<option value="03">3</option>'
            '<option value="04">4</option>'
            '<option value="05">5</option>'
            '<option value="06">6</option>'
            '<option value="07">7</option>'
            '<option value="08">8</option>'
            '<option value="09">9</option>'
            '<option value="10">10</option>'
            '<option value="11">11</option>'
            '<option value="12">12</option>'
            '<option value="13">13</option>'
            '<option value="14">14</option>'
            '<option value="15">15</option>'
            '<option value="16">16</option>'
            '<option value="17">17</option>'
            '<option value="18">18</option>'
            '<option value="19">19</option>'
            '<option value="20">20</option>'
            '<option value="21">21</option>'
            '<option value="22">22</option>'
            '<option value="23">23</option>'
            '<option value="24">24</option>'
            '<option value="25">25</option>'
            '<option value="26">26</option>'
            '<option value="27">27</option>'
            '<option value="28">28</option>'
            '<option value="29">29</option>'
            '<option value="30">30</option>'
            '<option value="31">31</option>'
          '</select>'
          '<select name="year" id="year">'
            '<option value="2017">2017</option>'
            '<option value="2016">2016</option>'
            '<option value="2015">2015</option>'
            '<option value="2014">2014</option>'
            '<option value="2013">2013</option>'
            '<option value="2012">2012</option>'
            '<option value="2011">2011</option>'
            '<option value="2010">2010</option>'
            '<option value="2009">2009</option>'
            '<option value="2008">2008</option>'
          '</select>'
          '<br />'
          '<br />'
          '<font color="white">Game number: </font>'
          '<select name="game" id="game">'
            '<option value="1">1</option>'
            '<option value="2">2</option>'
          '</select>'
          '<br />'
          '<br />'
          '<script>'
            'function gotogame() {{'
              'window.location = "./" + document.getElementById("year").value +'
              ' "-" + document.getElementById("month").value + "-" +'
              ' document.getElementById("day").value + "-" +'
              ' document.getElementById("away").value + "-" +'
              ' document.getElementById("home").value + "-" +'
              ' document.getElementById("game").value + ".html";'
            '}}'
          '</script>'
          '<button onclick="gotogame()">Submit</button>'
          '<br />'
          '<br />'
          '<font size="6" color="white">Today\'s Games (live updates)</font>'
        '</div>'
        '<br />'
        '<table style="width:1160px" align="center">'
        '{result_object_list_str}'
        '</table>'
        '<script>'
          'window.addEventListener("scroll", function(e) {{ '
            'localStorage.setItem("last_scroll", $(window).scrollTop()); '
          '}}); \n'
          'if (localStorage.getItem("last_scroll")) {{ '
            '$(window).scrollTop(localStorage.getItem("last_scroll")); '
          '}} '
          'document.getElementById("day").onchange = function() {{ '
            'localStorage.setItem("dayselecteditem", '
            'document.getElementById("day").value); '
          '}} \n'
          'if (localStorage.getItem("dayselecteditem")) {{ '
            'document.getElementById("day").value =  '
            'localStorage.getItem("dayselecteditem"); '
          '}} '
          'document.getElementById("month").onchange = function() {{ '
            'localStorage.setItem("monthselecteditem",  '
            'document.getElementById("month").value); '
          '}} \n'
          'if (localStorage.getItem("monthselecteditem")) {{ '
            'document.getElementById("month").value =  '
            'localStorage.getItem("monthselecteditem"); '
          '}} '
          'document.getElementById("year").onchange = function() {{ '
            'localStorage.setItem("yearselecteditem",  '
            'document.getElementById("year").value); '
          '}} \n'
          'if (localStorage.getItem("yearselecteditem")) {{ '
            'document.getElementById("year").value =  '
            'localStorage.getItem("yearselecteditem"); '
          '}} '
          'document.getElementById("game").onchange = function() {{ '
            'localStorage.setItem("gameselecteditem",  '
            'document.getElementById("game").value); '
          '}} \n'
          'if (localStorage.getItem("gameselecteditem")) {{ '
            'document.getElementById("game").value =  '
            'localStorage.getItem("gameselecteditem"); '
          '}} '
          'document.getElementById("away").onchange = function() {{ '
            'localStorage.setItem("awayselecteditem",  '
            'document.getElementById("away").value); '
          '}} \n'
          'if (localStorage.getItem("awayselecteditem")) {{ '
            'document.getElementById("away").value =  '
            'localStorage.getItem("awayselecteditem"); '
          '}} '
          'document.getElementById("home").onchange = function() {{ '
            'localStorage.setItem("homeselecteditem",  '
            'document.getElementById("home").value); '
          '}} \n'
          'if (localStorage.getItem("homeselecteditem")) {{ '
            'document.getElementById("home").value =  '
            'localStorage.getItem("homeselecteditem"); '
          '}} '
        '</script>'
      '</body>'
    '</html>'
)

OBJECT_ENTRY_TEMPLATE = (
    '<tr><td>'
    '<div align="center">'
    '<font size="5" color="white">{title_str}</font>'
    '</div>'
    '</td></tr>'
    '<tr><td>'
    '<div align="center">'
    '<object width="1160px" data="./{game_id_str}.svg" type="image/svg+xml">'
    '</div>'
    '</td></tr>'
    '<tr><td><br /></td></tr>'
    '<tr><td><br /></td></tr>'
)


HTML_WRAPPER = (
    '<html>'
    '<head>'
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

BIG_SVG_HEADER = (
    '<?xml version="1.0" standalone="no"?>'
    '<svg width="100%" height="100%" viewBox="0 0 {width} 4513" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="{width}" height="4513" fill="#AAAAAA"/> '
    '<rect x="0" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="60" font-family="Arial" text-anchor="middle" '
    'font-size="30">Batter</text>'
    '<rect x="0" y="2256" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="2316" font-family="Arial" text-anchor="middle" '
    'font-size="30">Batter</text>'
    '<rect x="0" y="1900" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="1960" font-family="Arial" text-anchor="middle" '
    'font-size="30">Inning Stats</text>'
    '<rect x="0" y="4156" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="4216" font-family="Arial" text-anchor="middle" '
    'font-size="30">Inning Stats</text>'
    '<line x1="0" y1="2256" x2="{width}" y2="2256" stroke="black" '
    'stroke-width="1"/>'
)

PITCHER_STATS_HEADER = (
    '<svg x="{x_box}" y="{y_box}" width="1596" height="256" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="1596" height="256" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="150" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">PITCHER</text>'
    '<text x="345" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">IP</text>'
    '<text x="409" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">WLS</text>'
    '<text x="482" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">BF</text>'
    '<text x="545" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">H</text>'
    '<text x="615" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">R</text>'
    '<text x="685" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">ER</text>'
    '<text x="755" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">SO</text>'
    '<text x="825" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">BB</text>'
    '<text x="897" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">IBB</text>'
    '<text x="967" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">HBP</text>'
    '<text x="1037" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">BLK</text>'
    '<text x="1105" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">WP</text>'
    '<text x="1175" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">HR</text>'
    '<text x="1250" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">S</text>'
    '<text x="1320" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">P</text>'
    '<text x="1398" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">ERA</text>'
    '<text x="1475" y="35" font-family="Arial" text-anchor="middle" '
    'font-size="20">WHIP</text>'
)

PITCHER_STATS_LINE_TEMPLATE = (
    '<a target="_parent" xlink:href="http://m.mlb.com/player/{pitcher_id}">'
    '<text x="10" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start" fill="blue">{pitcher}</text></a>'
    '<text x="40" y="{stats_y_pos}" font-family="Arial" font-size="{size_2}" '
    'text-anchor="start">{stats}</text>'
    '<text x="260" y="{name_y_pos}" font-family="Arial" font-size="{size_2}" '
    'text-anchor="end">{appears}</text>'
    '<text x="330" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_1}</text>'
    '<text x="400" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_2}</text>'
    '<text x="470" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_3}</text>'
    '<text x="540" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_4}</text>'
    '<text x="610" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_5}</text>'
    '<text x="680" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_6}</text>'
    '<text x="750" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_7}</text>'
    '<text x="820" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_8}</text>'
    '<text x="890" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_9}</text>'
    '<text x="960" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_10}</text>'
    '<text x="1030" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_11}</text>'
    '<text x="1100" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_12}</text>'
    '<text x="1170" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_13}</text>'
    '<text x="1240" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_14}</text>'
    '<text x="1310" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_15}</text>'
    '<text x="1380" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_16}</text>'
    '<text x="1450" y="{name_y_pos}" font-family="Arial" font-size="{size_1}" '
    'text-anchor="start">{box_score_17}</text>'
)

INNING_STATS_BOX = (
    '<svg x="{box_x}" y="{box_y}" width="1596" height="256" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="40" y="28" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_1}</text>'
    '<text x="40" y="48" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_2}</text>'
    '<text x="40" y="68" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_3}</text>'
    '<text x="40" y="88" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_4}</text>'
    '<text x="140" y="28" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_5}</text>'
    '<text x="140" y="48" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_6}</text>'
    '<text x="140" y="68" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_7}</text>'
    '<text x="140" y="88" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_8}</text>'
    '<text x="192" y="28" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_9}</text>'
    '<text x="192" y="48" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_10}</text>'
    '<text x="192" y="68" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_11}</text>'
    '<text x="192" y="88" font-family="Arial" '
    'text-anchor="start" '
    'font-size="20">{stats_str_12}</text>'
    '</svg>'
)

TOTAL_BOX_SCORE_STATS_BOX = (
    '<svg x="{box_x}" y="{box_y}" width="266" height="400" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="400" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="50" y="60" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">AB</text>'
    '<text x="50" y="110" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">R</text>'
    '<text x="50" y="160" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">H</text>'
    '<text x="50" y="210" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">RBI</text>'
    '<text x="50" y="260" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">BB</text>'
    '<text x="50" y="310" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">SO</text>'
    '<text x="50" y="360" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">LOB</text>'
    '<text x="150" y="60" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_1}</text>'
    '<text x="150" y="110" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_2}</text>'
    '<text x="150" y="160" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_3}</text>'
    '<text x="150" y="210" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_4}</text>'
    '<text x="150" y="260" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_5}</text>'
    '<text x="150" y="310" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_6}</text>'
    '<text x="150" y="360" font-family="Arial" text-anchor="start" '
    'font-size="30" font-weight="bold">{stats_str_7}</text>'
    '</svg>'
)

BIG_SVG_COLUMN = (
    '<rect x="{x_pos}" y="0" width="266" height="100" fill="white" '
    'stroke="black" '
    'stroke-width="1"/>'
    '<text x="{text_x_pos}" y="60" font-family="Arial" '
    'text-anchor="middle" '
    'font-size="30">{inning_num}</text>'
    '<rect x="{x_pos}" y="2256" width="266" height="100" '
    'fill="white" '
    'stroke="black" '
    'stroke-width="1"/>'
    '<text x="{text_x_pos}" y="2316" font-family="Arial" '
    'text-anchor="middle" '
    'font-size="30">{inning_num}</text>'
    '<line x1="0" y1="2256" x2="{width}" y2="2256" '
    'stroke="black" stroke-width="1"/>'
)

BIG_SVG_TITLE = (
    '<svg width="266" height="1300" x="{x_pos}" y="{y_pos}" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="1300" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<rect x="0" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="67" font-family="Arial" text-anchor="middle" '
    'font-size="50">{inning_half}</text>'
    '<text x="95" y="700" transform="rotate(-90,95,700)" '
    'fill="black" font-size="55" font-family="Arial" text-anchor="middle" '
    '>{game_str}</text>'
    '<text x="165" y="700" transform="rotate(-90,165,700)" '
    'fill="black" font-size="45" font-family="Arial" text-anchor="middle" '
    '>{location}</text>'
    '<text x="220" y="700" transform="rotate(-90,220,700)" '
    'fill="black" font-size="30" font-family="Arial" text-anchor="middle" '
    '>{datetime}</text>'
    '</svg>'
)

BOX_SCORE_COLUMN_HEADER = (
    '<rect x="{x_pos}" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="{text_x_pos}" y="60" font-family="Arial" '
    'text-anchor="start" font-size="20">'
    'AB'
    '&#160;&#160;&#160;R'
    '&#160;&#160;&#160;H'
    '&#160;&#160;RBI'
    '&#160;BB'
    '&#160;SO'
    '&#160;LOB'
    '</text>'
    '<rect x="{x_pos}" y="2256" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="{text_x_pos}" y="2316" font-family="Arial" text-anchor="start" '
    'font-size="20">'
    'AB'
    '&#160;&#160;&#160;R'
    '&#160;&#160;&#160;H'
    '&#160;&#160;RBI'
    '&#160;BB'
    '&#160;SO'
    '&#160;LOB'
    '</text>'
)

BATTER_SVG_HEADER = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
)

BATTER_NAME_TEMPLATE = (
    '<a target="_parent" xlink:href="http://m.mlb.com/player/{batter_id}">'
    '<text x="10" y="{name_y_pos}" font-family="Arial" '
    'font-size="{batter_font_size}" '
    'text-anchor="start" fill="blue">{batter}</text></a>'
    '<text x="40" y="{stats_y_pos}" font-family="Arial" '
    'font-size="{stats_font_size}" '
    'text-anchor="start">{stats}</text>'
    '<text x="260" y="{name_y_pos}" font-family="Arial" '
    'font-size="{stats_font_size}" '
    'text-anchor="end">{appears}</text>'
)

SIGNATURE = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<a target="_parent" xlink:href="http://www.livebaseballscorecards.com">'
    '<image xlink:href="baseball-fairy-161.png" x="50" y="10" height="161" '
    'width="163" />'
    '<text x="133" y="190" font-family="Arial" font-size="20" '
    'text-anchor="middle" fill="blue">livebaseballscorecards.com</text></a>'
    '</svg>'
)

BOX_SCORE_LINE_TEMPLATE = (
    '<text x="13" y="{name_y_pos}" font-family="Arial" '
    'font-size="{batter_font_size}" text-anchor="start">{box_score_line}</text>'
)

BATTER_SUB_DIVISION_LINE = (
    '<line x1="{x_pos}" y1="{y_pos_1}" x2="{x_pos}" y2="{y_pos_2}" '
    'stroke="blue" stroke-width="5"/>'
)

PITCHER_SUB_DIVISION_LINE = (
    '<line x1="{x_pos_1}" y1="{y_pos}" x2="{x_pos_2}" y2="{y_pos}" '
    'stroke="blue" stroke-dasharray="15, 10" stroke-width="5"/>'
)

SVG_HEADER = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<line x1="67" y1="0" x2="67" y2="266" stroke="black" fill="transparent"/>'
    '<!-- Diamond -->'
    '<path d="M71 101 A 45 45, 0, 0, 1, 261 101 L 166 196 Z" stroke="black" '
    'fill="transparent"/>'
    '<path d="M112 142 L 166 89 L 220 142" stroke="black" fill="transparent"/>'
    '<!-- Pitch box and Strike zone -->'
    '<rect x="29" y="160" width="11" height="19" stroke="lightgray" '
    'fill="transparent"/>'
    '<path d="M13 266 L 13 143 L 55 143 L 55 266" stroke="black" '
    'fill="transparent"/>'
)

BIG_RECTANGLE = ('<path d="M0 {y_pos} L {width} {y_pos} '
                 'L {width} {y_pos_2} L 0 {y_pos_2}" '
                 'stroke="black" stroke-width="4" fill="none"/>')

FOOTER_BOX = (
    '<rect x="0" y="0" width="{width}" height="4513" fill="none" '
    'stroke="black" stroke-width="4"/>'
)

SVG_FOOTER = '</svg>'

SVG_PITCH_TEMPLATE = (
    '<text x="{pitch_text_x_1}" y="{pitch_text_y}" font-family="Arial" '
    'fill="{pitch_color}" font-size="13">{pitch_code}'
    '<title id="title">{title}</title></text>'
    '<text x="{pitch_text_x_2}" y="{pitch_text_y}" font-family="Arial" '
    'fill="{pitch_color}" font-size="13">{pitch_type} '
    '<title id="title">{title}</title></text>'
    '<text x="{pitch_text_x_3}" y="{pitch_text_y}" font-family="Arial" '
    'fill="{pitch_color}" font-size="13">'
    '{pitch_speed}<title id="title">{title}</title></text>'
    '<rect x="{pitch_location_x}" y="{pitch_location_y}" width="2" '
    'height="2" stroke="{pitch_color}" fill="{pitch_color}"/>'
)

SVG_PICKOFF_TEMPLATE = (
    '<text x="{pickoff_text_x_1}" y="{pickoff_text_y}" font-family="Arial" '
    'fill="{pickoff_color}" font-size="13">{pickoff_base}'
    '<title id="title">{title}</title></text>'
    '<text x="{pickoff_text_x_2}" y="{pickoff_text_y}" font-family="Arial" '
    'fill="{pickoff_color}" font-size="13">{pickoff_result} '
    '<title id="title">{title}</title></text>'
)

SVG_SUMMARY_TEMPLATE = (
    '<text x="260" y="192" font-family="Arial" font-size="34" '
    'text-anchor="end">{summary}'
    '<title id="title">{title}</title>'
    '</text>'
)

SVG_BASE_1 = (
    '<path d="M162 192 L 216 138" stroke="black" fill="transparent" '
    'stroke-width="11"/>'
)

SVG_BASE_2_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89" stroke="black" fill="transparent" '
    'stroke-width="11"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
)

SVG_BASE_2_OUT_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 194 117" stroke="black" fill="transparent" '
    'stroke-width="11"/>'
    '<path d="M184 124 L 201 107" stroke="black" fill="transparent" '
    'stroke-width="5"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
)

SVG_BASE_3_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89 L 111 142" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
)

SVG_BASE_3_OUT_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89 L 138 116" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<path d="M130 109 L 145 124" stroke="black" fill="transparent" '
    'stroke-width="5"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
)

SVG_BASE_4_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89 L 112 141" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<path d="M112 134 L 169 192" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<rect x="79" y="138" width="75" height="75" stroke="black" fill="black" '
    'transform = "rotate(-45 100 100)"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
    '<text x="164" y="133" font-family="Arial" text-anchor="middle" '
    'font-size="22" fill="white">{base_4_number}</text>'
    '<text x="164" y="158" font-family="Arial" text-anchor="middle" '
    'font-size="22" fill="white">{base_4_summary}'
    '<title id="title">{base_4_title}</title>'
    '</text>'
)

SVG_BASE_4_OUT_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89 L 111 142 L 137 167" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<path d="M128 174 L 143 158" stroke="black" fill="transparent" '
    'stroke-width="5"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
    '<text x="164" y="133" font-family="Arial" text-anchor="middle" '
    'font-size="22">{base_4_number}</text>'
    '<text x="164" y="158" font-family="Arial" text-anchor="middle" '
    'font-size="22">{base_4_summary}'
    '<title id="title">{base_4_title}</title>'
    '</text>'
)

SVG_OUT_TEMPLATE = (
    '<circle cx="255" cy="{y_val}" r="8" stroke="#c10000" stroke-width="1" '
    'fill="transparent" />'
    '<text x="251" y="{y_text}" fill="#c10000" font-family="Arial" '
    'font-size="15">{out_number}</text>'
)

SVG_FIELDING_TEMPLATE = (
    '<text x="165" y="68" font-family="Arial" font-size="43" '
    'text-anchor="middle">{summary}'
    '<title id="title">{title}</title>'
    '</text>'
)

SVG_SWINGING_STRIKEOUT_TEMPLATE = (
    '<text x="165" y="140" font-family="Arial" font-size="140" '
    'text-anchor="middle">K'
    '<title id="title">{title}</title>'
    '</text>'
)

SVG_CALLED_STRIKEOUT_TEMPLATE = (
    '<text x="155" y="140" font-family="Arial" font-size="140" '
    'text-anchor="middle" transform="translate(320 0) scale(-1 1)">K'
    '<title id="title">{title}</title>'
    '</text>'
)

SVG_COUNT_TEMPLATE = (
    '<text x="70" y="15" font-family="Arial" font-size="15">{count_str}'
    '</text>'
)

SVG_RUNNER_TEMPLATE = ('<text x="70" y="{y_val}" font-family="Arial" '
                       'stroke="{color}" font-size="16" '
                       'text-anchor="start">{summary}'
                       '<title id="title">{title}</title></text>')

SVG_HIT_BALL_TEMPLATE = (
    '<rect x="{hit_x}" y="{hit_y}" width="4" height="4" stroke="blue" '
    'fill="blue"/>'
)

SVG_HIT_LINE_TEMPLATE = (
    '<path d="M165 192 A 165 192 0 0 0 {hit_x} {hit_y}" stroke="blue" '
    'fill="none"/>'
)

SVG_HIT_GROUNDER_TEMPLATE = (
    '<path d="M165 192 L {hit_x} {hit_y}" stroke-dasharray="5, 5" '
    'stroke="blue" fill="none"/>'
)

SVG_HIT_FLY_TEMPLATE = (
    '<path d="M165 192 Q 20 20 {hit_x} {hit_y}" stroke="blue" '
    'fill="none"/>'
)
