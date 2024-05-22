import datetime

import baseball

this_datetime = datetime.datetime(2024,5,5)
baseball.write_games_for_date(this_datetime, '/var/www/html', True, True, True)
