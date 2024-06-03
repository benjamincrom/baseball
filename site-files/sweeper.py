from datetime import date, timedelta, datetime

import baseball

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = datetime(1965, 5, 1)
end_date = datetime(1966, 6, 2)
for single_date in daterange(start_date, end_date):
    #try:
    baseball.write_games_for_date(single_date, '.', True, True, True)
    #except Exception as e:
    #    print(e)
    #    continue