from datetime import timedelta, datetime
from re import findall
from urllib.request import urlopen

from boto3 import resource

LINK_TEMPLATE = (
    'http://gd2.mlb.com/components/game/mlb/year_{year}/month_{month}/day_{day}/'
)

s3 = resource("s3")
bucket = s3.Bucket('livebaseballscorecards-artifacts')

def lambda_handler(event, context):
    time_shift = timedelta(hours=14)
    today = datetime.utcnow() - time_shift

    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)

    today_link = LINK_TEMPLATE.format(year=year, month=month, day=day)
    content = str(urlopen(today_link).read())
    game_id_list = findall(r'>\s*(gid\_\w+)/<', content)

    for game_id in game_id_list:
        today_game_link = today_link + '{}/'.format(game_id)
        boxscore_link = today_game_link + 'boxscore.xml'
        players_link = today_game_link + 'players.xml'
        inning_link = today_game_link + 'inning/inning_all.xml'

        boxscore_xml = urlopen(boxscore_link).read().decode('utf-8')
        boxscore_key = boxscore_link.split('game/mlb/year_')[1]
        players_xml = urlopen(players_link).read().decode('utf-8')
        players_key = players_link.split('game/mlb/year_')[1]
        inning_xml = urlopen(inning_link).read().decode('utf-8')
        inning_key = inning_link.split('game/mlb/year_')[1]

        bucket.put_object(Key=boxscore_key, Body=boxscore_xml)
        bucket.put_object(Key=players_key, Body=players_xml)
        bucket.put_object(Key=inning_key, Body=inning_xml)

    return "OK"
