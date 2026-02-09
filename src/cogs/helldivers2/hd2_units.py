"""
a list of known enemies by id
"""

enemy_units = {
    0: 'any',
    1764323819: 'One True Flag',
    
    # Bugs
    793026793: 'Shriekers',
    1046000873: 'Impalers',
    1299714559: 'Chargers',
    1379865898: 'Bile Spewer',
    1405979473: 'Harvester',
    2058088313: 'Warrior',
    2115960485: 'Spore Burst Warriors',
    2514244534: 'Bile Titan',
    3929716830: 'Hive Lord',
    
    # Automaton
    # 523260929: '?', # was in first at 2025-07-22
    1153658728: 'Factory Strider',
    2664856027: 'Shredder Tank',
    4039692928: 'Trooper',
    
    # Illuminate
    2880434041: 'Fleshmobs',
    3097344451: 'Leviathans',
    4211847317: 'Voteles',
}


def get_enemy(_id: int) -> str:
    if _id in enemy_units:
        return enemy_units[_id]
    else:
        print(f"unknown unit _id: {_id}")
        return _id
