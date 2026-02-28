from cogs.helldivers2.hd2_units import get_enemy
from cogs.helldivers2.hd2_items import get_item
from pip._vendor.pygments.unistring import No
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
    # LIBERATION_NEEDED = 11 # it seems that I understood this flag wrong, maybe mission scope? 1:planet, 2:sector...
    PLANET = 12


class MOMissionTypes():
    EXTRACT_SAMPLES = 2
    KILL_ENEMIES = 3
    EXTRACT_SUCCESSFUL_MISSION = 7
    COMPLETE_OPERATIONS = 9
    ATTACK_PLANET = 11
    DEFENT_PLANET = 12
    CONQUER_HOLD_PLANET = 13
    EXPAND = 15


# register point for hd2 data service
hd2_data:HD2DataService = None


class MOTask():
    
    def __init__(self, task:dict) -> None:
        self.target = task.get(MOTaskValueTypes.TARGET_COUNT, None)
        
        self.faction_id = task.get(MOTaskValueTypes.FACTION, None)
        self.faction = hd2_data.target_faction(self.faction_id) if self.faction_id else None
        
        self.unit_type_id = task.get(MOTaskValueTypes.UNIT_TYPE, None)
        self.unit = f" ({get_enemy(self.unit_type_id)})" if self.unit_type_id else ""
        
        self.item_id = task.get(MOTaskValueTypes.ITEM, None)
        self.item = get_item(self.item_id) if self.item_id else ""
        
        self.planet_id = task.get(MOTaskValueTypes.PLANET, None)
        if self.planet_id:
            self.planet = hd2_data.planets[self.planet_id]
            self.planet_name = self.planet["name"]
        else:
            self.planet = None
            self.planet_name = None


def mo_task_paramerts(task:dict) -> dict:
    """
    @return faction_id, target_id, libertation_needed, planet_id, unit_type_id
    """
    task_out = {}
    for value, value_type in zip(task['values'], task['valueTypes']):
        if value_type in MOTaskValueTypes:
            task_out[value_type] = value

    return task_out


def mo_attack_planet(progress:int, task:MOTask) -> str:
    planet_id = task.planet_id
    planet_name = task.planet_name

    defense, percentage, faction, _, _ = hd2_data.planet_info(planet_id)

    if progress:
        defense_icon = "  "
        percentage = 100

    else:
        defense_icon = "🛡️" if defense else "⚔️"

    holder_icon = hd2_data.faction_icon(faction)

    return f"{holder_icon}{defense_icon} {planet_name}: {abs(percentage):3.2f}%\n"


def mo_defend_planet(progress:int, task:MOTask) -> str:
    target = task.target
    faction = task.faction

    return f"Defend Planets against {faction}: {progress}/{target}\n"


def mo_kill_enemies(progress:int, task:MOTask) -> str:
    target = task.target
    faction_id = task.faction_id
    unit_type_id = task.unit_type_id
    weapon_type_id = task.item_id
    planet_id = task.planet_id
    
    if planet_id > 0:
        planet_name = hd2_data.planets[planet_id]["name"]
    else:
        planet_name = ""

    progress_percent = progress / target * 100

    faction = hd2_data.target_faction(faction_id)
    unit = f" ({get_enemy(unit_type_id)})" if unit_type_id else ""
    with_weapon = f" with {get_item(weapon_type_id)}" if weapon_type_id else ""
    icon = hd2_data.faction_icon(faction)
    on_planet = f" on {planet_name}" if planet_name else ""
    
    return f"{icon} {faction}{unit}{on_planet} killed{with_weapon} {progress:,}/{target:,} ({progress_percent:.2f}%)\n"


def mo_extract_successful_mission(progress:int, task:MOTask) -> str:
    target = task.target
    progress_percent = progress / target * 100

    faction_id = task.faction_id
    against = ""
    if faction_id != 0:
        faction = hd2_data.target_faction(faction_id)
        against = f" against {faction}"
        
    planet_id = task.planet_id
    if planet_id > 0:
        planet_name = f" on {hd2_data.planets[planet_id]['name']}"
    else:
        planet_name = ""

    return f"Extract from a successful mission{against}{planet_name} {progress}/{target} ({progress_percent:.2f}%)\n"


def mo_extract_samples(progress:int, task:MOTask) -> str:
    faction_id = task.faction_id
    planet_id = task.planet_id
    target = task.target

    sample_type_id = task.item_idm
    sample_type = f"{get_item(sample_type_id)}" if sample_type_id else ""

    progress_percent = progress / target * 100

    if faction_id:
        faction = hd2_data.target_faction(faction_id)
        return f"Extract {sample_type} Samples from any {faction} controlled planet: {progress:,}/{target:,} ({progress_percent:.2f}%)\n"

    planet = hd2_data.planets[planet_id]['name']
    return f"Extract {sample_type} Samples on {planet}: {progress:,}/{target:,} ({progress_percent:.2f}%)\n"


def mo_conquer_and_hold_planet(progress:int, task:MOTask) -> str:
    planet_id = task.planet_id
    planet_name = task.planet_name

    defense, percentage, faction, _, _ = hd2_data.planet_info(planet_id)
    
    if faction == "Humans":
        progress = 1
    
    if progress:
        defense_icon = "  "
        percentage = 100
        faction = 0
    
    else:
        defense_icon = "🛡️" if defense else "⚔️"

    holder_icon = hd2_data.faction_icon(faction)
    
    hold_or_conquer = ""
    if percentage == 100:
        hold_or_conquer = f"- Hold until Major order complete!"
    else:
        hold_or_conquer = f"- Conquer until Major order complete!"

    return f"{holder_icon}{defense_icon} {planet_name} {abs(percentage):3.2f}% {hold_or_conquer}\n"


def mo_expand(progress:int, _) -> str:
    return f"Liberate more Planets than Lost: {progress}\n"


def mo_complete_operations(c_progress:int, task:MOTask) -> str:
    target_count = task.target
    p_progress = c_progress / target_count * 100  # percent

    faction = task.faction
    against = f"against {faction}"

    return f"Win Operations {against}: {c_progress}/{target_count} ({p_progress:.2f}%)\n"


def mo_liberate_designated_planets(progress:int, task:MOTask) -> str:
    print(progress)
    print(task)


__mo_missions = {
    MOMissionTypes.EXTRACT_SAMPLES: mo_extract_samples,
    MOMissionTypes.KILL_ENEMIES: mo_kill_enemies,
    MOMissionTypes.EXTRACT_SUCCESSFUL_MISSION: mo_extract_successful_mission,
    MOMissionTypes.COMPLETE_OPERATIONS: mo_complete_operations,
    MOMissionTypes.ATTACK_PLANET: mo_attack_planet,
    MOMissionTypes.DEFENT_PLANET: mo_defend_planet,
    MOMissionTypes.CONQUER_HOLD_PLANET: mo_conquer_and_hold_planet,
    MOMissionTypes.EXPAND: mo_expand,
    }


def mission(mission_type:MOMissionTypes, progress:int, task:dict) -> str:
    if mission_type in __mo_missions:
        # print(mission_type, progress)
        task = MOTask(mo_task_paramerts(task))
        
        return __mo_missions[mission_type](progress, task)
    else:
        return f"unkown major order {mission_type}\n"


def test():
    hd2_data = HD2DataService()
    mo_body = hd2_data.get_major_order()
    
    print(mo_body)


if __name__ == "__main__":
    test()
