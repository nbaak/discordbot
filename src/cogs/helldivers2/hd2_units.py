"""
a list of known enemies by id
"""

enemy_units = {
    0: 'any', 
    2514244534: 'Bile Titan',
}

def get_enemy(id:int) -> str:
    if id in enemy_units:
        return enemy_units[id]
    else:
        return None