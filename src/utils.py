def convert_turn_to_state(turn: int) -> str:
    if turn < 6:
        return 'BAN PHASE 1'
    elif turn < 12:
        return 'PICK PHASE 1'
    elif turn < 16:
        return 'BAN PHASE 2'
    elif turn < 20: return 'PICK PHASE 2'
    else: return 'ended' 

from models import RegisteredTeam

def construct_config(user: str, game_version: str, blue_team: RegisteredTeam, 
red_team:RegisteredTeam, tournament_logo) -> dict:
    return {
        "frontend": {
            "scoreEnabled": True,
            "spellsEnabled": False,
            "coachesEnabled": True,
            "redTeam": {
                "name": red_team.name,
                "score": red_team.score,
                "coach":red_team.coach,
                "color": "rgb(222,40,70)",
                "logo": user+"/" +red_team.logo
            },
            "blueTeam": {
                "name": blue_team.name,
                "score": blue_team.score,
                "coach":  blue_team.coach,
                "color": "rgb(0,151,196)",
                "logo": user+"/" +blue_team.logo
            },
            "patch": game_version,
            "tournament": user+"/" +tournament_logo
        },
        "contentPatch": "latest",
        "contentCdn": "https://ddragon.leagueoflegends.com/cdn"
        }

