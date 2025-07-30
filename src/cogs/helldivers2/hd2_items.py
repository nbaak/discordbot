"""
known items in game by id
"""

items = {
    0: 'any',
    1978117092: "Stalwart",
    934703916: "Machine Gun",
    4038802832: "Heavy Machine Gun",
    3992382197: "Common",
    2985106497: "Rare",
}

def get_item(id:int) -> str:
    if id in items:
        return items[id]
    else:
        return None