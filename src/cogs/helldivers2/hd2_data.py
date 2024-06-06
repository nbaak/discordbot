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
        
        self.load_all()
        self.update_all()
        
    def update_major_order(self) -> bool:
        mo_data = api.get_major_order()
        new_mo = False
        if not self.major_order or mo_data[0]['id32'] != self.major_order[0]['id32']:
            new_mo = True
            
        self.major_order = mo_data
        
        return new_mo
        
    def update_campaign(self):
        self.campaign = api.get_campaign()
        
    def update_war_status(self):
        self.war_status = api.get_war_status()
        
    def update_war_info(self):
        self.war_info = api.get_war_info()
        
    def update_all(self):
        self.update_campaign()
        self.update_major_order()
        # self.update_war_info()
        # self.update_war_status()
        
    def save_all(self):
        with open('hd2.bin', 'wb') as f:
            pickle.dump(self, f)
            
    def load_all(self):
        try:
            with open('hd2.bin', 'rb') as f:
                data = pickle.load(f)
                print(type(data))
                self.war_status = data.war_status
                self.war_info = data.war_info
                self.news = data.news
                self.campaign = data.campaign
                self.planet_index = data.planet_index
                self.major_order = data.major_order                
                
                return True
        except:
            print('no data file found')
            return False
        
    def find_ind_campain_dict(self, search_key, search_value:str) -> dict:
        
        for planet in self.campaign:
            for k, v in planet.items():
                if k == search_key and v == search_value:
                    return planet
        
        return None
    
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
                planet = self.find_ind_campain_dict('planetIndex', planet_id)
                progress = planet['percentage']
                
            text += f"{planet_name} {progress:3.2f}%\n"
        
        return text
    
    def mo_time_remaining(self, major_order:dict) -> str:
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
        
    def get_campaign(self):
        if self.campaign:
            text = "War Campaign:\n"
            
            for entry in sorted(self.campaign, key=lambda c: c['players'], reverse=True):
                defense = "🛡️" if entry['defense'] else "⚔️"
                percentage = float(entry['percentage'])
                text += f"{entry['name']} {defense}: liberation: {percentage:3.2f}, active Helldivers: {entry['players']}\n"
            
            helldivers_online_total = sum([planet['players'] for planet in self.campaign])
            text += f"\nHelldivers active: {helldivers_online_total}"
                
            return text
            

def main():
    data = HD2DataService()
    data.update_all()
    for k, v in data.major_order[0].items():
        if type(v) == dict:
            for kk, vv in v.items():
                print(f'  {kk} {vv}')
        print(k, v)

    print()        
    print(data.get_major_order())
    print(data.get_campaign())

    data.save_all()
    

if __name__ == "__main__":
    main()
