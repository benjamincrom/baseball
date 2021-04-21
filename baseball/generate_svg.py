from collections import namedtuple

from pytz import timezone

from baseball.baseball_events import (AUTOMATIC_BALL_POSITION,
                                      Substitution,
                                      Pitch,
                                      Pickoff,
                                      RunnerAdvance)

FakePlateAppearance = namedtuple(
    'FakePlateAppearance',
    'scorecard_summary batter plate_appearance_description'
)

EASTERN_TIMEZONE_STR = 'America/New_York'
DEFAULT_LOGO = 'baseball-fairy-161.png'
LOGO_DICT = {
    'LAA': 'team_logos/angels.gif',
    'HOU': 'team_logos/astros.gif',
    'OAK': 'team_logos/athletics.gif',
    'TOR': 'team_logos/blue-jays.gif',
    'ATL': 'team_logos/braves.gif',
    'MIL': 'team_logos/brewers.gif',
    'ML4': 'team_logos/brewers.gif',
    'STL': 'team_logos/cardinals.gif',
    'CHC': 'team_logos/cubs.gif',
    'ARI': 'team_logos/diamondbacks.gif',
    'LAD': 'team_logos/dodgers.gif',
    'SF': 'team_logos/giants.gif',
    'CLE': 'team_logos/indians.gif',
    'SEA': 'team_logos/mariners.gif',
    'MIA': 'team_logos/marlins.gif',
    'FLO': 'team_logos/marlins.gif',
    'NYM': 'team_logos/mets.gif',
    'WSH': 'team_logos/nationals.gif',
    'BAL': 'team_logos/orioles.gif',
    'SD': 'team_logos/padres.gif',
    'PHI': 'team_logos/phillies.gif',
    'PIT': 'team_logos/pirates.gif',
    'TEX': 'team_logos/rangers.gif',
    'TB': 'team_logos/rays.gif',
    'CIN': 'team_logos/reds.gif',
    'BOS': 'team_logos/red-sox.gif',
    'COL': 'team_logos/rockies.gif',
    'KC': 'team_logos/royals.gif',
    'DET': 'team_logos/tigers.gif',
    'MIN': 'team_logos/twins.gif',
    'CWS': 'team_logos/white-sox.gif',
    'CHW': 'team_logos/white-sox.gif',
    'NYY': 'team_logos/yankees.gif'
}


HEIGHT = 4513
WIDTH = 3192
BOX_WIDTH = 266
BOX_HEIGHT = 200
EXTRA_COLUMNS = 3
NUM_MINIMUM_INNINGS = 9
LEN_BATTING_LIST = 9
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
PITCHER_MED_FONT_SIZE = 17
PITCHER_SMALL_FONT_SIZE = 13
PITCHER_STATS_LARGE_FONT_SIZE = 15
PITCHER_STATS_MED_FONT_SIZE = 13
PITCHER_STATS_SMALL_FONT_SIZE = 10
PITCHER_BOX_SCORE_LARGE_Y = 70
PITCHER_BOX_SCORE_MED_Y = 64
PITCHER_BOX_SCORE_SMALL_Y = 56
PITCHER_BOX_SCORE_X_INCREMENT = 70
PITCHER_BOX_SCORE_LARGE_Y_INCREMENT = 40
PITCHER_BOX_SCORE_MED_Y_INCREMENT = 34
PITCHER_BOX_SCORE_SMALL_Y_INCREMENT = 26
PITCHER_BOX_STATS_LARGE_Y_OFFSET = 73
PITCHER_BOX_STATS_MED_Y_OFFSET = 70
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
BASE_SVG_FONT_SMALL = 11
BASE_SVG_FONT_BIG = 22
FIRST_BASE_Y = 115
FIRST_BASE_X = 220
SECOND_BASE_Y = 80
SECOND_BASE_X = 186
THIRD_BASE_X = 112
SHORTSTOP_Y = 90
SHORTSTOP_X = 130
LEFT_FIELDER_Y = 58
LEFT_FIELDER_X = 105
CENTER_FIELDER_Y = 35
RIGHT_FIELDER_X = 225
BATTER_FONT_SIZE_BIG = 20
BATTER_FONT_SIZE_MED_PLUS = 18
BATTER_FONT_SIZE_MED = 15
BATTER_FONT_SIZE_SMALL = 10
BATTER_SPACE_BIG = 38
BATTER_SPACE_MED_PLUS = 32
BATTER_SPACE_MED = 22
BATTER_SPACE_SMALL = 15
BATTER_STATS_OFFSET_BIG = 15
BATTER_STATS_OFFSET_MED_PLUS = 13
BATTER_STATS_OFFSET_MED = 10
BATTER_STATS_OFFSET_SMALL = 6
BATTER_STATS_SPACES_BIG = 4
BATTER_STATS_SPACES_MED_PLUS = 5
BATTER_STATS_SPACES_MED = 6
BATTER_STATS_SPACES_SMALL = 10
BATTER_INITIAL_Y_POS = 25
BIG_TITLE_SIZE = 55
SMALL_TITLE_SIZE = 45
SUMMARY_SIZE_LARGE = 43
SUMMARY_SIZE_SMALL = 30
RED_COLOR = '#c10000'
BLUE_COLOR = 'blue'
DARK_GREEN_COLOR = 'darkgreen'
BLACK_COLOR = 'black'
HALF_SCALE_HEADER = '<g transform="scale(0.5)">'
HALF_SCALE_FOOTER = '</g>'
SVG_FOOTER = '</svg>'

PITCH_TYPE_DESCRIPTION = {'Ball': 'B',
                          'Ball In Dirt': 'D',
                          'Called Strike': 'C',
                          'Automatic Strike': 'C',
                          'Swinging Strike': 'S',
                          'Strike': 'S',
                          'Unknown Strike': 'S',
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
                          'In play, runs(s)': 'X',
                          'In play, out(s)': 'X',
                          'In play, no out': 'X'}

BIG_SVG_HEADER = (
    '<?xml version="1.0" standalone="no"?>'
    '<svg height="2256" viewBox="0 0 {width} 4513" '
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
    '<text x="80" y="700" transform="rotate(-90,80,700)" '
    'fill="black" font-size="{title_size}" font-family="Arial" text-anchor="middle" '
    '>{game_str}</text>'
    '<text x="145" y="700" transform="rotate(-90,145,700)" '
    'fill="black" font-size="45" font-family="Arial" text-anchor="middle" '
    '>{location}</text>'
    '<text x="200" y="700" transform="rotate(-90,200,700)" '
    'fill="black" font-size="30" font-family="Arial" text-anchor="middle" '
    '>{datetime}</text>'
    '<text x="235" y="700" transform="rotate(-90,235,700)" '
    'fill="black" font-size="30" font-family="Arial" text-anchor="middle" '
    '>{detail_str}</text>'
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

HOME_LOGO = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<image xlink:href="{logo}" x="50" y="0" height="200" '
    'width="163" />'
    '</svg>'
)

AWAY_LOGO = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<image xlink:href="{logo}" x="50" y="0" height="200" '
    'width="163" />'
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
    '<a target="_parent" xlink:href="http://www.livebaseballscorecards.com">'
    '<text x="{text_pos}" y="3545" font-family="Arial" font-size="20" '
    'text-anchor="right" fill="blue">livebaseballscorecards.com</text></a>'
    '<a target="_parent" xlink:href="http://www.livebaseballscorecards.com">'
    '<text x="{text_pos}" y="1290" font-family="Arial" font-size="20" '
    'text-anchor="right" fill="blue">livebaseballscorecards.com</text></a>'
)

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
    'font-size="{base_2_size}">{base_2_summary}'
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
    'font-size="{base_2_size}">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
)

