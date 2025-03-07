"""
a list of known enemies by id
"""

enemy_units = {
    0: 'any', 
    1379865898: 'Bile Spewer',
    1405979473: 'Harvester',
    2058088313: 'Warrior',
    2514244534: 'Bile Titan',
    2664856027: 'Shredder Tank',
    4211847317: 'Voteles',
}

def get_enemy(id:int) -> str:
    if id in enemy_units:
        return enemy_units[id]
    else:
        print(f"unknown unit id: {id}")
        return None