from cogs.helldivers2 import api
import pickle
import datetime
import time


class HD2DataService():
    
    def __init__(self):
        self.war_status = None
        self.war_info = None
        self.news = None
        self.campaign = None
        self.planet_index = None
        self.major_order = None
        self.planets = api.planets()
        
        self.update_all()
        
    def update_major_order(self):
        self.major_order = api.get_major_order()
        
    def update_campaign(self):
        new_campaign = api.get_campaign()
        if new_campaign:
            self.campaign = new_campaign
        
    def update_war_status(self):
        new_war_status = api.get_war_status()
        if new_war_status:
            self.war_status = new_war_status
        
    def update_war_info(self):
        new_war_inf0 = api.get_war_info()
        if new_war_inf0:
            self.war_info = new_war_inf0
        
    def update_all(self):
        self.update_campaign()
        self.update_major_order()
        self.update_war_status()
        # self.update_war_info()
        
    def find_in_campain_dict(self, search_key, search_value:str) -> dict:
        
        for planet in self.campaign:
            for k, v in planet.items():
                if k == search_key and v == search_value:
                    return planet
        
        return None
    
    def get_faction_for_planet(self, planet_id:int) -> str:
        owner = self.war_status["planetStatus"][planet_id]["owner"]
        factions = {1: "🌎", 2: "🪲", 3: "🤖"}
        
        return factions[owner] if owner in factions else "?" 
    
    def mo_progress(self, major_order:dict):
        progress = major_order['progress']
        tasks = major_order['setting']['tasks']
        planets = [self.planets[str(task['values'][2])]['name'] for task in tasks]
        planet_ids = [task['values'][2] for task in tasks]
        
        text = f"{major_order['setting']['taskDescription']}\n"
        for planet_name, prog, planet_id in list(zip(planets, progress, planet_ids)):
            
            if prog:
                progress = prog * 100
            else:
                planet = self.find_in_campain_dict('planetIndex', planet_id)
                progress = planet['percentage'] if planet else 0
            
            owner = self.get_faction_for_planet(planet_id)
            text += f"{owner} {planet_name}: {progress:3.2f}%\n"
        
        return text
    
    def mo_time_remaining(self, major_order:dict=None) -> str:
        major_order = major_order or self.major_order[0]
        remaining = int(major_order['expiresIn'])
        delta = datetime.timedelta(seconds=remaining)
        return delta
        
    def get_major_order(self):
        if self.major_order:
            mo = self.major_order[0]
            expires = int(self.major_order[0]['expiresIn'])
            progress = self.mo_progress(mo)
            
            title = f"{self.major_order[0]['setting']['overrideTitle']}\n{self.major_order[0]['setting']['overrideBrief']}\n"
            text = f"{title}\n{progress}\n" 
            text += f"ends in {self.mo_time_remaining(mo)}"
            
            return text
        
        else:
            return f"MAJOR ORDER\nNo Major Order active!"
        
    def get_campaign(self):
        if self.campaign:
            text = "War Campaign:\n"
            
            for entry in sorted(self.campaign, key=lambda c: c['players'], reverse=True):
                owner = self.get_faction_for_planet(entry['planetIndex'])
                defense = "🛡️" if entry['defense'] else "⚔️"
                percentage = float(entry['percentage'])
                text += f"{owner} {entry['name']} {defense}: liberation: {percentage:3.2f}%, active Helldivers: {entry['players']}\n"
            
            helldivers_online_total = sum([planet['players'] for planet in self.campaign])
            text += f"\nHelldivers active: {helldivers_online_total}"
                
            return text
            

def main():
    data = HD2DataService()
    data.update_all()
    # for k, v in data.major_order[0].items():
    #     if type(v) == dict:
    #         for kk, vv in v.items():
    #             print(f'  {kk} {vv}')
    #     print(k, v)
        
    print(data.get_major_order())
    print(data.get_campaign())    


if __name__ == "__main__":
    main()