SVG_BASE_3_TEMPLATE = (
    '<path d="M162 192 L 216 138 L 164 89 L 111 142" stroke="black" '
    'fill="transparent" stroke-width="11"/>'
    '<text x="199" y="93" font-family="Arial" text-anchor="start" '
    'font-size="22">{base_2_number}</text>'
    '<text x="199" y="114" font-family="Arial" text-anchor="start" '
    'font-size="{base_2_size}">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="{base_3_size}">{base_3_summary}'
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
    'font-size="{base_2_size}">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="{base_3_size}">{base_3_summary}'
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
    'font-size="{base_2_size}">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="{base_3_size}">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
    '<text x="164" y="133" font-family="Arial" text-anchor="middle" '
    'font-size="22" fill="white">{base_4_number}</text>'
    '<text x="164" y="158" font-family="Arial" text-anchor="middle" '
    'font-size="{base_4_size}" fill="white">{base_4_summary}'
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
    'font-size="{base_2_size}">{base_2_summary}'
    '<title id="title">{base_2_title}</title>'
    '</text>'
    '<text x="132" y="93" font-family="Arial" text-anchor="end" '
    'font-size="22">{base_3_number}</text>'
    '<text x="132" y="114" font-family="Arial" text-anchor="end" '
    'font-size="{base_3_size}">{base_3_summary}'
    '<title id="title">{base_3_title}</title>'
    '</text>'
    '<text x="164" y="133" font-family="Arial" text-anchor="middle" '
    'font-size="22">{base_4_number}</text>'
    '<text x="164" y="158" font-family="Arial" text-anchor="middle" '
    'font-size="{base_4_size}">{base_4_summary}'
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
    '<text x="165" y="68" font-family="Arial" font-size="{size}" '
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
                       'stroke="{color}" fill="{color}" font-size="16" '
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
    '<path d="M165 192 Q 20 20 {hit_x} {hit_y}" stroke="blue" fill="none"/>'
)


def get_game_width(game):
    inning_length = max(len(game.inning_list), NUM_MINIMUM_INNINGS)
    game_width = BOX_WIDTH * (inning_length + EXTRA_COLUMNS)

    return game_width

