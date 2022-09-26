

import json
from json import JSONEncoder
from math import ceil
from pydantic import BaseModel

class Match(BaseModel):
        # DaweDraft(nameKey, match_data.dawe_id, PORT, match_data.game_version, match_data.blue_players, match_data.red_players, match_data.game_config).init()
    dawe_id: str
    game_version: str
    blue_players: list[str]
    red_players: list[str]
    game_config: dict


class Champion:
    def __init__(self, name: str, version: str):
        self.name = name.lower() if type(name) == str else ''
        self.idName = name.lower() if type(name) == str else ''
        
        if type(name) == str:
            self.loadingImg = f'/cache/{version}/champion/{self.name}_loading.jpg' 
            self.splashImg = f'/cache/{version}/champion/{self.name}_splash.jpg'
            self.splashCenteredImg = f'/cache/{version}/champion/{self.name}_centered_splash.jpg'
            self.squareImg = f'/cache/{version}/champion/{self.name}_square.png'
        else: 
            self.loadingImg, self.splashCenteredImg, self.splashImg, self.squareImg = ('','','','')
    def to_json(self):
        return self.__dict__
class Position:
    TOP = 0
    JUNGLER = 1
    MID = 2
    ADC = 3
    SUPPORT = 4

class Ban:
    def __init__(self, champion: Champion, active: bool):
        self.champion = champion
        self.isActive = active


    def to_json(self):
        return self.__dict__
class Pick:
    def __init__(self, champion: Champion, position: Position, name: str, active: bool):
        self.isActive = active
        self.displayName = name
        self.id = position
        self.champion = champion


    def to_json(self):
        return self.__dict__
class Team:
    def __init__(self, listBans: list[Ban], listPicks: list[Pick], active: bool):
        self.bans = listBans
        self.picks = listPicks
        self.isActive = active


    def to_json(self):
        return self.__dict__

class State:
    def __init__(self, blueTeam: Team, redTeam: Team, version: str, time: int, state: str, config: dict) -> None:
        self.leagueConnected = True
        self.champSelectActive = True
        self.blueTeam = blueTeam
        self.redTeam = redTeam
        self.meta = {
            "cdn": "https://ddragon.leagueoflegends.com/cdn",
            "version": {
                "champion": version,
                "item": version
                }
        }
        self.timer = time
        self.state = state
        self.config = config
    def to_json(self):
        return self.__dict__

class Message:
    def __init__(self, state: State):
        self.eventType = 'newState'
        self.state = state
    
class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

