import argparse
import logging

from datetime import timedelta, datetime
from typing import List, Optional
from requests import get
from dateutil.parser import parse as dateparse
from pathlib import Path

from baseball import (fetch_schedule_summary, generate_today_game_svgs)

logger = logging.getLogger('baseball.cli')
FORMAT = '%(levelname)s [%(name)s] %(asctime)s (%(filename)s:%(lineno)s -- %(funcName)s) :: %(message)s'
logging.basicConfig(format=FORMAT)

EPILOG = "Copyright (c) 2018-2023 Benjamin B. Crom - MIT License"

def dir_path(string):
    file_or_dir = Path(string)
    if not file_or_dir.exists() or not file_or_dir.is_file() or file_or_dir.is_dir():
        return string
    else:
        raise argparse.ArgumentTypeError(f"'{string}' is not a valid path")

def schedule_main(args) -> int:
    schedule_summary = fetch_schedule_summary(args)
    return 0

def site_generate_main(args) -> int:
    print("Generating livebaseballscorecards files in {output_dir}".format(output_dir=args.output_dir))
    generate_today_game_svgs(args.output_dir, args.write_game_html, args.write_date_html, args.write_index_html)
    return 0

def main(args: Optional[List[str]] = None) -> int:

    if args is None:
        import sys
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="baseball", epilog=EPILOG)
    subparsers = parser.add_subparsers(required=False, title="commands", help="additional command help")

    schedule_parser = subparsers.add_parser("schedule", help="baseball schedule retrieving command", epilog=EPILOG)
    schedule_parser.set_defaults(func=schedule_main)
    schedule_parser.add_argument("--start-date", type=str, help="start or only date to retrieve games for", metavar="YYYY-MM-DD", nargs='?')
    schedule_parser.add_argument("--end-date", type=str, help="end date to retrieve games for, if not set will be the same as start-date", metavar="YYYY-MM-DD", nargs='?')

    site_generate_parser = subparsers.add_parser("site-generate", help="generate artifacts based on baseball stats information", epilog=EPILOG)
    site_generate_parser.set_defaults(func=site_generate_main)
    site_generate_parser.add_argument("--output-dir", type=dir_path, help="output directory to write files, will be created if it doesn't exist")
    site_generate_parser.add_argument("-g", "--write-game-html", action="store_true", help="also generate game html along with svg files")
    site_generate_parser.add_argument("-d", "--write-date-html", action="store_true", help="also generate date html along with svg files")
    site_generate_parser.add_argument("-i", "--write-index-html", action="store_true", help="also generate index html along with svg files")

    parsed_args = parser.parse_args()
    if hasattr(parsed_args, 'func'):
        return(parsed_args.func(parsed_args))
    else:
        parser.print_usage()
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