def get_big_svg_header(game):
    inning_length = max(len(game.inning_list), NUM_MINIMUM_INNINGS)
    game_width = get_game_width(game)

    big_svg_str = BIG_SVG_HEADER.format(width=game_width)

    for inning_num in range(1, inning_length + 1):
        x_pos = inning_num * BOX_WIDTH
        text_x_pos = x_pos + (BOX_WIDTH // 2)

        big_svg_str += BIG_SVG_COLUMN.format(inning_num=inning_num,
                                             x_pos=x_pos,
                                             text_x_pos=text_x_pos,
                                             width=game_width)

    box_score_header_x_pos = (inning_length + 1) * BOX_WIDTH
    box_score_header_text_x_pos = box_score_header_x_pos + 13

    big_svg_str += BOX_SCORE_COLUMN_HEADER.format(
        x_pos=box_score_header_x_pos,
        text_x_pos=box_score_header_text_x_pos,
    )

    return big_svg_str

def get_summary_svg(plate_appearance):
    batter_on_base = False

    for event in plate_appearance.event_list:
        batter_on_base = (
            isinstance(event, RunnerAdvance) and
            event.runner == plate_appearance.batter and
            event.end_base
        )

    if plate_appearance.got_on_base:
        return_str = SVG_SUMMARY_TEMPLATE.format(
            summary=plate_appearance.scorecard_summary,
            title=plate_appearance.plate_appearance_description
        )
    else:
        if (plate_appearance.scorecard_summary == 'K' and
                not batter_on_base):
            return_str = SVG_SWINGING_STRIKEOUT_TEMPLATE.format(
                title=plate_appearance.plate_appearance_description
            )
        elif (plate_appearance.scorecard_summary == 'ꓘ' and
              not batter_on_base):
            return_str = SVG_CALLED_STRIKEOUT_TEMPLATE.format(
                title=plate_appearance.plate_appearance_description
            )
        else:
            if len(plate_appearance.scorecard_summary) < 9:
                size = SUMMARY_SIZE_LARGE
            else:
                size = SUMMARY_SIZE_SMALL

            return_str = SVG_FIELDING_TEMPLATE.format(
                summary=plate_appearance.scorecard_summary.replace('ꓘ', 'K'),
                title=plate_appearance.plate_appearance_description,
                size=size
            )

    if plate_appearance.got_on_base and plate_appearance.error_str:
        if len(plate_appearance.scorecard_summary) < 9:
            size = SUMMARY_SIZE_LARGE
        else:
            size = SUMMARY_SIZE_SMALL

        return_str += SVG_FIELDING_TEMPLATE.format(
            summary=plate_appearance.error_str,
            title=plate_appearance.plate_appearance_description,
            size=size
        )

    return return_str

def get_pitch_color(event):
    if ('Strike' in event.pitch_description or
            'Foul' in event.pitch_description):
        color = RED_COLOR
    elif 'In play' in event.pitch_description:
        color = BLUE_COLOR
    else:
        color = BLACK_COLOR

    return color

def process_pitch_position(event):
    if event.pitch_position == AUTOMATIC_BALL_POSITION:
        x_coord, y_coord = AUTOMATIC_BALL_COORDINATE
    else:
        x_scale_factor = event.pitch_position[0] / PITCH_MAX_COORD
        x_coord = int(
            PITCH_X_MAX - (PITCH_BOX_WIDTH * x_scale_factor)
        )

        y_scale_factor = event.pitch_position[1] / PITCH_MAX_COORD
        y_coord = int(PITCH_Y_MIN + (PITCH_BOX_HEIGHT * y_scale_factor))

    return x_coord, y_coord

def process_pitch(x_val, y_val, event, pitch_svg):
    color = get_pitch_color(event)
    description = event.pitch_description.split(' (')[0]
    code = PITCH_TYPE_DESCRIPTION[description]

    pitch_type = event.pitch_type or ''
    x_coord, y_coord = process_pitch_position(event)

    if event.pitch_speed:
        speed = int(round(event.pitch_speed))
    else:
        speed = ''

    pitch_svg += SVG_PITCH_TEMPLATE.format(
        pitch_text_x_1=x_val,
        pitch_text_x_2=x_val + PITCH_TYPE_X_OFFSET,
        pitch_text_x_3=x_val + PITCH_SPEED_X_OFFSET,
        pitch_text_y=y_val,
        pitch_color=color,
        pitch_code=code,
        pitch_type=pitch_type,
        pitch_speed=speed,
        pitch_location_x=x_coord,
        pitch_location_y=y_coord,
        title=event.pitch_description
    )

    return pitch_svg

def process_pickoff(x_val, y_val, event, pitch_svg):
    pickoff_base = event.pickoff_base[0]

    if event.pickoff_was_successful:
        color = RED_COLOR
        pickoff_result = 'OUT'
    else:
        color = BLACK_COLOR
        pickoff_result = 'SAFE'

    pitch_svg += SVG_PICKOFF_TEMPLATE.format(
        pickoff_text_x_1=x_val,
        pickoff_text_x_2=x_val + PITCH_TYPE_X_OFFSET,
        pickoff_text_y=y_val,
        pickoff_color=color,
        pickoff_base=pickoff_base,
        pickoff_result=pickoff_result,
        title=event.pickoff_description
    )

    return pitch_svg

def get_pitch_svg(plate_appearance):
    pitch_svg = ''
    x_val = FIRST_PITCH_X_VAL
    y_val = FIRST_PITCH_Y_VAL

    for event in plate_appearance.event_list:
        if y_val > PITCH_Y_LIMIT:
            y_val = PITCH_ROW_2_Y_VAL
            x_val += PITCH_X_OFFSET

        if isinstance(event, Pitch):
            pitch_svg = process_pitch(x_val, y_val, event, pitch_svg)
            y_val += PITCH_Y_OFFSET
        elif isinstance(event, Pickoff):
            pitch_svg += process_pickoff(x_val, y_val, event, pitch_svg)
            y_val += PITCH_Y_OFFSET

    return pitch_svg

def get_runner_title_str(event):
    title_flag_str = ''
    if event.runner_scored:
        title_flag_list = []
        if event.run_earned:
            title_flag_list.append('Earned')

        if event.is_rbi:
            title_flag_list.append('RBI')

        if title_flag_list:
            title_flag_str = ' ({})'.format(', '.join(title_flag_list))
        else:
            title_flag_str = ''

    return title_flag_str

def get_runner_color(event):
    if not event.end_base and not event.runner_scored:
        color = RED_COLOR
    elif event.runner_scored:
        color = DARK_GREEN_COLOR
    else:
        color = BLACK_COLOR

    return color

def get_runner_end_base_str(plate_appearance, event):
    if event.end_base:
        this_end_base_str = event.end_base[0]
        if this_end_base_str == 's':
            this_end_base_str = 'H'
    elif event.runner_scored:
        this_end_base_str = 'H'
    else:
        this_end_base_str = ''
        for out_runner, out_base in plate_appearance.out_runners_list:
            if out_runner == event.runner:
                this_end_base_str = out_base[0]
                if this_end_base_str in ['h', 's']:
                    this_end_base_str = 'H'

    return this_end_base_str

def get_player_last_name(player_obj):
    return player_obj.last_name

def get_runners_svg(plate_appearance):
    runner_svg_str = ''
    all_runners_list = list(
        set([event.runner for event in plate_appearance.event_list
             if (isinstance(event, RunnerAdvance) and
                 event.runner != plate_appearance.batter)])
    )

    all_runners_list.sort(key=get_player_last_name)

    y_val_list = []
    for runner in all_runners_list:
        start_base_num = 1000
        color = None
        end_base = 0
        this_end_base = ''
        runner_event = None
        for event in plate_appearance.event_list:
            if (isinstance(event, RunnerAdvance) and
                    event.start_base and
                    runner == event.runner):
                runner_event = event
                color = get_runner_color(event)
                if int(event.start_base[0]) < start_base_num:
                    start_base_num = int(event.start_base[0])

                this_end_base = get_runner_end_base_str(plate_appearance, event)
                if this_end_base == 'H':
                    end_base = this_end_base

                if end_base == 'H':
                    break

                if this_end_base and int(this_end_base) > end_base:
                    end_base = int(this_end_base)

        if color:
            summary = '{}-{}'.format(start_base_num, this_end_base)
            is_forceout_desc = (
                'Forceout' in runner_event.run_description or
                (
                    ('Double Play' in runner_event.run_description or
                     'Triple Play' in runner_event.run_description or
                     'DP' in runner_event.run_description or
                     'TP' in runner_event.run_description)
                    and
                    ('F' not in plate_appearance.scorecard_summary and
                     'L' not in plate_appearance.scorecard_summary)
                )
            )

            if (is_forceout_desc and runner_event.end_base == ''
                    and this_end_base and not runner_event.runner_scored):
                summary += 'f'

            title_flag_str = get_runner_title_str(runner_event)

            title = '{}: {}{}'.format(
                str(runner_event.runner),
                runner_event.run_description,
                title_flag_str
            )

            y_val = RUNNER_SUMMARY_Y_VAL
            if start_base_num == 2:
                y_val += RUNNER_SUMMARY_Y_OFFSET
            elif start_base_num == 3:
                y_val += (RUNNER_SUMMARY_Y_OFFSET * 2)

            while y_val in y_val_list:
                y_val -= RUNNER_SUMMARY_Y_OFFSET

            y_val_list.append(y_val)
            runner_svg_str += SVG_RUNNER_TEMPLATE.format(
                y_val=y_val,
                color=color,
                summary=summary,
                title=title
            )

    return runner_svg_str

def get_outs_svg(plate_appearance, prev_plate_appearance):
    outs_svg = ''
    outs_list = []

    if not prev_plate_appearance:
        outs_before = 0
    else:
        outs_before = prev_plate_appearance.inning_outs

    outs_this_pa = plate_appearance.inning_outs - outs_before
    if outs_this_pa > 0:
        outs_list = range(outs_before + 1, plate_appearance.inning_outs + 1)

    y_val = OUT_CIRCLE_Y_VAL
    for out in outs_list:
        outs_svg += SVG_OUT_TEMPLATE.format(
            y_val=y_val,
            y_text=y_val + OUT_TEXT_Y_OFFSET,
            out_number=out
        )

        y_val += OUT_CIRCLE_Y_OFFSET

    return outs_svg

def get_components(plate_appearance):
    number = plate_appearance.batter.number

    if plate_appearance.scorecard_summary:
        summary = plate_appearance.scorecard_summary.split()[0]
    else:
        summary = None

    title = plate_appearance.plate_appearance_description

    return number, summary, title

def get_all_base_components(base_2_pa, base_3_pa, home_pa):
    if base_2_pa:
        base_2_number, base_2_summary, base_2_title = get_components(base_2_pa)
    else:
        base_2_number, base_2_summary, base_2_title = '', '', ''

    if base_3_pa:
        base_3_number, base_3_summary, base_3_title = get_components(base_3_pa)
    else:
        base_3_number, base_3_summary, base_3_title = '', '', ''

    if home_pa:
        base_4_number, base_4_summary, base_4_title = get_components(home_pa)
    else:
        base_4_number, base_4_summary, base_4_title = '', '', ''

    return (base_2_number,
            base_2_summary,
            base_2_title,
            base_3_number,
            base_3_summary,
            base_3_title,
            base_4_number,
            base_4_summary,
            base_4_title)

def get_base_font_size(base_2_summary, base_3_summary, base_4_summary):
    if base_2_summary and len(base_2_summary) > 6:
        base_2_size = BASE_SVG_FONT_SMALL
    else:
        base_2_size = BASE_SVG_FONT_BIG

    if base_3_summary and len(base_3_summary) > 6:
        base_3_size = BASE_SVG_FONT_SMALL
    else:
        base_3_size = BASE_SVG_FONT_BIG

    if base_4_summary and len(base_4_summary) > 6:
        base_4_size = BASE_SVG_FONT_SMALL
    else:
        base_4_size = BASE_SVG_FONT_BIG

    return base_2_size, base_3_size, base_4_size

def process_base_appearances(base_2_pa, base_3_pa, home_pa, batter_final_base,
                             batter_out_base):
    (base_2_number,
     base_2_summary,
     base_2_title,
     base_3_number,
     base_3_summary,
     base_3_title,
     base_4_number,
     base_4_summary,
     base_4_title) = get_all_base_components(base_2_pa, base_3_pa, home_pa)

    base_2_size, base_3_size, base_4_size = get_base_font_size(base_2_summary,
                                                               base_3_summary,
                                                               base_4_summary)

    if batter_out_base:
        if batter_out_base == '1B':
            base_svg = ''
        elif batter_out_base == '2B':

            base_svg = SVG_BASE_2_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_2_size=base_2_size
            )
        elif batter_out_base == '3B':
            base_svg = SVG_BASE_3_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_2_size=base_2_size,
                base_3_size=base_3_size
            )
        elif batter_out_base == 'H':
            base_svg = SVG_BASE_4_OUT_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_4_number=base_4_number,
                base_4_summary=base_4_summary,
                base_4_title=base_4_title,
                base_2_size=base_2_size,
                base_3_size=base_3_size,
                base_4_size=base_4_size
            )
        else:
            raise ValueError('Invalid Base')
    elif batter_final_base:
        if batter_final_base == '1B':
            base_svg = SVG_BASE_1
        elif batter_final_base == '2B':
            base_svg = SVG_BASE_2_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_2_size=base_2_size
            )
        elif batter_final_base == '3B':
            base_svg = SVG_BASE_3_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_2_size=base_2_size,
                base_3_size=base_3_size
            )
        elif batter_final_base == 'H':
            base_svg = SVG_BASE_4_TEMPLATE.format(
                base_2_number=base_2_number,
                base_2_summary=base_2_summary,
                base_2_title=base_2_title,
                base_3_number=base_3_number,
                base_3_summary=base_3_summary,
                base_3_title=base_3_title,
                base_4_number=base_4_number,
                base_4_summary=base_4_summary,
                base_4_title=base_4_title,
                base_2_size=base_2_size,
                base_3_size=base_3_size,
                base_4_size=base_4_size
            )
        else:
            raise ValueError('Invalid Base')
    else:
        base_svg = ''

    return base_svg

def player_got_on_base(plate_appearance):
    got_on_base = False
    for event in plate_appearance.event_list:
        if (isinstance(event, RunnerAdvance) and
                event.runner == plate_appearance.batter and
                event.end_base):
            got_on_base = True

    return got_on_base

