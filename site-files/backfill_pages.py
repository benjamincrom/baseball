"""Bring the archive's pages up to the current templates, once.

A game page is template alone (its title and its card's file name), so
each is regenerated from HTML_WRAPPER with polling off. A day page carries
the games' captions, which the file names cannot give back, so only its
loaders are rewritten: the old jQuery script that refetched every card
every ten seconds becomes a one-time load, the loader function is put in
the head, and the jQuery tag goes. The site's current date is left to the
generator, which owns it. Every write is a temporary file renamed into
place, so nginx never serves a half-written page. Idempotent: a page
already current is not touched.

    python3 backfill_pages.py /var/www/html --exclude 2026-09-23 [--prefix 1950-] [--dry-run]
"""
import argparse
import os
import re
import sys

from baseball.fetch_game import HTML_WRAPPER, LBS_LOADER_JS

GAME_PAGE = re.compile(r'^(\d{4}-\d{2}-\d{2}-[A-Z0-9]+-[A-Z0-9]+-\d)\.html$')
DAY_PAGE = re.compile(r'^(\d{4}-\d{2}-\d{2})\.html$')
# The old loader on a day page: one script per game, jQuery inside, no '<' in it.
OLD_ENTRY = re.compile(r"<script>\$\(document\)\.ready\(function\(\) \{\$\.get\('([^']+)\.svg'[^<]*</script>")
JQUERY_TAG = re.compile(r'<script src="https://ajax\.googleapis\.com/ajax/libs/jquery/[^"]*"></script>')
LOADER_TAG = '<script>' + LBS_LOADER_JS.format() + '</script>'


def write_atomically(path, text):
    tmp = os.path.join(os.path.dirname(path), f'.{os.path.basename(path)}.tmp-{os.getpid()}')
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(text)
    os.replace(tmp, path)


def new_game_page(game_id):
    return HTML_WRAPPER.format(title=game_id, filename=game_id + '.svg', poll_ms=0)


def new_day_page(old):
    if not OLD_ENTRY.search(old):
        return None
    text = OLD_ENTRY.sub(lambda m: f"<script>lbsLoad('{m.group(1)}.svg', '{m.group(1)}', 0, true);</script>", old)
    text = JQUERY_TAG.sub('', text)
    if 'function lbsLoad(' not in text:
        text = text.replace('</head>', LOADER_TAG + '</head>', 1)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--exclude', action='append', default=[], help="a date the generator owns, e.g. today's")
    ap.add_argument('--prefix', default='', help='only files starting with this, e.g. 1950-')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    counts = {'game_rewritten': 0, 'game_current': 0, 'day_rewritten': 0, 'day_untouched': 0, 'skipped': 0, 'errors': 0}
    for name in sorted(os.listdir(args.root)):
        if not name.startswith(args.prefix):
            continue
        if any(name.startswith(d) for d in args.exclude):
            counts['skipped'] += 1
            continue
        path = os.path.join(args.root, name)
        try:
            game = GAME_PAGE.match(name)
            day = DAY_PAGE.match(name)
            if game:
                text = new_game_page(game.group(1))
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    if fh.read() == text:
                        counts['game_current'] += 1
                        continue
                if not args.dry_run:
                    write_atomically(path, text)
                counts['game_rewritten'] += 1
            elif day:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    old = fh.read()
                text = new_day_page(old)
                if text is None or text == old:
                    counts['day_untouched'] += 1
                    continue
                if not args.dry_run:
                    write_atomically(path, text)
                counts['day_rewritten'] += 1
        except Exception as e:  # keep going: one bad page must not stop the rest
            counts['errors'] += 1
            print(f'{name}: {e}', file=sys.stderr)
    print(('dry run: ' if args.dry_run else '') + ', '.join(f'{k}={v}' for k, v in counts.items()))


if __name__ == '__main__':
    main()
