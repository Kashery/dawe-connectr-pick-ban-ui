from models import *
import json
from fastapi import FastAPI
import multiprocessing
import uvicorn
from server import run_server
from dawe import DaweDraft

active_games = {}

PORT = "8998"
GAME_VERSION = "12.18.1"
DAWE_ID = "1bLGkT7S"
app = FastAPI()

@app.get("/test")
def test():
    return "hola"

@app.put("/match/{nameKey}")
async def create_dawe_game(nameKey: str, match_data: Match):
    if nameKey in active_games:
        active_games[nameKey].kill()
        active_games[nameKey].join()
    active_games[nameKey] = multiprocessing.Process(target= dawe_game, args=(nameKey, match_data.dawe_id, PORT, match_data.game_version, match_data.blue_players, match_data.red_players, match_data.game_config, ))
    active_games[nameKey].start()

def dawe_game(nameKey, dawe_id, PORT, game_version, blue_players, red_players, game_config):
    DaweDraft(nameKey, dawe_id, PORT, game_version, blue_players, red_players, game_config).init()

if __name__ == '__main__':
    pr = multiprocessing.Process(target = run_server, args=(PORT,) )
    pr.start()
    print("SATRTING")
    uvicorn.run("main:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)

