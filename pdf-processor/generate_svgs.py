from datetime import datetime

from sys import exc_info
from traceback import format_exception

from multiprocessing import Pool

import baseball

"""
baseball.fetch_game.write_svg_from_file_range(
    '1950-01-01',
    '1960-01-01',
    '/Volumes/B_Crom_SSD/raw_mlb_data',
    '/Volumes/B_Crom_SSD/scorecards',
    True,
    True
)
"""

def f(this_date_tuple):
    start_date_str, end_date_str = this_date_tuple
    baseball.fetch_game.write_svg_from_file_range(
        start_date_str,
        end_date_str,
        '/Volumes/B_Crom_SSD/raw_mlb_data',
        '/Volumes/B_Crom_SSD/scorecards',
        True,
        True
    )

date_list = [
    ('1950-01-01', '1955-01-01'),
    ('1955-01-01', '1960-01-01'),
    ('1960-01-01', '1965-01-01'),
    ('1965-01-01', '1970-01-01'),
    ('1970-01-01', '1975-01-01'),
    ('1975-01-01', '1980-01-01'),
    ('1980-01-01', '1985-01-01'),
    ('1985-01-01', '1990-01-01'),
    ('1990-01-01', '1995-01-01'),
    ('1995-01-01', '2000-01-01'),
    ('2000-01-01', '2005-01-01'),
    ('2005-01-01', '2010-01-01'),
    ('2010-01-01', '2015-01-01'),
    ('2015-01-01', '2020-01-01'),
    ('2020-01-01', '2025-01-01')
]

with Pool(16) as p:
    p.map(f, date_list)
