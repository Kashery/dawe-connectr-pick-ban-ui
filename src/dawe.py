from distutils.command.config import config
from models import *
import json
from websocket import create_connection, WebSocket, WebSocketTimeoutException
from utils import convert_turn_to_state
DAWE_URL = "draftlol.dawe.gg"
WS_SERVER = "ws://localhost:" 
class DaweDraft:
    def __init__(self, path_key : str, dawe_game : str, port: str, game_version: str, blueTeam: list, redTeam: list, config) -> None:
        self.path_key = path_key
        self.dawe_game = dawe_game
        self.port = port
        self.game_version = game_version
        self.redTeam = redTeam
        self.blueTeam = blueTeam
        self.config = config
        self.status_start()
        self.dawe_socket = create_connection("wss://" + DAWE_URL)
        self.dawe_socket.settimeout(1)
        self.lol_ui_socket = create_connection(WS_SERVER + str(port) + "/" + self.path_key)
        self.dawe_socket.send('{"type":"joinroom","roomId":"'+ self.dawe_game +'"}')
        pass
    def init(self ):

        while True:
            print("alive")
            try:
                dawe_data = json.loads(self.dawe_socket.recv())['newState']
                if dawe_data['state'] == 'ongoing' and self.status.state == 'starting':
                    self.start_game()

                if dawe_data['state'] == 'ongoing':
                    self.update_game(dawe_data)

                elif dawe_data['state'] == 'finished':
                    self.update_game(dawe_data)
                    
            except WebSocketTimeoutException:
                try:
                    if self.status.state == 'ongoing':
                        self.send_time()
                    else: 
                        self.lol_ui_socket.send(MyJSONEncoder().encode(Message(self.status)))
                except ConnectionAbortedError:
                    print("error")
                    pass
                    

    def send_time(self):
        self.status.timer -= 1
        self.lol_ui_socket.send(MyJSONEncoder().encode(Message(self.status)))

    def update_game(self, dawe_data: dict):

        self.status.state = convert_turn_to_state(dawe_data['turn'])
        self.status.blueTeam.bans= [ Ban(Champion(name, self.game_version), False) for name in dawe_data["blueBans"] ]
        self.status.redTeam.bans= [ Ban(Champion(name, self.game_version), False) for name in dawe_data["redBans"] ]
        self.status.blueTeam.picks= [Pick(Champion(dawe_data["bluePicks"][i], self.game_version), i, self.blueTeam[i], False)  for i in range(0, len(dawe_data["bluePicks"]))]
        # self.status.blueTeam.picks= [Pick(Champion(dawe_data["bluePicks"][i], self.game_versio), i, teams[status.config["frontend"]["blueTeam"]["name"]][i], False)  for i in range(0, len(dawe_data["bluePicks"]))]
        self.status.redTeam.picks= [Pick(Champion(dawe_data["redPicks"][i], self.game_version), i, self.redTeam[i], False) for i in range(0, len(dawe_data["redPicks"]))]
        self.status.timer = int(dawe_data["nextTimeout"]/1000)

        self.set_active(dawe_data["nextTeam"],  dawe_data["nextType"])

        self.lol_ui_socket.send(MyJSONEncoder().encode(Message(self.status)))

    def set_active(self, currentTeam: str, currentType: str):
        self.unset_active()
        if currentTeam == 'red':
            self.set_champ_active(self.status.redTeam, currentType)
        elif currentTeam == 'blue':
            self.set_champ_active(self.status.blueTeam, currentType)
        else:
            self.status.state = ""
            self.status.timer = ""

    def unset_active (self):
        self.status.blueTeam.isActive = False
        self.status.redTeam.isActive = False
        for pick in self.status.blueTeam.picks + self.status.redTeam.picks:
            pick.isActive = False
        for ban in self.status.blueTeam.bans + self.status.redTeam.bans:
            ban.isActive = False
        
    def set_champ_active(self, team: Team, actionType: str):
        team.isActive = True
        if actionType == 'pick':
            team.picks[len(team.picks) - 1].isActive = True
        elif actionType == 'ban':
            team.bans[len(team.bans) - 1].isActive = True

    def start_game(self):
        self.lol_ui_socket.send('{"eventType":"champSelectStarted"}')
        self.lol_ui_socket.send(MyJSONEncoder().encode(Message(self.status)))

    def status_start(self):
        config = self.config
        self.status = State(blueTeam = Team([],[],False), redTeam= Team([],[], False), version=self.game_version, time=30, state="starting", config=config)
