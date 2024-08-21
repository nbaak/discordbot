
class MOTaskTypes():
    NONE = 0
    FACTION = 1
    TARGET_COUNT = 3
    UNIT_TYPE = 4
    LIBERATION_NEEDED = 11
    PLANET = 12

    
class MOMissionTypes():
    EXTRACT_SAMPLES = 2
    KILL_ENEMIES = 3
    ATTACK_PLANET = 11
    DEFENT_PLANET = 12
    HOLD_PLANET = 13


def mo_task_paramerts(task_in) -> tuple:
    """
    @return faction_id, target_id, libertation_needed, planet_id, unit_type_id
    """        
    task = task_in.copy()
    faction_id = target = liberation_needed = planet_id = unit_type = None

    for value, value_type in zip(task['values'], task['valueTypes']):
        if value_type == MOTaskTypes.NONE:
            continue            
        elif value_type == MOTaskTypes.FACTION:
            faction_id = value
            continue
        elif value_type == MOTaskTypes.TARGET_COUNT:
            target = value
            continue
        elif value_type == MOTaskTypes.UNIT_TYPE:
            unit_type = value
            continue
        elif value_type == MOTaskTypes.LIBERATION_NEEDED:
            liberation_needed = value
            continue
        elif value_type == MOTaskTypes.PLANET:
            planet_id = value
            continue
        else:
            continue
        
    return faction_id, target, liberation_needed, planet_id, unit_type


def test():
    print(13 == MOMissionTypes.HOLD_PLANET)
    
    
if __name__ == "__main__":
    test()
