def convert_turn_to_state(turn: int) -> str:
    if turn < 6:
        return 'BAN PHASE 1'
    elif turn < 12:
        return 'PICK PHASE 1'
    elif turn < 16:
        return 'BAN PHASE 2'
    elif turn < 20: return 'PICK PHASE 2'
    else: return 'ended' 