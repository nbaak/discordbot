
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
    LIBERTAE_MORE_PLANETS_THAN_LOST = 15


def mo_task_paramerts(task) -> dict:
    """
    @return faction_id, target_id, libertation_needed, planet_id, unit_type_id
    """
    task_out = {}
    for value, value_type in zip(task['values'], task['valueTypes']):
        if value_type == MOTaskTypes.NONE:
            continue            
        elif value_type == MOTaskTypes.FACTION:
            task_out[MOTaskTypes.FACTION] = value
            continue
        elif value_type == MOTaskTypes.TARGET_COUNT:
            task_out[MOTaskTypes.TARGET_COUNT] = value
            continue
        elif value_type == MOTaskTypes.UNIT_TYPE:
            task_out[MOTaskTypes.UNIT_TYPE] = value
            continue
        elif value_type == MOTaskTypes.LIBERATION_NEEDED:
            task_out[MOTaskTypes.LIBERATION_NEEDED] = value
            continue
        elif value_type == MOTaskTypes.PLANET:
            task_out[MOTaskTypes.PLANET] = value
            continue
        else:
            continue
        
    return task_out


def test():
    print(13 == MOMissionTypes.HOLD_PLANET)
    
    
if __name__ == "__main__":
    test()
