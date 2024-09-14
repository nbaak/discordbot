"""
a list of known enemies by id
"""

enemy_units = {
    0: 'any', 
    2514244534: 'Bile Titan',
    1379865898: 'Bile Spewer',
    2058088313: 'Warrior'
}

def get_enemy(id:int) -> str:
    if id in enemy_units:
        return enemy_units[id]
    else:
        return None