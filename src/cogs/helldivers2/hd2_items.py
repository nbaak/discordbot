"""
known items in game by id
"""

items = {
    0: 'any',
    934703916: "Machine Gun",
    1978117092: "Stalwart",
    
    2197477188: "Orbital Railcannon Strike",
    
    2985106497: "Rare",
    3992382197: "Common",
    
    4038802832: "Heavy Machine Gun",
}

def get_item(id:int) -> str:
    if id in items:
        return items[id]
    else:
        print(f"Unkown Item: {id}")
        return None