def fix_pa(plate_appearance, event):
    summary = None
    description = None

    if 'Stolen' in event.run_description:
        summary = 'S'
        description = '{} batting: Stolen Base'.format(plate_appearance.batter)
    elif 'Caught Stealing' in event.run_description:
        summary = 'CS'
        description = '{} batting: Caught Stealing'.format(
            plate_appearance.batter
        )
    elif 'Passed Ball' in event.run_description:
        summary = 'PB'
        description = '{} batting: Passed Ball'.format(plate_appearance.batter)
    elif 'Wild Pitch' in event.run_description:
        summary = 'WP'
        description = '{} batting: Wild Pitch'.format(plate_appearance.batter)
    elif 'Balk' in event.run_description:
        summary = 'BLK'
        description = '{} batting: Balk'.format(plate_appearance.batter)
    elif 'Defensive Indiff' in event.run_description:
        summary = 'DI'
        description = '{} batting: Defensive Indifference'.format(
            plate_appearance.batter
        )
    elif 'Error' in event.run_description:
        summary = 'E'
        description = '{} batting: {}'.format(
            plate_appearance.batter,
            event.run_description
        )

    if summary and description:
        return_pa = FakePlateAppearance(summary,
                                        plate_appearance.batter,
                                        description)
    else:
        return_pa = plate_appearance

    return return_pa

def get_base_svg(plate_appearance, plate_appearance_list):
    plate_appearance_index = plate_appearance_list.index(plate_appearance)
    plate_appearance_list = (
        plate_appearance_list[plate_appearance_index:plate_appearance_index+8]
    )

    second_base_pa = third_base_pa = home_plate_pa = None
    batter_final_base = batter_out_base = batter_is_done = None

    batter = plate_appearance.batter
    for this_pa in plate_appearance_list:
        for event in this_pa.event_list:
            if (isinstance(event, RunnerAdvance) and
                    event.runner == batter):
                if not event.end_base:
                    batter_is_done = True

                for out_runner, out_base in this_pa.out_runners_list:
                    if out_base == '1st' and event.start_base == '1B':
                        out_base = '2nd'
                    if out_base == '2nd' and event.start_base == '2B':
                        out_base = '3rd'
                    if out_base == '3rd' and event.start_base == '3B':
                        out_base = 'home'

                    if out_runner == batter:
                        if out_base == '1st':
                            batter_out_base = '1B'
                        elif out_base == '2nd':
                            batter_out_base = '2B'
                            if plate_appearance != this_pa:
                                second_base_pa = fix_pa(this_pa, event)
                        elif out_base == '3rd':
                            batter_out_base = '3B'
                            if plate_appearance != this_pa:
                                third_base_pa = fix_pa(this_pa, event)
                        elif out_base == 'home':
                            batter_out_base = 'H'
                            if plate_appearance != this_pa:
                                home_plate_pa = fix_pa(this_pa, event)

                if (event.end_base == '1B' and
                        batter_final_base not in ['2B', '3B', 'H']):
                    batter_final_base = '1B'
                elif (event.end_base == '2B' and
                      batter_final_base not in ['3B', 'H']):
                    batter_final_base = '2B'
                    if plate_appearance != this_pa:
                        second_base_pa = fix_pa(this_pa, event)
                elif event.end_base == '3B' and batter_final_base not in ['H']:
                    batter_final_base = '3B'
                    if plate_appearance != this_pa:
                        third_base_pa = fix_pa(this_pa, event)
                elif event.runner_scored:
                    batter_final_base = 'H'
                    if plate_appearance != this_pa:
                        home_plate_pa = fix_pa(this_pa, event)
            elif isinstance(event, Substitution):
                if event.outgoing_player == batter and event.position == 'PR':
                    batter = event.incoming_player

        if batter_is_done:
            break

    if third_base_pa and second_base_pa == third_base_pa:
        second_base_pa = None

    if home_plate_pa and third_base_pa == home_plate_pa:
        third_base_pa = None

    base_svg = process_base_appearances(second_base_pa,
                                        third_base_pa,
                                        home_plate_pa,
                                        batter_final_base,
                                        batter_out_base)

    return base_svg

def get_hit_svg(plate_appearance):
    hit_svg = ''
    hit_location = plate_appearance.hit_location
    if hit_location:
        if hit_location[0] == 'S':
            hit_location = hit_location[1:]

        if len(hit_location) == 2:
            hit_type = hit_location[0]
            hit_position_num = int(hit_location[1])

            is_valid_hit_type = False
            if hit_type in ['B', 'G']:
                template = SVG_HIT_GROUNDER_TEMPLATE
                is_valid_hit_type = True
            elif hit_type in ['L', 'E']:
                template = SVG_HIT_LINE_TEMPLATE
                is_valid_hit_type = True
            elif hit_type in ['P', 'F']:
                template = SVG_HIT_FLY_TEMPLATE
                is_valid_hit_type = True

            if is_valid_hit_type:
                if hit_position_num == 1:
                    hit_svg = template.format(hit_x=PITCHER_X,
                                              hit_y=PITCHER_Y)
                elif hit_position_num == 2:
                    hit_svg = template.format(hit_x=PITCHER_X,
                                              hit_y=CATCHER_Y)
                elif hit_position_num == 3:
                    hit_svg = template.format(hit_x=FIRST_BASE_X,
                                              hit_y=FIRST_BASE_Y)
                elif hit_position_num == 4:
                    hit_svg = template.format(hit_x=SECOND_BASE_X,
                                              hit_y=SECOND_BASE_Y)
                elif hit_position_num == 5:
                    hit_svg = template.format(hit_x=THIRD_BASE_X,
                                              hit_y=FIRST_BASE_Y)
                elif hit_position_num == 6:
                    hit_svg = template.format(hit_x=SHORTSTOP_X,
                                              hit_y=SHORTSTOP_Y)
                elif hit_position_num == 7:
                    hit_svg = template.format(hit_x=LEFT_FIELDER_X,
                                              hit_y=LEFT_FIELDER_Y)
                elif hit_position_num == 8:
                    hit_svg = template.format(hit_x=PITCHER_X,
                                              hit_y=CENTER_FIELDER_Y)
                elif hit_position_num == 9:
                    hit_svg = template.format(hit_x=RIGHT_FIELDER_X,
                                              hit_y=LEFT_FIELDER_Y)

    return hit_svg

def get_count_svg(plate_appearance):
    balls = 0
    strikes = 0
    for event in plate_appearance.event_list:
        if (isinstance(event, Pitch) and
                'In play' not in event.pitch_description):
            if ('Strike' in event.pitch_description or
                    'Missed Bunt' in event.pitch_description or
                    'Foul Bunt' in event.pitch_description):
                strikes += 1
            elif 'Foul' in event.pitch_description and strikes < 2:
                strikes += 1
            elif 'Foul' not in event.pitch_description:
                balls += 1

    count_str = '{}-{}'.format(balls, strikes)
    count_svg = SVG_COUNT_TEMPLATE.format(count_str=count_str)

    return count_svg

def get_inning_half_stats_tuple_list(game):
    inning_half_stats_tuple_list = []
    for inning_index, inning in enumerate(game.inning_list):
        inning_half_stats_tuple_list.extend(
            [(inning_index + 1, 'top', inning.top_half_inning_stats),
             (inning_index + 1, 'bottom', inning.bottom_half_inning_stats)]
        )

    return inning_half_stats_tuple_list

def get_svg_content_list(game):
    content_list = []
    for inning_index, inning in enumerate(game.inning_list):
        tuple_list = [(inning.top_half_appearance_list, 'top'),
                      (inning.bottom_half_appearance_list, 'bottom')]

        for plate_appearance_list, inning_half_str in tuple_list:
            if plate_appearance_list:
                prev_plate_appearance = None
                for plate_appearance_tuple in enumerate(plate_appearance_list):
                    pa_index, plate_appearance = plate_appearance_tuple

                    plate_appearance_svg = '{}{}{}{}{}{}'.format(
                        get_summary_svg(plate_appearance),
                        get_pitch_svg(plate_appearance),
                        get_runners_svg(plate_appearance),
                        get_count_svg(plate_appearance),
                        get_hit_svg(plate_appearance),
                        get_outs_svg(plate_appearance, prev_plate_appearance)
                    )

                    if player_got_on_base(plate_appearance):
                        plate_appearance_svg += get_base_svg(
                            plate_appearance,
                            plate_appearance_list
                        )

                    id_tuple = (inning_index + 1, inning_half_str, pa_index + 1)
                    content_list.append(
                        (id_tuple,
                         plate_appearance_svg,
                         plate_appearance.plate_appearance_summary)
                    )

                    prev_plate_appearance = plate_appearance

    return content_list

