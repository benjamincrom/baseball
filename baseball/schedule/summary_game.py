""" PEP 610 """
import json
import re
import urllib.parse

from typing import Any, Dict, Iterable, Optional, Type, TypeVar, Union

# {'gamePk': 718501, 'link': '/api/v1.1/game/718501/feed/live', 'gameType': 'R', 'season': '2023', 'gameDate': '2023-04-20T00:10:00Z', 'officialDate': '2023-04-19', 'status': {'abstractGameState': 'Preview', 'codedGameState': 'P', 'detailedState': 'Pre-Game', 'statusCode': 'P', 'startTimeTBD': False, 'abstractGameCode': 'P'}, 'teams': {'away': {'leagueRecord': {'wins': 11, 'losses': 7, 'pct': '.611'}, 'score': 0, 'team': {'id': 141, 'name': 'Toronto Blue Jays', 'link': '/api/v1/teams/141'}, 'splitSquad': False, 'seriesNumber': 6}, 'home': {'leagueRecord': {'wins': 8, 'losses': 10, 'pct': '.444'}, 'score': 0, 'team': {'id': 117, 'name': 'Houston Astros', 'link': '/api/v1/teams/117'}, 'splitSquad': False, 'seriesNumber': 6}}, 'venue': {'id': 2392, 'name': 'Minute Maid Park', 'link': '/api/v1/venues/2392'}, 'content': {'link': '/api/v1/game/718501/content'}, 'gameNumber': 1, 'publicFacing': True, 'doubleHeader': 'N', 'gamedayType': 'P', 'tiebreaker': 'N', 'calendarEventID': '14-718501-2023-04-19', 'seasonDisplay': '2023', 'dayNight': 'night', 'scheduledInnings': 9, 'reverseHomeAwayStatus': False, 'inningBreakLength': 120, 'gamesInSeries': 3, 'seriesGameNumber': 3, 'seriesDescription': 'Regular Season', 'recordSource': 'S', 'ifNecessary': 'N', 'ifNecessaryDescription': 'Normal Game'}

class ScheduleSummaryGame:

    def __init__(self, gamePk: str, link: str, officialDate: str, away_team: str, home_team: str, game_status: str) -> None:
        self.gamePk = gamePk
        self.link = link
        self.officialDate = officialDate
        self.away_team = away_team
        self.home_team = home_team
        self.game_status = game_status

    @classmethod
    def from_dict(self, d: Dict[str, Any]) -> "ScheduleSummaryGame":
        return self(gamePk=d['gamePk'],
                    link=d['link'],
                    officialDate=d['officialDate'],
                    away_team=d['teams']['away']['team']['name'],
                    home_team=d['teams']['home']['team']['name'],
                    game_status=d['status']['detailedState'])

    def _asdict(self):
        return ({'gamePk': self.gamePk,
                'link': self.link,
                'officialDate': self.officialDate,
                'away_team': self.away_team,
                'home_team': self.home_team,
                'game_status': self.game_status})

    def json(self):
        return json.dumps(self._asdict())

    def __repr__(self):
        return f'ScheduleSummaryGame(gamePk={self.gamePk}, officialDate="{self.officialDate}", description="{self.home_team} vs. {self.away_team}", status="{self.game_status}")'

    def __str__(self):
        return self.__repr__()
