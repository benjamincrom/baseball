**Table of Contents**

- [Baseball](#baseball)
    - [Installing from pypi](#installing-from-pypi)
    - [Installing from source](#installing-from-source)
    - [Fetch individual MLB game](#fetch-individual-mlb-game)
    - [Fetch list of MLB games](#fetch-list-of-mlb-games)
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

# Baseball
This package fetches and parses event data for Major League Baseball games.

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
```
Write scorecard as SVG image:
```python
with open(game_id + '.svg') as fh:
    fh.write(game.get_svg_str())
```

## Fetch list of MLB games
* __get_game_list_from_file_range(__*start_date_str, end_date_str, input_dir*__)__

Fetch a list of game objects which each contain metadata and events for a single MLB game.

First, download and unzip the source data:
```shell
wget https://spaces-host.nyc3.digitaloceanspaces.com/livebaseballscorecards-artifacts/baseball_files_2008-2017.zip
unzip baseball_files_2008-2017.zip -d ./baseball_files_2008-2017
```
Then import the files in Python using this library:
```python
import baseball
game_tuple_list = baseball.get_game_list_from_file_range('1-1-2017', '12-31-2017', 'baseball_files_2008-2017')
```
See [the included Jupyter notebook](baseball_stats.ipynb) for examples on how to use a game object for analysis.

## Game Class Structure
### Game
- away_batter_box_score_dict
- away_pitcher_box_score_dict
- away_team __([Team](#team))__
- away_team_stats
- first_pitch_datetime
- first_pitch_str
- game_date_str
- home_batter_box_score_dict
- home_pitcher_box_score_dict
- home_team __([Team](#team))__
- home_team_stats
- inning_list __(Inning list)__
- last_pitch_datetime
- last_pitch_str
- location
- get_svg_str()

### Team
- abbreviation
- batting_order_list_list __(List of nine [PlayerAppearance](#playerappearance) lists)__
- name
- pitcher_list __([PlayerAppearance](#playerappearance) list)__
- player_id_dict
- player_last_name_dict
- player_name_dict

### Inning
- bottom_half_appearance_list __([PlateAppearance](#plateappearance) list)__
- bottom_half_inning_stats
- top_half_appearance_list __([PlateAppearance](#plateappearance) list)__
- top_half_inning_stats

### PlateAppearance
- batter __([Player](#player))__
- batting_team __([Team](#team))__
- error_str
- event_list __(list: Pitch, Pickoff, RunnerAdvance, Substitution, Switch objects)__
- got_on_base
- hit_location
- inning_outs
- out_runners_list __([Player](#player) list)__
- pitcher __([Player](#player))__
- plate_appearance_description
- plate_appearance_summary
- runners_batted_in_list __([Player](#player) list)__
- scorecard_summary
- scoring_runners_list __([Player](#player) list)__

### Player
- era
- first_name
- last_name
- mlb_id
- number
- obp
- slg

### PlayerAppearance
- start_inning_batter_num
- start_inning_half
- start_inning_num
- end_inning_batter_num
- end_inning_half
- end_inning_num
- pitcher_credit_code
- player_obj __([Player](#player))__
- position

### Pitch
- pitch_description
- pitch_position
- pitch_speed
- pitch_type

### Pickoff
- pickoff_description
- pickoff_base
- pickoff_was_successful

### RunnerAdvance
- run_description
- runner __([Player](#player))__
- start_base
- end_base
- runner_scored
- run_earned
- is_rbi

### Substitution
- incoming_player __([Player](#player))__
- outgoing_player __([Player](#player))__
- batting_order
- position

### Switch
- player __([Player](#player))__
- old_position_num
- new_position_num
- new_batting_order

## Functions

write_svg_from_url
write_svg_from_file_range
write_game_svg_and_html
get_game_generator_from_file_range
get_game_list_from_file_range
get_game_from_xml_strings
get_game_from_files
get_filename_list
