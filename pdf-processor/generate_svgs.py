import baseball

# write_svg_from_file_range now parallelizes internally across a process pool
# (SVG_PROCESS_POOL_SIZE in baseball/fetch_game.py), so these ranges are run one
# after another rather than wrapped in an outer Pool. An outer pool would make
# these workers daemonic, and daemonic processes cannot create the child
# processes that the inner pool needs.
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

if __name__ == '__main__':
    for start_date_str, end_date_str in date_list:
        baseball.fetch_game.write_svg_from_file_range(
            start_date_str,
            end_date_str,
            '/Volumes/B_Crom_SSD/raw_mlb_data',
            '/Volumes/B_Crom_SSD/scorecards',
            True,
            True
        )
