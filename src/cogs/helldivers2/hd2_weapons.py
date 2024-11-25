"""
known weapons in game by id
"""

weapons = {
    0: 'any',
    1978117092: "Stalwart",
    934703916: "Machine Gun",
    4038802832: "Heavy Machine Gun",
}

def get_weapon(id:int) -> str:
    if id in weapons:
        return weapons[id]
    else:
        return None