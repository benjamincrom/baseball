from datetime import date, timedelta, datetime

import baseball

import sys

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = datetime(1950, 1, 1)
end_date = datetime(1959, 1, 1)
for single_date in daterange(start_date, end_date):
    baseball.write_games_for_date(single_date, '/backfill', True, True, True)
    eprint(single_date)

