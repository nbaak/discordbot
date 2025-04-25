from cogs.helldivers2.hd2_units import get_enemy
from cogs.helldivers2.hd2_items import get_item
try:
    from cogs.helldivers2.hd2_data import HD2DataService
except:
    import importlib
    HD2DataService = importlib.import_module("cogs.helldivers2.hd2_data")

from enum import IntEnum


class MOTaskValueTypes(IntEnum):
    NONE = 0
    FACTION = 1
    TARGET_COUNT = 3
    UNIT_TYPE = 4
    ITEM = 5
    LIBERATION_NEEDED = 11
    PLANET = 12

    
class MOMissionTypes():
    EXTRACT_SAMPLES = 2
    KILL_ENEMIES = 3
    COMPLETE_OPERATIONS = 9
    ATTACK_PLANET = 11
    DEFENT_PLANET = 12
    HOLD_PLANET = 13
    LIBERTAE_MORE_PLANETS_THAN_LOST = 15

    
# register point fopr hd2 data service
hd2_data:HD2DataService = None

# mo valuze types as compact dict based on MOTaskValueTypes
# mo_task_value_types:dict = {v: k for k, v in vars(MOTaskValueTypes).items() if not k.startswith("__")}


def mo_task_paramerts(task:dict) -> dict:
    """
    @return faction_id, target_id, libertation_needed, planet_id, unit_type_id
    """
    task_out = {}
    for value, value_type in zip(task['values'], task['valueTypes']):
        if value_type in MOTaskValueTypes:
            task_out[value_type] = value
        
    return task_out


def mo_attack_planet(progress:int, task:dict) -> str:
    planet_id = task[MOTaskValueTypes.PLANET]
    planet_name = hd2_data.planets[planet_id]["name"]
    
    defense, percentage, faction, _, _ = hd2_data.planet_info(planet_id)
    
    if progress:
        defense_icon = "  "
        percentage = 100
        
    else:
        defense_icon = "🛡️" if defense else "⚔️"                
        
    holder_icon = hd2_data.faction_icon(faction)
        
    text = f"{holder_icon}{defense_icon} {planet_name}: {abs(percentage):3.2f}%\n"
    
    return text

    
def mo_defend_planet(progress:int, task:dict) -> str:
    # planet_id = task[MOTaskValueTypes.PLANET]
    target = task[MOTaskValueTypes.TARGET_COUNT]
    faction_id = task[MOTaskValueTypes.FACTION]
    # unit_type_id = task[MOTaskValueTypes.UNIT_TYPE]
    
    faction = hd2_data.target_faction(faction_id)
    text = f"Defend Planets against {faction}: {progress}/{target}\n"
    
    return text


def mo_kill_enemies(progress:int, task:dict) -> str: 
    # planet_id = task[MOTaskValueTypes.PLANET]
    target = task[MOTaskValueTypes.TARGET_COUNT]
    faction_id = task[MOTaskValueTypes.FACTION]
    unit_type_id = task[MOTaskValueTypes.UNIT_TYPE]
    weapon_type_id = task[MOTaskValueTypes.ITEM]
    
    progress_percent = progress / target * 100
    
    faction = hd2_data.target_faction(faction_id)        
    unit = f" ({get_enemy(unit_type_id)}s)" if unit_type_id else ""
    weapon = f" with {get_item(weapon_type_id)}" if weapon_type_id else ""
    icon = hd2_data.faction_icon(faction)
    
    return f"{icon}   {faction}{unit} killed{weapon} {progress:,}/{target:,} ({progress_percent:.2f}%)\n"


def mo_extract_samples(progress:int, task:dict) -> str:
    planet_id = task[MOTaskValueTypes.PLANET]
    target = task[MOTaskValueTypes.TARGET_COUNT]
    
    sample_type_id = task[MOTaskValueTypes.ITEM]
    sample_type = f"{get_item(sample_type_id)}" if sample_type_id else ""
            
    progress_percent = progress / target * 100
    
    return f"Extract {sample_type} Samples on {hd2_data.planets[planet_id]['name']}: {progress:,}/{target:,} ({progress_percent:.2f}%)\n"


def mo_hold_planet(progress:int, task:dict) -> str:
    planet_id = task[MOTaskValueTypes.PLANET]
    planet_name = hd2_data.planets[planet_id]["name"]
    
    defense, percentage, faction, _, _ = hd2_data.planet_info(planet_id)
        
    if progress:
        defense_icon = "  "
        percentage = 100
        faction = 0
        
    else:
        defense_icon = "🛡️" if defense else "⚔️" 
    
    holder_icon = hd2_data.faction_icon(faction)
    
    return f"{holder_icon}{defense_icon} {planet_name}: {abs(percentage):3.2f}%\n"


def mo_liberate_more_planets_than_lost(progress:int, task:dict) -> str:
    task_d = mo_task_paramerts(task)        
    return f"Liberate more Planets than Lost: {progress}\n"


def mo_complete_operations(c_progress:int, task:dict) -> str:
    target_count = task[MOTaskValueTypes.TARGET_COUNT]
    p_progress = c_progress / target_count  # percent
        
    return f"Win Operations: {c_progress}/{target_count} ({p_progress:.2}%)\n"


__mo_missions = {
    MOMissionTypes.EXTRACT_SAMPLES: mo_extract_samples,
    MOMissionTypes.KILL_ENEMIES: mo_kill_enemies,
    MOMissionTypes.COMPLETE_OPERATIONS: mo_complete_operations,
    MOMissionTypes.ATTACK_PLANET: mo_attack_planet,
    MOMissionTypes.DEFENT_PLANET: mo_defend_planet,
    MOMissionTypes.HOLD_PLANET: mo_hold_planet,
    MOMissionTypes.LIBERTAE_MORE_PLANETS_THAN_LOST: mo_liberate_more_planets_than_lost,
    }


def mission(mission_type:MOMissionTypes, progress:int, task:dict) -> str:
    if mission_type in __mo_missions:
        return __mo_missions[mission_type](progress, mo_task_paramerts(task))
    else:
        return f"unkown major order {mission_type}\n"


def test():
    print(13 == MOMissionTypes.HOLD_PLANET)
    print(3 in MOTaskValueTypes)
    
    
if __name__ == "__main__":
    test()
