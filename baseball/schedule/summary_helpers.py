# -*- coding: utf-8 -*-
import argparse
import logging

from datetime import timedelta, datetime
from typing import List, Optional
from requests import get
from dateutil.parser import parse as dateparse

from .summary_game import ScheduleSummaryGame
from baseball.core import formatted_date, formatted_date_from_str

GAME_SCHEDULE_URL = ('https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1'
                     '&startDate={start_date}'
                     '&endDate={end_date}'
                     '&hydrate=decisions,probablePitcher(note),linescore,broadcasts,game(content(media(epg))),seriesStatus')

logger = logging.getLogger('baseball.cli')
FORMAT = '%(levelname)s [%(name)s] %(asctime)s (%(filename)s:%(lineno)s -- %(funcName)s) :: %(message)s'
logging.basicConfig(format=FORMAT)

def fetch_schedule_summary(args) -> "ScheduleSummaryGame[]":
    logger.info(args)
    time_shift = timedelta(minutes = 545)
    today = datetime.utcnow() - time_shift
    today_date_str = formatted_date(today)
    start_date_str = None
    end_date_str = None
    if args.start_date is not None:
        start_date_str = formatted_date_from_str(args.start_date)
    else:
        start_date_str = today_date_str

    if args.end_date is not None:
        end_date_str = formatted_date_from_str(args.end_date)
    else:
        end_date_str = start_date_str

    all_games_dict = get(
        GAME_SCHEDULE_URL.format(start_date=start_date_str, end_date=end_date_str)
    ).json()

    game_list = []
    for x in all_games_dict['dates']:
        for y in x['games']:
            game_list.append(ScheduleSummaryGame.from_dict(y))
    for g in game_list:
        print(g)

    return game_list
