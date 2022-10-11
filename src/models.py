

from json import JSONEncoder
from pydantic import BaseModel
from fastapi import WebSocket
from typing import List


class RegisteredTeam(BaseModel):
    name: str
    logo: str
    score: int
    coach: str
    players: list[str]

class Match(BaseModel):
        # DaweDraft(nameKey, match_data.dawe_id, PORT, match_data.game_version, match_data.blue_players, match_data.red_players, match_data.game_config).init()
    dawe_id: str
    game_version: str
    blue_team: RegisteredTeam
    red_team: RegisteredTeam
    tournament_logo: str
    


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

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
