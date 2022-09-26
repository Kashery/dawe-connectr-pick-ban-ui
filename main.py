from distutils.command.config import config
from models import *
import json
from websocket import create_connection, WebSocket, WebSocketTimeoutException
from utils import convert_turn_to_state
from server import run_server

teams = json.loads(open('teams.json', 'r').read())
DAWE_URL = "draftlol.dawe.gg"
PORT = "8998"
WS_SERVER = "ws://localhost:" + PORT

GAME_VERSION = "12.18.1"
DAWE_ID = "1bLGkT7S"

def init():
    status = status_start()
    dawe_socket = create_connection("wss://" + DAWE_URL)
    dawe_socket.settimeout(1)
    lol_ui_socket = create_connection(WS_SERVER)
    dawe_socket.send('{"type":"joinroom","roomId":"'+ DAWE_ID +'"}')
    while True:
        print("alive")
        try:
            dawe_data = json.loads(dawe_socket.recv())['newState']
            if dawe_data['state'] == 'ongoing' and status.state == 'starting':
                start_game(lol_ui_socket, status)

            if dawe_data['state'] == 'ongoing':
                update_game(lol_ui_socket, status, dawe_data)

            elif dawe_data['state'] == 'finished':
                update_game(lol_ui_socket, status, dawe_data)
                exit()
        except WebSocketTimeoutException:
            if status.state != 'starting':
                send_time(lol_ui_socket, status)

def send_time(socket:WebSocket, status: State):
    status.timer -= 1
    socket.send(MyJSONEncoder().encode(Message(status)))

def update_game(socket:WebSocket, status: State, dawe_data: dict):

    status.state = convert_turn_to_state(dawe_data['turn'])
    status.blueTeam.bans= [ Ban(Champion(name, GAME_VERSION), False) for name in dawe_data["blueBans"] ]
    status.redTeam.bans= [ Ban(Champion(name, GAME_VERSION), False) for name in dawe_data["redBans"] ]
    status.blueTeam.picks= [Pick(Champion(dawe_data["bluePicks"][i], GAME_VERSION), i, teams[status.config["frontend"]["blueTeam"]["name"]][i], False)  for i in range(0, len(dawe_data["bluePicks"]))]
    status.redTeam.picks= [Pick(Champion(dawe_data["redPicks"][i], GAME_VERSION), i, teams[status.config["frontend"]["redTeam"]["name"]][i], False) for i in range(0, len(dawe_data["redPicks"]))]
    status.timer = int(dawe_data["nextTimeout"]/1000)

    set_active(status,  dawe_data["nextTeam"],  dawe_data["nextType"])

    socket.send(MyJSONEncoder().encode(Message(status)))

def set_active(status: State, currentTeam: str, currentType: str):
    unset_active(status)
    if currentTeam == 'red':
        set_champ_active(status.redTeam, currentType)
    elif currentTeam == 'blue':
        set_champ_active(status.blueTeam, currentType)
    else:
        status.state = ""
        status.timer = ""

def unset_active (status: State):
    status.blueTeam.isActive = False
    status.redTeam.isActive = False
    for pick in status.blueTeam.picks + status.redTeam.picks:
        pick.isActive = False
    for ban in status.blueTeam.bans + status.redTeam.bans:
        ban.isActive = False
    
def set_champ_active(team: Team, actionType: str):
    team.isActive = True
    if actionType == 'pick':
        team.picks[len(team.picks) - 1].isActive = True
    elif actionType == 'ban':
        team.bans[len(team.bans) - 1].isActive = True

def start_game(socket: WebSocket, status: State):
    socket.send('{"eventType":"champSelectStarted"}')
    socket.send(MyJSONEncoder().encode(Message(status)))

def status_start():
    config = json.loads(open('front-config.json', 'r').read())
    status = State(blueTeam = Team([],[],False), redTeam= Team([],[], False), version=GAME_VERSION, time=30, state="starting", config=config)
    return status


import multiprocessing
if __name__ == '__main__':
    pr = multiprocessing.Process(target = run_server, args=(PORT,) )
    pr.start()
    print("SATRTING")
    init()