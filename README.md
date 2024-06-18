**Table of Contents**

- [Baseball](#baseball)
    - [Installing from pypi](#installing-from-pypi)
    - [Installing from source](#installing-from-source)
    - [Fetch individual MLB game](#fetch-individual-mlb-game)
    - [Fetch list of MLB games](#fetch-list-of-mlb-games)
    - [Get Game generator given target directory and date range](#get-game-generator-given-target-directory-and-date-range)
    - [Get raw XML files for an individual MLB game](#get-raw-xml-files-for-an-individual-mlb-game)
    - [Convert XML documents into Game object](#convert-xml-documents-into-game-object)
    - [Write scorecard SVGs for all MLB games on a given date](#write-scorecard-svgs-for-all-mlb-games-on-a-given-date)
    - [Game Class Structure](#game-class-structure)
        - [Game](#game)
        - [Team](#team)
        - [Inning](#inning)
        - [PlateAppearance](#plateappearance)
        - [Player](#player)
        - [PlayerAppearance](#playerappearance)
        - [Pitch](#pitch)
        - [Pickoff](#pickoff)
        - [RunnerAdvance](#runneradvance)
        - [Substitution](#substitution)
        - [Switch](#switch)
    - [Analyze a game: 2017 World Series - Game 7](#analyze-a-game-2017-world-series---game-7)
    - [Analyze a player's season: R.A. Dickey - 2017](#analyze-a-players-season-ra-dickey---2017)
    - [Analyze a lineup of pitchers: Atlanta Braves - 2017 Regular Season](#analyze-a-lineup-of-pitchers-atlanta-braves---2017-regular-season)

# Baseball
This package fetches and parses event data for Major League Baseball games.  [Game](#game) objects generated via the **\_from\_url** methods pull data from MLB endpoints where events are published within about 30 seconds of occurring.  This [XML/JSON source data zip file](https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball_1974_2021.zip) contains event data from MLB games 1974 - 2020.

## Installing from pypi
```
pip3 install baseball
```
## Installing from source
```
git clone git@github.com:benjamincrom/baseball.git
cd baseball/
python3 setup.py install
```

## Fetch individual MLB game
* __get_game_from_url(__*date_str, away_code, home_code, game_number*__)__

Fetch an object which contains metadata and events for a single MLB game.
```python
import baseball
game_id, game = baseball.get_game_from_url('2017-11-1', 'HOU', 'LAD', 1)
game_dict = game._asdict()
game_json_str = game.json()
```
Write scorecard as SVG image:
```python
with open(game_id + '.svg', 'w') as fh:
    fh.write(game.get_svg_str())
```
2017-11-01-HOU-LAD-1.svg
![svg](README_images/2017-11-01-HOU-LAD-1.svg)

