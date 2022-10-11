# dawe-connector pick-ban-ui

> Based on [lol-pick-ban-ui project](https://github.com/RCVolus/lol-pick-ban-ui) from @RCVolus (Riot Community)

> This module connects in real time the information from [draftlol.dawe.gg](https://draftlol.dawe.gg/) to a cool UI allowing you to show the picks&bans phase differently.




## Usage
### Requirements
- Install [Docker](https://www.docker.com/)
- Install [Postman](https://www.postman.com/) or similar to send POST requests

### Steps
- Execute `docker compose up -d` to run all the services.
- Add the logos from teams and tournaments under the folder:
```
📦cache
 ┗ 📂logos
   ┗ 📂PROFILE_NAME
     ┣ 📜logo1.png
     ┗ 📜logo2.png
```
- Download the DataDragon data from the current patch and add it on
```
📦cache
   📂PATCH NUMBER
   ┣ 📂champion
   ┃ ┣ 📜CHAMPION_centered_splash.jpg
   ┃ ┣ 📜CHAMPION_loading.jpg
   ┃ ┣ 📜CHAMPION_splash.jpg
   ┃ ┗ 📜CHAMPION_square.png
   ┗ 📂spell
     ┗ 📜SPELLS IMAGES
```
- Using postman or a similar tool, send a `PUT` request to `http://localhost/api/PROFILE_NAME
```
{
    "dawe_id": "DAWE GAME ID",
    "game_version": "MATCH ID",
    "blue_team": {
        "name": "BLUE TEAM ID",
        "logo": "BLUE TEAM LOGO FILE",
        "score": 1,
        "coach": "BLUE TEAM COACH",
        "players": [
            "BLUE TEAM TOPLANER",
            "BLUE TEAM JUNGLER",
            "BLUE TEAM MIDLANER",
            "BLUE TEAM ADC",
            "BLUE TEAM SUPPORT"
        ]
    },
    "red_team": {
        "name": "RED TEAM ID",
        "logo": "RED TEAM LOGO FILE",
        "score": 1,
        "coach": "RED TEAM COACH",
        "players": [
            "RED TEAM TOPLANER",
            "RED TEAM JUNGLER",
            "RED TEAM MIDLANER",
            "RED TEAM ADC",
            "RED TEAM SUPPORT"
        ]
    },
    "tournament_logo":"TOURNAMENT LOGO"
}
```
- Open `http://localhost/view/PROFILE_NAME`. The dawe draft should appear.

## Dev & Contributions
### Frontend Development
Check [lol-pick-ban-ui project](https://github.com/RCVolus/lol-pick-ban-ui) from @RCVolus or our [own fork](https://github.com/GFWard-Developers/lol-pick-ban-ui)
### Requirements
- Linux (or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install))
- Python 3.10.6
- Docker (to deploy the frontend)
- Python-venv (recommended)
### How to execute
- Use Docker to run the compiled frontend with an NGINX to reroute the WS traffic propertly:
`docker compose up web` 

- Install the required python packages: `python -m pip install -r requirements.txt`

- Run `./src/main.py`

