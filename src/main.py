from models import *
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
import multiprocessing
import uvicorn
from dawe import DaweDraft
from fastapi.staticfiles import StaticFiles
import threading

    

PORT = "4557"
GAME_VERSION = "12.18.1"
DAWE_ID = "uxcmm8aQ"
app = FastAPI()
active_games : dict[str, (threading.Thread, threading.Event)] = {}
ws_manager = {}
lock = threading.Lock()

@app.on_event("shutdown")
def shutdown_event():
    for game in active_games.values():
        print(game)
        if game[0].is_alive():
            game[1].set()
            game[0].join()


app.mount("/cache", StaticFiles(directory="./cache"), name="cache")

@app.websocket("/ws/{nameKey}")
async def websocket_end(websocket:WebSocket, nameKey: str):
    if nameKey not in ws_manager:
        ws_manager[nameKey] = ConnectionManager()

    await  ws_manager[nameKey].connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        
        ws_manager[nameKey].disconnect(websocket)

@app.put("/{nameKey}")
async def create_dawe_game(nameKey: str, match_data: Match, background_tasks: BackgroundTasks):

    if nameKey in active_games and active_games[nameKey][0].is_alive():
        print(active_games[nameKey])
        active_games[nameKey][1].set()
        active_games[nameKey][0].join()

    event = multiprocessing.Event()
    
    thread = threading.Thread(target = dawe_game, args= (nameKey, match_data.dawe_id, PORT, match_data.game_version, match_data.blue_players, match_data.red_players, match_data.game_config, ))
    active_games[nameKey] = (thread, event)
    thread.start()
    
    


def dawe_game(nameKey, dawe_id, PORT, game_version, blue_players, red_players, game_config):
    if nameKey not in ws_manager:
        ws_manager[nameKey] = ConnectionManager()
    DaweDraft(nameKey, dawe_id, PORT, game_version, blue_players, red_players, game_config, ws_manager[nameKey],active_games[nameKey][1]).init()

if __name__ == '__main__':

    uvicorn.run("main:app",host='0.0.0.0', port=4557, reload=False, debug=True, workers=5)

