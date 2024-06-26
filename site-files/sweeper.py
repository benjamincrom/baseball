from datetime import date, timedelta, datetime

import baseball

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = datetime(1967, 6, 1)
end_date = datetime(2025, 1, 1)
for single_date in daterange(start_date, end_date):
    #print(single_date)
    try:
        baseball.write_games_for_date(single_date, '/mnt/backfill', True, True, True)
    except Exception as e:
        print(e)
        continue

