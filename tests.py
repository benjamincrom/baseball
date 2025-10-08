import baseball

def test_fetch_game():
    game_id, game = baseball.get_game_from_url('11-1-2017', 'HOU', 'LAD', 1)
    assert game.weather == 'Overcast'
    assert game_id == '2017-11-01-HOU-LAD-1'
