**Table of Contents**

- [Baseball](#baseball)
    - [Installing from pypi](#installing-from-pypi)
    - [Installing from source](#installing-from-source)
    - [Recover Scrabble Game](#recover-scrabble-game)
    - [Play Scrabble Game](#play-scrabble-game)
        - [Create a new Scrabble game object](#create-a-new-scrabble-game-object)
        - [Make Move](#make-move)
        - [Find Best Move (Brute Force)](#find-best-move-brute-force)
        - [Exchange Tiles](#exchange-tiles)
        - [Conclude Game](#conclude-game)

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

## Game Structure
### Game
- away_batter_box_score_dict
- away_pitcher_box_score_dict
- away_team (Team)
- away_team_stats
- first_pitch_datetime
- first_pitch_str
- game_date_str
- home_batter_box_score_dict
- home_pitcher_box_score_dict
- home_team (Team)
- home_team_stats
- inning_list (Inning list)
- last_pitch_datetime
- last_pitch_str
- location

### Team
- abbreviation
- batting_order_list_list (List of nine PlayerApperance lists)
- name
- pitcher_list (PlayerApperance list)
- player_id_dict
- player_last_name_dict
- player_name_dict

### Inning
- bottom_half_appearance_list (PlateAppearance list)
- bottom_half_inning_stats
- top_half_appearance_list (PlateAppearance list)
- top_half_inning_stats

### PlateAppearance
- batter (Player)
- batting_team (Team)
- error_str
- event_list (list: Pitch, Pickoff, RunnerAdvance, Substitution, Switch objects)
- got_on_base
- hit_location
- inning_outs
- out_runners_list (Player list)
- pitcher (Player)
- plate_appearance_description
- plate_appearance_summary
- runners_batted_in_list (Player list)
- scorecard_summary
- scoring_runners_list (Player list)

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
- player_obj (Player)
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
- runner (Player)
- start_base
- end_base
- runner_scored
- run_earned
- is_rbi

### Substitution
- incoming_player (Player)
- outgoing_player (Player)
- batting_order
- position

### Switch
- player (Player)
- old_position_num
- new_position_num
- new_batting_order

## Functions

get_game_xml_from_url
write_svg_from_url
write_svg_from_file_range
write_game_svg_and_html
get_game_generator_from_file_range
get_game_list_from_file_range
get_game_from_xml_strings
get_game_from_files
get_filename_list



* __scrabble.main.ScrabbleGame(__*num_players*__)__

```
>>> from scrabble.main import ScrabbleGame
>>> game = ScrabbleGame(num_players=4)
>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______★_______
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[G, T, E, A, D, P, C], [E, I, S, O, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 0
Player 1's move
72 tiles remain in bag
Player 1: 0
Player 2: 0
Player 3: 0
Player 4: 0
```

### Make Move
* __scrabble.main.ScrabbleGame.place\_word(__*word, start_location, is_vertical_move*__)__

Place a word from the rack of the next player onto the board.  If the
move is legal you will be prompted as to whether or not the move was
successfully challenged.  If the move goes through through then the method will
return `True`.  If the move is illegal you will not receive a challenge prompt
and the method will return `False`.
```
>>> game.place_word(word='GATE', start_location=('h', 8), is_vertical_move=False)
Challenge successful (Y/N)N
True

>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______GATE____
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[D, P, C, O, E, F, N], [E, I, S, O, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 1
Player 2's move
68 tiles remain in bag
Player 1: 10
Player 2: 0
Player 3: 0
Player 4: 0
```

### Find Best Move (Brute Force)
* **scrabble.main.ScrabbleGame.get_best_move()**

Find the best move via brute-force search.  Returns the move score and move
tuple of the form *(location, word, is_vertical_move)*.
```
>>> game.get_best_move()

(27, (('l', 4), 'EGOISM', True))
```

### Exchange Tiles
* __scrabble.main.ScrabbleGame.exchange(__*letter_list*__)__

Exchange up to all a player's rack tiles as long as the bag has at least
one entire rack of tiles remaining.
```
>>> game.exchange(letter_list=['E', 'I', 'S', 'O'])
True

>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______GATE____
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[D, P, C, O, E, F, N], [A, P, R, M, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 1
Player 3's move
68 tiles remain in bag
Player 1: 10
Player 2: 0
Player 3: 0
Player 4: 0
```

### Conclude Game
* __scrabble.main.ScrabbleGame.conclude\_game(__*empty_rack_id=None*__)__

Calculates final scores and declares a winner.  This method will automatically
be called and bonuses automatically awarded if one player has an empty rack
(plays out) when the tile bag is empty.
```
>>> game.conclude_game()
Game Over! Player 1 wins with a score of 10
```