def get_batter_spacing_values(batter_list):
    if len(batter_list) <= 5:
        batter_font_size = BATTER_FONT_SIZE_BIG
        batter_space_increment = BATTER_SPACE_BIG
        stats_y_offset = BATTER_STATS_OFFSET_BIG
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_BIG // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_BIG + '%s') * 6
        )
    elif len(batter_list) > 5 and len(batter_list) < 9:
        batter_font_size = BATTER_FONT_SIZE_MED
        batter_space_increment = BATTER_SPACE_MED
        stats_y_offset = BATTER_STATS_OFFSET_MED
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_MED // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_MED + '%s') * 6
        )
    else:
        batter_font_size = BATTER_FONT_SIZE_SMALL
        batter_space_increment = BATTER_SPACE_SMALL
        stats_y_offset = BATTER_STATS_OFFSET_SMALL
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_SMALL // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_SMALL + '%s') * 6
        )

    for batter in batter_list:
        if (len(str(batter.player_obj)) > 18 and
                batter_font_size == BATTER_FONT_SIZE_BIG):
            batter_font_size = BATTER_FONT_SIZE_MED_PLUS
            batter_space_increment = BATTER_SPACE_MED_PLUS
            stats_y_offset = BATTER_STATS_OFFSET_MED_PLUS
            box_score_line_template = (
                ('&#160;' * (BATTER_STATS_SPACES_MED_PLUS // 2)) + '%s' +
                ('&#160;' * BATTER_STATS_SPACES_MED_PLUS + '%s') * 6
            )

    return (batter_font_size,
            batter_space_increment,
            stats_y_offset,
            box_score_line_template)

def get_team_batter_box_score_list(game, team, box_score_dict, offset):
    box_score_svg = ''
    num_innings = max(len(game.inning_list), NUM_MINIMUM_INNINGS)
    box_score_x_offset = BOX_WIDTH * (num_innings + 1)

    for batter_list in team.batting_order_list_list:
        box_score_svg += BATTER_SVG_HEADER.format(
            x_pos=box_score_x_offset,
            y_pos=offset + (BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, _, box_score_line_template = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:
            if last_batter == batter_appearance.player_obj:
                box_score_line_str = ''
            else:
                box_score_line_str = (
                    box_score_line_template %
                    box_score_dict[batter_appearance.player_obj]
                )

            box_score_svg += BOX_SCORE_LINE_TEMPLATE.format(
                name_y_pos=batter_y_pos,
                box_score_line=box_score_line_str,
                batter_font_size=batter_font_size
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        box_score_svg += SVG_FOOTER
        offset += BOX_HEIGHT

    return box_score_svg

def get_team_batter_list(team, offset):
    batter_svg = ''
    for batter_list in team.batting_order_list_list:
        batter_svg += BATTER_SVG_HEADER.format(
            x_pos=0,
            y_pos=offset + (BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, stats_y_offset, _ = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:
            if last_batter == batter_appearance.player_obj:
                batter_str = ''
                stats_str = ''
            else:
                batter_str = '{}'.format(batter_appearance.player_obj)
                if batter_appearance.player_obj.bat_side:
                    batter_str += ', {}'.format(
                        batter_appearance.player_obj.bat_side
                    )

                if (batter_appearance.player_obj.obp and
                        batter_appearance.player_obj.slg):
                    stats_str = 'OBP: {:.3f}, SLG: {:.3f}'.format(
                        batter_appearance.player_obj.obp,
                        batter_appearance.player_obj.slg
                    )
                else:
                    stats_str = ''

            appears_str = '({}, {})'.format(batter_appearance.start_inning_num,
                                            batter_appearance.position)

            batter_svg += BATTER_NAME_TEMPLATE.format(
                batter_id=batter_appearance.player_obj.mlb_id,
                name_y_pos=batter_y_pos,
                stats_y_pos=batter_y_pos + stats_y_offset,
                stats=stats_str,
                appears=appears_str,
                batter=batter_str,
                batter_font_size=batter_font_size,
                stats_font_size=batter_font_size - 5
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        batter_svg += SVG_FOOTER
        offset += BOX_HEIGHT

    return batter_svg

def get_batter_list_and_stats(game):
    both_teams_batters_svg = ''

    tuple_list = [
        (game.away_team, game.away_batter_box_score_dict, 0),
        (game.home_team, game.home_batter_box_score_dict, HEIGHT // 2)
    ]

    for team, box_score_dict, offset in tuple_list:
        both_teams_batters_svg += '{}{}'.format(
            get_team_batter_list(team, offset),
            get_team_batter_box_score_list(game, team, box_score_dict, offset)
        )

    return both_teams_batters_svg

def get_team_stats_box(box_x, box_y, stats_tuple):
    box_1_x = box_x
    stats_box_1_svg = INNING_STATS_BOX.format(
        box_x=box_1_x,
        box_y=box_y,
        stats_str_1='1B: &#160;{}'.format(stats_tuple.B1),
        stats_str_2='2B: &#160;{}'.format(stats_tuple.B2),
        stats_str_3='3B: &#160;{}'.format(stats_tuple.B3),
        stats_str_4='HR: {}'.format(stats_tuple.HR),
        stats_str_5='SF:',
        stats_str_6='SAC:',
        stats_str_7='DP:',
        stats_str_8='HBP:',
        stats_str_9='{}'.format(stats_tuple.SF),
        stats_str_10='{}'.format(stats_tuple.SAC),
        stats_str_11='{}'.format(stats_tuple.DP),
        stats_str_12='{}'.format(stats_tuple.HBP)
    )

    box_2_x = box_x + BOX_WIDTH
    stats_box_2_svg = INNING_STATS_BOX.format(
        box_x=box_2_x,
        box_y=box_y,
        stats_str_1='WP: {}'.format(stats_tuple.WP),
        stats_str_2='PB: &#160;{}'.format(stats_tuple.PB),
        stats_str_3='SB: &#160;{}'.format(stats_tuple.SB),
        stats_str_4='CS: &#160;{}'.format(stats_tuple.CS),
        stats_str_5='PA:',
        stats_str_6='',
        stats_str_7='',
        stats_str_8='',
        stats_str_9='{}'.format(stats_tuple.PA),
        stats_str_10='',
        stats_str_11='',
        stats_str_12=''
    )

    both_stats_boxes_svg = stats_box_1_svg + stats_box_2_svg

    return both_stats_boxes_svg

def get_inning_stats_box(box_x, box_y, stats_tuple):
    stats_box_svg = (
        INNING_STATS_BOX.format(
            box_x=box_x,
            box_y=box_y,
            stats_str_1='R: {}'.format(stats_tuple.R),
            stats_str_2='E: {}'.format(stats_tuple.E),
            stats_str_3='K: {}'.format(stats_tuple.K),
            stats_str_4='S: {}'.format(stats_tuple.S),
            stats_str_5='H:',
            stats_str_6='LOB:',
            stats_str_7='BB:',
            stats_str_8='P:',
            stats_str_9='{}'.format(stats_tuple.H),
            stats_str_10='{}'.format(stats_tuple.LOB),
            stats_str_11='{}'.format(stats_tuple.BB),
            stats_str_12='{}'.format(stats_tuple.P)
        )
    )

    return stats_box_svg

def get_this_pa_num(player_appearance, appearance_list):
    this_pa_num = None
    if appearance_list:
        for pa_index, plate_app in enumerate(appearance_list):
            if plate_app.batter == player_appearance.player_obj:
                this_pa_num = pa_index + 1

    return this_pa_num

def add_away_batter_sub_division_lines(game):
    sub_divisions_svg = ''
    for batter_appearance_list in game.away_team.batting_order_list_list:
        batting_pos_index = game.away_team.batting_order_list_list.index(
            batter_appearance_list
        )

        last_batter = None
        for batter_app in batter_appearance_list:
            same_last_batter = last_batter == batter_app.player_obj
            if not same_last_batter:
                x_pos = BOX_WIDTH * batter_app.start_inning_num
                y_pos = ((BOX_HEIGHT * batting_pos_index) +
                         (BOX_HEIGHT // 2))

                for inning_index, inning in enumerate(game.inning_list):
                    if batter_app.start_inning_num == inning_index + 1:
                        inning_pa_num = get_this_pa_num(
                            batter_app,
                            inning.top_half_appearance_list
                        )

                        if (not inning_pa_num or
                                batter_app.start_inning_batter_num > inning_pa_num
                                or batter_app.start_inning_half == 'bottom'):
                            x_pos += BOX_WIDTH

                if not (batter_app.start_inning_num == 1 and
                        batter_app.start_inning_batter_num == 1 and
                        batter_app.start_inning_half == 'top'):
                    sub_divisions_svg += (
                        BATTER_SUB_DIVISION_LINE.format(
                            x_pos=x_pos,
                            y_pos_1=y_pos,
                            y_pos_2=y_pos + BOX_HEIGHT
                        )
                    )

            last_batter = batter_app.player_obj

    return sub_divisions_svg

def add_home_batter_sub_division_lines(game):
    sub_divisions_svg = ''
    for batter_appearance_list in game.home_team.batting_order_list_list:
        batting_pos_index = game.home_team.batting_order_list_list.index(
            batter_appearance_list
        )
        last_batter = None
        for batter_app in batter_appearance_list:
            same_last_batter = last_batter == batter_app.player_obj

            if not same_last_batter:
                x_pos = BOX_WIDTH * batter_app.start_inning_num
                y_pos = ((BOX_HEIGHT * batting_pos_index) +
                         (HEIGHT // 2 + BOX_HEIGHT // 2))

                for inning_index, inning in enumerate(game.inning_list):
                    if batter_app.start_inning_num == inning_index + 1:
                        inning_pa_num = get_this_pa_num(
                            batter_app,
                            inning.bottom_half_appearance_list
                        )

                        if ((not inning_pa_num or
                             batter_app.start_inning_batter_num > inning_pa_num)
                                and batter_app.start_inning_half == 'bottom'):
                            x_pos += BOX_WIDTH

                if not (batter_app.start_inning_num == 1 and
                        batter_app.start_inning_batter_num == 1 and
                        batter_app.start_inning_half == 'top'):
                    sub_divisions_svg += (
                        BATTER_SUB_DIVISION_LINE.format(
                            x_pos=x_pos,
                            y_pos_1=y_pos,
                            y_pos_2=y_pos + BOX_HEIGHT
                        )
                    )

            last_batter = batter_app.player_obj

    return sub_divisions_svg

def add_away_pitcher_sub_division_lines(game):
    sub_divisions_svg = ''

    for pitcher_app in game.away_team.pitcher_list:
        if pitcher_app.end_inning_num:
            total_pa_num = 0

            for inning_index, inning in enumerate(game.inning_list):
                inning_num = inning_index + 1
                inning_pa_num = 1

                if not inning.bottom_half_appearance_list:
                    continue

                num_appearances = len(inning.bottom_half_appearance_list)
                mod_num = num_appearances % LEN_BATTING_LIST
                for appearance in inning.bottom_half_appearance_list:
                    if (inning_num == pitcher_app.end_inning_num and
                            (inning_pa_num == pitcher_app.end_inning_batter_num
                             or pitcher_app.end_inning_half == 'top')):

                        x_pos = BOX_WIDTH * pitcher_app.end_inning_num
                        x_pos_2 = x_pos + BOX_WIDTH
                        y_pos = (
                            (BOX_HEIGHT * (total_pa_num % LEN_BATTING_LIST)) +
                            (HEIGHT // 2 + BOX_HEIGHT // 2)
                        )

                        if ((LEN_BATTING_LIST * 2) >= num_appearances >
                                LEN_BATTING_LIST):
                            if inning_pa_num <= mod_num:
                                x_pos_2 -= (BOX_WIDTH // 2)
                            elif inning_pa_num > LEN_BATTING_LIST:
                                x_pos += (BOX_WIDTH // 2)
                                y_pos += (BOX_HEIGHT // 2)
                        elif num_appearances > (LEN_BATTING_LIST * 2):
                            if inning_pa_num <= mod_num:
                                x_pos_2 -= (BOX_WIDTH // 2)
                            elif inning_pa_num > LEN_BATTING_LIST:
                                x_pos += (BOX_WIDTH // 2)
                            elif inning_pa_num > (LEN_BATTING_LIST * 2):
                                x_pos_2 -= (BOX_WIDTH // 2)
                                y_pos += (BOX_HEIGHT // 2)
                            elif inning_pa_num > (LEN_BATTING_LIST * 3):
                                x_pos += (BOX_WIDTH // 2)
                                y_pos += (BOX_HEIGHT // 2)

                        sub_divisions_svg += (
                            PITCHER_SUB_DIVISION_LINE.format(x_pos_1=x_pos,
                                                             x_pos_2=x_pos_2,
                                                             y_pos=y_pos)
                        )

                    if appearance.plate_appearance_summary != 'Runner Out':
                        inning_pa_num += 1
                        total_pa_num += 1

    return sub_divisions_svg

def add_home_pitcher_sub_division_lines(game):
    sub_divisions_svg = ''

    for pitcher_app in game.home_team.pitcher_list:
        if pitcher_app.end_inning_num:
            total_pa_num = 0

            for inning_index, inning in enumerate(game.inning_list):
                inning_num = inning_index + 1
                inning_pa_num = 1
                last_batter_no_pa = False

                for appearance in inning.top_half_appearance_list:
                    if (inning_num == pitcher_app.end_inning_num and
                            inning_pa_num == pitcher_app.end_inning_batter_num
                            and pitcher_app.end_inning_half != 'bottom'):

                        x_pos = BOX_WIDTH * pitcher_app.end_inning_num
                        y_pos = ((BOX_HEIGHT *
                                  (total_pa_num % LEN_BATTING_LIST)) +
                                 (BOX_HEIGHT // 2))

                        sub_divisions_svg += (
                            PITCHER_SUB_DIVISION_LINE.format(
                                x_pos_1=x_pos,
                                x_pos_2=x_pos + BOX_WIDTH,
                                y_pos=y_pos
                            )
                        )

                    if appearance.plate_appearance_summary == 'Runner Out':
                        last_batter_no_pa = True
                    else:
                        total_pa_num += 1
                        inning_pa_num += 1

                if (inning_num == pitcher_app.end_inning_num and
                        pitcher_app.end_inning_half == 'bottom'):
                    sub_divisions_svg += add_end_inning_pitcher_sub(
                        pitcher_app,
                        total_pa_num,
                        last_batter_no_pa
                    )

    return sub_divisions_svg

def add_end_inning_pitcher_sub(pitcher_app, total_pa_num, last_batter_no_pa):
    batting_pos_index = (
        (total_pa_num % LEN_BATTING_LIST) +
        int(last_batter_no_pa)
    )

    x_pos = BOX_WIDTH * pitcher_app.end_inning_num
    y_pos = ((BOX_HEIGHT * batting_pos_index) +
             (BOX_HEIGHT // 2))

    this_sub_division_svg = (
        PITCHER_SUB_DIVISION_LINE.format(
            x_pos_1=x_pos,
            x_pos_2=x_pos + BOX_WIDTH,
            y_pos=y_pos
        )
    )

    return this_sub_division_svg

def get_box_score_whip_era(box_score_tuple):
    if box_score_tuple.ERA is not None:
        if box_score_tuple.ERA == '&#8734;':
            era_str = '&#8734;'
        else:
            era_str = ('%.2f' % box_score_tuple.ERA)
    else:
        era_str = ''

    if box_score_tuple.WHIP is not None:
        if box_score_tuple.WHIP == '&#8734;':
            whip_str = '&#8734;'
        else:
            whip_str = ('%.3f' % box_score_tuple.WHIP)
    else:
        whip_str = ''

    return era_str, whip_str

def get_pitcher_box_score_lines(pitcher_app_list, chunk_size, box_score_dict):
    pitcher_rows_svg = ''
    row_increment = 0

    if chunk_size == SMALL_CHUNK_SIZE:
        initial_y = PITCHER_BOX_SCORE_LARGE_Y
        text_size_1 = PITCHER_LARGE_FONT_SIZE
        text_size_2 = PITCHER_STATS_LARGE_FONT_SIZE
        stats_offset = PITCHER_BOX_STATS_LARGE_Y_OFFSET
        defined_text_increment = PITCHER_BOX_SCORE_LARGE_Y_INCREMENT
    elif chunk_size == LARGE_CHUNK_SIZE:
        initial_y = PITCHER_BOX_SCORE_SMALL_Y
        text_size_1 = PITCHER_SMALL_FONT_SIZE
        text_size_2 = PITCHER_STATS_SMALL_FONT_SIZE
        stats_offset = PITCHER_BOX_STATS_SMALL_Y_OFFSET
        defined_text_increment = PITCHER_BOX_SCORE_SMALL_Y_INCREMENT

    for pitcher_app in pitcher_app_list:
        if (len(str(pitcher_app.player_obj)) > 18 and
                chunk_size == SMALL_CHUNK_SIZE):
            initial_y = PITCHER_BOX_SCORE_MED_Y
            text_size_1 = PITCHER_MED_FONT_SIZE
            text_size_2 = PITCHER_STATS_MED_FONT_SIZE
            stats_offset = PITCHER_BOX_STATS_MED_Y_OFFSET
            defined_text_increment = PITCHER_BOX_SCORE_MED_Y_INCREMENT

    for pitcher_app in pitcher_app_list:
        initial_y = PITCHER_BOX_SCORE_SMALL_Y
        box_score_tuple = box_score_dict[pitcher_app.player_obj]
        era_str, whip_str = get_box_score_whip_era(box_score_tuple)
        initial_era_stat_str = 'ERA: ' + str(pitcher_app.player_obj.era)
        appears_str = '({}, {})'.format(pitcher_app.start_inning_num,
                                        pitcher_app.position)

        pitcher_str = '{}'.format(pitcher_app.player_obj)
        if pitcher_app.player_obj.pitch_hand:
            pitcher_str += ', {}'.format(pitcher_app.player_obj.pitch_hand)

        pitcher_rows_svg += PITCHER_STATS_LINE_TEMPLATE.format(
            pitcher_id=pitcher_app.player_obj.mlb_id,
            name_y_pos=initial_y + row_increment,
            stats_y_pos=stats_offset + row_increment,
            pitcher=pitcher_str,
            box_score_1=box_score_tuple.IP, box_score_2=box_score_tuple.WLS,
            box_score_3=box_score_tuple.BF, box_score_4=box_score_tuple.H,
            box_score_5=box_score_tuple.R, box_score_6=box_score_tuple.ER,
            box_score_7=box_score_tuple.SO, box_score_8=box_score_tuple.BB,
            box_score_9=box_score_tuple.IBB, box_score_10=box_score_tuple.HBP,
            box_score_11=box_score_tuple.BLK, box_score_12=box_score_tuple.WP,
            box_score_13=box_score_tuple.HR, box_score_14=box_score_tuple.S,
            box_score_15=box_score_tuple.P, box_score_16=era_str,
            box_score_17=whip_str,
            stats=initial_era_stat_str,
            appears=appears_str,
            size_1=text_size_1,
            size_2=text_size_2
        )

        row_increment += defined_text_increment

    return pitcher_rows_svg

def chunks(this_list, num_elements):
    for i in range(0, len(this_list), num_elements):
        yield this_list[i:i + num_elements]

def create_pitcher_stats_svg(chunk_tuple_list, chunk_size, box_score_dict):
    pitcher_stats_svg = ''
    for location, pitcher_chunk in chunk_tuple_list:
        x_box, y_box = location
        pitcher_stats_svg += PITCHER_STATS_HEADER.format(x_box=x_box,
                                                         y_box=y_box)

        pitcher_stats_svg += '{}{}'.format(
            get_pitcher_box_score_lines(pitcher_chunk,
                                        chunk_size,
                                        box_score_dict),
            SVG_FOOTER
        )

    return pitcher_stats_svg

def add_team_pitcher_box_score(team, box_score_dict, offset):
    pitcher_app_list = team.pitcher_list
    if len(pitcher_app_list) <= 10:
        chunk_size = SMALL_CHUNK_SIZE
    else:
        chunk_size = LARGE_CHUNK_SIZE

    pitcher_chunk_list = list(chunks(pitcher_app_list, chunk_size))
    location_tuple_list = [
        (0, BOX_HEIGHT * 10 + offset),
        (WIDTH // 2, BOX_HEIGHT * 10 + offset)
    ]

    chunk_tuple_list = []
    for location_index, location_tuple in enumerate(location_tuple_list):
        if location_index < len(pitcher_chunk_list):
            pitcher_chunk = pitcher_chunk_list[location_index]
        else:
            pitcher_chunk = []

        chunk_tuple_list.append((location_tuple, pitcher_chunk))

    pitcher_stats_svg = create_pitcher_stats_svg(chunk_tuple_list,
                                                 chunk_size,
                                                 box_score_dict)

    return pitcher_stats_svg

def add_all_pitcher_box_scores(game):
    all_pitcher_box_svg = ''

    tuple_list = [
        (game.home_team,
         game.home_pitcher_box_score_dict,
         0),
        (game.away_team,
         game.away_pitcher_box_score_dict,
         HEIGHT // 2)
    ]

    for this_tuple in tuple_list:
        team, box_score_dict, offset = this_tuple
        all_pitcher_box_svg += add_team_pitcher_box_score(team,
                                                          box_score_dict,
                                                          offset)

    return all_pitcher_box_svg

def get_team_stats_svg(game):
    team_stats_svg = ''
    game_width = get_game_width(game)
    tuple_list = [
        (
            game_width - (BOX_WIDTH * 2),
            (BOX_HEIGHT * LEN_BATTING_LIST +
             BOX_HEIGHT // 2),
            game.away_team_stats
        ), (
            game_width - (BOX_WIDTH * 2),
            (HEIGHT // 2 +
             BOX_HEIGHT * LEN_BATTING_LIST +
             BOX_HEIGHT // 2),
            game.home_team_stats
        )
    ]

    for box_x, box_y, stats_tuple in tuple_list:
        team_stats_svg += get_team_stats_box(box_x, box_y, stats_tuple)

    return team_stats_svg

def get_box_score_totals(game):
    box_score_totals_svg = ''
    game_width = get_game_width(game)

    tuple_list = [
        (
            game.away_batter_box_score_dict,
            game_width - BOX_WIDTH,
            6 * BOX_HEIGHT + BOX_HEIGHT // 2
        ),
        (
            game.home_batter_box_score_dict,
            game_width - BOX_WIDTH,
            (6 * BOX_HEIGHT + BOX_HEIGHT // 2 +
             HEIGHT // 2)
        )
    ]

    for box_score_dict, x_pos, y_pos in tuple_list:
        box_score_totals_svg += TOTAL_BOX_SCORE_STATS_BOX.format(
            box_x=x_pos,
            box_y=y_pos,
            stats_str_1=box_score_dict['TOTAL'].AB,
            stats_str_2=box_score_dict['TOTAL'].R,
            stats_str_3=box_score_dict['TOTAL'].H,
            stats_str_4=box_score_dict['TOTAL'].RBI,
            stats_str_5=box_score_dict['TOTAL'].BB,
            stats_str_6=box_score_dict['TOTAL'].SO,
            stats_str_7=box_score_dict['TOTAL'].LOB
        )

    return box_score_totals_svg

def is_bat_around(this_inning_tuple_list, inning_pa_num):
    return (
        len(this_inning_tuple_list) > LEN_BATTING_LIST and
        (inning_pa_num > LEN_BATTING_LIST or
         inning_pa_num <= (len(this_inning_tuple_list) %
                           LEN_BATTING_LIST))
    )

def assemble_stats_svg(game):
    stats_svg = ''
    inning_half_stats_list = get_inning_half_stats_tuple_list(game)
    for inning_num, inning_half_str, stats_tuple in inning_half_stats_list:
        if stats_tuple:
            box_x = inning_num * BOX_WIDTH

            if inning_half_str == 'bottom':
                box_y = (HEIGHT // 2 +
                         BOX_HEIGHT * LEN_BATTING_LIST +
                         BOX_HEIGHT // 2)
            elif inning_half_str == 'top':
                box_y = (BOX_HEIGHT * LEN_BATTING_LIST +
                         BOX_HEIGHT // 2)
            else:
                raise ValueError('Invalid inning half str')

            stats_svg += get_inning_stats_box(box_x, box_y, stats_tuple)

    return stats_svg

def get_logo(game):
    signature_svg = ''
    game_width = get_game_width(game)

    signature_svg = ''
    x_pos = game_width - BOX_WIDTH
    y_pos = 8 * BOX_HEIGHT + BOX_HEIGHT // 2
    away_logo_str = LOGO_DICT.get(game.away_team.abbreviation, DEFAULT_LOGO)
    signature_svg += AWAY_LOGO.format(x_pos=x_pos,
                                      y_pos=y_pos,
                                      logo=away_logo_str)

    x_pos = game_width - BOX_WIDTH
    y_pos = 8 * BOX_HEIGHT + BOX_HEIGHT // 2 + HEIGHT // 2
    home_logo_str = LOGO_DICT.get(game.home_team.abbreviation, DEFAULT_LOGO)
    signature_svg += HOME_LOGO.format(x_pos=x_pos,
                                      y_pos=y_pos,
                                      logo=home_logo_str)

    return signature_svg

def write_individual_pa_svg(svg_content, inning_pa_num, this_inning_tuple_list,
                            this_x_pos, this_y_pos):
    this_svg = ''
    bat_around_flag = False
    if len(this_inning_tuple_list) <= (LEN_BATTING_LIST * 2):
        if is_bat_around(this_inning_tuple_list, inning_pa_num):
            bat_around_flag = True
            this_svg += HALF_SCALE_HEADER
            this_x_pos *= 2
            this_y_pos *= 2
            if inning_pa_num > LEN_BATTING_LIST:
                this_y_pos += BOX_HEIGHT
                this_x_pos += BOX_WIDTH
    else:
        bat_around_flag = True
        this_svg += HALF_SCALE_HEADER
        this_x_pos *= 2
        this_y_pos *= 2
        if LEN_BATTING_LIST < inning_pa_num <= (LEN_BATTING_LIST * 2):
            this_x_pos += BOX_WIDTH
        elif (LEN_BATTING_LIST * 2) < inning_pa_num <= (LEN_BATTING_LIST * 3):
            this_y_pos += BOX_HEIGHT
        elif (LEN_BATTING_LIST * 3) < inning_pa_num:
            this_x_pos += BOX_WIDTH
            this_y_pos += BOX_HEIGHT

    this_svg += '{}{}{}'.format(
        SVG_HEADER.format(x_pos=this_x_pos, y_pos=this_y_pos),
        svg_content,
        SVG_FOOTER
    )

    if bat_around_flag:
        this_svg += HALF_SCALE_FOOTER

    return this_svg

def assemble_box_content_dict(game):
    content_list_svg = ''
    svg_content_list = get_svg_content_list(game)
    top_pa_index = 0
    bottom_pa_index = 0
    for id_tuple, svg_content, summary in svg_content_list:
        inning_num, inning_half_str, inning_pa_num = id_tuple
        top_offset = top_pa_index % LEN_BATTING_LIST
        bottom_offset = bottom_pa_index % LEN_BATTING_LIST
        this_x_pos = inning_num * BOX_WIDTH
        if inning_half_str == 'bottom':
            if (summary != 'Runner Out' and
                    'Caught Stealing' not in summary and
                    'Pickoff' not in summary):
                bottom_pa_index += 1

            this_y_pos = (HEIGHT // 2 +
                          bottom_offset * BOX_HEIGHT +
                          BOX_HEIGHT // 2)
        elif inning_half_str == 'top':
            if (summary != 'Runner Out' and
                    'Caught Stealing' not in summary):
                top_pa_index += 1

            this_y_pos = (top_offset * BOX_HEIGHT +
                          BOX_HEIGHT // 2)
        else:
            raise ValueError('Invalid inning half str')

        this_inning_tuple_list = [
            id_tuple for (id_tuple, _, _) in svg_content_list
            if id_tuple[0] == inning_num and id_tuple[1] == inning_half_str
        ]

        content_list_svg += write_individual_pa_svg(svg_content,
                                                    inning_pa_num,
                                                    this_inning_tuple_list,
                                                    this_x_pos,
                                                    this_y_pos)

    return content_list_svg

def get_game_title_str(game):
    game_teams_str = '{} @ {}'.format(game.away_team.name,
                                      game.home_team.name)

    return game_teams_str

def assemble_game_title_svg(game):
    game_title_svg = ''
    game_str = '{} @ {}'.format(game.away_team.name, game.home_team.name)
    this_start_datetime = (game.start_datetime if game.start_datetime
                           else game.expected_start_datetime)

    if this_start_datetime:
        this_start_datetime = this_start_datetime.astimezone(
            timezone(game.timezone_str)
        )

        est_time = this_start_datetime.astimezone(
            timezone(EASTERN_TIMEZONE_STR)
        )

        if ((est_time.hour == 23 and est_time.minute == 33) or
                (est_time.hour == 0 and est_time.minute == 0)):
            game_datetime = '{}'.format(
                this_start_datetime.strftime('%a %b %d %Y')
            )
        elif game.start_datetime and game.end_datetime:
            start_str = game.start_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p')

            end_str = game.end_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime(' - %-I:%M %p %Z')

            game_datetime = '{}{}'.format(start_str, end_str)
        else:
            game_datetime = game.expected_start_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p %Z')

        if game.is_doubleheader:
            game_datetime += ', Game {}'.format(game.game_date_str[-1])

        if game.is_suspended:
            game_datetime += ', Suspended'
        elif game.is_postponed:
            game_datetime += ', Postponed'

    else:
        game_datetime = ''

    game_width = get_game_width(game)
    location_str = game.location.replace('&', '&amp;')
    detail_str = ''
    if game.attendance:
        detail_str += 'Att. {:,}'.format(int(game.attendance))

    if game.weather:
        if detail_str != '':
            detail_str += ' - '

        detail_str += game.weather

    if game.temp:
        if detail_str != '':
            detail_str += ' - '

        detail_str += '{} F'.format(int(game.temp))

    tuple_list = [('TOP', 0), ('BOTTOM', HEIGHT // 2)]
    for inning_half_str, y_pos in tuple_list:
        title_size = BIG_TITLE_SIZE if len(game_str) < 42 else SMALL_TITLE_SIZE
        game_title_svg += BIG_SVG_TITLE.format(
            x_pos=game_width - BOX_WIDTH,
            y_pos=y_pos,
            inning_half=inning_half_str,
            game_str=game_str,
            location=location_str,
            datetime=game_datetime,
            detail_str=detail_str,
            title_size=title_size
        )

    return game_title_svg

def get_big_rectangles(game):
    game_width = get_game_width(game)

    big_rectangles_svg = '{}{}'.format(
        BIG_RECTANGLE.format(y_pos=0, y_pos_2=HEIGHT // 2, width=game_width),
        BIG_RECTANGLE.format(y_pos=HEIGHT // 2, y_pos_2=HEIGHT, width=game_width)
    )

    return big_rectangles_svg

def get_footer_box(game):
    game_width = get_game_width(game)
    text_pos = game_width - 255
    footer_box_svg = '{}'.format(FOOTER_BOX.format(width=game_width,
                                                   text_pos=text_pos))

    return footer_box_svg

def get_game_svg_str(game):
    big_svg_text = '{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}'.format(
        get_big_svg_header(game),
        get_batter_list_and_stats(game),
        assemble_stats_svg(game),
        assemble_box_content_dict(game),
        get_team_stats_svg(game),
        add_away_batter_sub_division_lines(game),
        add_home_batter_sub_division_lines(game),
        add_away_pitcher_sub_division_lines(game),
        add_home_pitcher_sub_division_lines(game),
        add_all_pitcher_box_scores(game),
        assemble_game_title_svg(game),
        get_logo(game),
        get_box_score_totals(game),
        get_big_rectangles(game),
        get_footer_box(game),
        SVG_FOOTER
    )

    return big_svg_text
