from cogs.helldivers2 import api
import datetime
from typing import Union, Dict, List, Tuple
from cogs.helldivers2.hd2_tools import convert_to_datetime, get_recent_messages, \
    delta_to_now, formatted_delta


class HD2DataService():
    
    def __init__(self):
        self.war: Union[Dict, None] = None
        self.war_statistics: Union[Dict, None] = None
        self.news: Union[Dict, None] = None
        self.campaign: Union[List[Dict], None] = None
        self.planet_index: Union[Dict, None] = None
        self.major_order: Union[Dict, None] = None
        self.planets: Dict = api.planets()
        self.news: List = []
        
        self.update_all()
        
    def update_dispatch(self):
        new_dispatch = api.dispatch()
        self.news = []
        for news in new_dispatch:
            published_int = convert_to_datetime(news['published'])
            news['published'] = published_int
            self.news.append(news)  
        
    def update_major_order(self):
        self.major_order = api.get_major_order()
        
    def update_campaign(self):
        new_campaign = api.get_campaign()
        if new_campaign:
            self.campaign = new_campaign
        
    def update_war(self):
        new_war_data = api.get_war()
        if new_war_data:
            self.war = new_war_data
    
    def update_war_statistics(self):
        new_war_data = api.get_war_statistics()
        if new_war_data:
            self.war_statistics = new_war_data
        
    def update_all(self):
        self.update_campaign()
        self.update_major_order()
        self.update_war()
        self.update_war_statistics()
        self.update_dispatch()
        
    def find_in_campaign_dict(self, search_key, search_value:str) -> Union[Dict, None]: 
        for planet in self.campaign:
            for k, v in planet.items():
                if k == search_key and v == search_value:
                    return planet        
        return None
    
    def get_faction_for_planet(self, planet_id:int) -> Tuple[int, str]:
        try:
            owner_id:int = self.planet_index[planet_id]["currentOwner"]
            icon:str = self.faction_icon(owner_id)
            return owner_id, icon
        except KeyError:
            return 0, "?"
    
    def faction_icon(self, faction:Union[int, str]) -> str:
        if isinstance(faction, int):
            factions = {0: "🌎", 1: "🪲", 2: "🤖", 3: "🦑"}
        else:
            factions = {"Humans": "🌎", "Terminids": "🪲", "Automatons": "🤖", "Illuminates": "🦑"}
        
        return factions[faction] if faction in factions else "?"
    
    def faction_name(self, faction_id:int) -> str:
        # factions = {0: "Humans", 1: "Terminids", 2: "Automatons", 3: "Illuminates"}
        factions = self.war_statistics['factions']
        return factions[faction_id]
    
    def mo_attack_planets(self, progress, task) -> str:
        planet_name = self.planets[str(task['values'][2])]['name']
        planet_id = task['values'][2]
        prog = progress
            
        planet = self.find_in_campaign_dict('planetIndex', planet_id)
        
        if planet:
            # part of campaign (attack of defense)
            progress = planet['percentage']
            defense = "🛡️" if planet['defense'] else "⚔️"
            holder_icon = self.faction_icon(planet['faction'])
        else:
            # not part of campaign
            current_owner, holder_icon = self.get_faction_for_planet(planet_id)
            progress = 100 if current_owner == 1 else prog * 100
            defense = ""            
        
        # print(planet_name, planet, prog)                
            
        text = f"{holder_icon}{defense} {planet_name}: {abs(progress):3.2f}%\n"
        return text
    
    def mo_kill_enemies(self, progress:int, task:dict) -> str:
        target = task['values'][2]
        progress_percent = progress / target * 100
        faction = self.faction_name(task['values'][1])  # I hope that 1 is the targeted faction.. atm it works..
        
        return f"{faction} killed {progress:,}/{target:,} ({progress_percent:.2f}%)\n"
    
    def mo_progress(self, major_order:dict) -> str:
        progress = major_order['progress']
        tasks = major_order['setting']['tasks']
        text = f"{major_order['setting']['taskDescription']}\n"
        
        for task, prog in zip(tasks, progress):
            if task['type'] == 3:
                text += self.mo_kill_enemies(prog, task)
            elif task['type'] == 11: 
                text += self.mo_attack_planets(prog, task)
        
        return text
    
    def mo_time_remaining(self, major_order:dict=None) -> str:
        if major_order:
            major_order = major_order
        elif major_order == None and self.major_order:
            major_order = self.major_order[0]
        else:
            major_order = None
            
        if major_order: 
            remaining = int(major_order['expiresIn'])
            delta = datetime.timedelta(seconds=remaining)
            return formatted_delta(delta)
        else:
            return '---'
        
    def get_major_order(self) -> str:
        if self.major_order:
            mo = self.major_order[0]
            progress = self.mo_progress(mo)
            
            title = f"{self.major_order[0]['setting']['overrideTitle']}\n{self.major_order[0]['setting']['overrideBrief']}\n"
            text = f"{title}\n{progress}\n" 
            text += f"ends in {self.mo_time_remaining(mo)}"
            
            return text
        
        else:
            return f"MAJOR ORDER\nNo Major Order active!"
    
    def get_current_onlie_players(self):
        return self.war_statistics['statistics']['playerCount'] if self.war_statistics else 0
        
    def get_campaign(self) -> str:
        if self.campaign:
            text = "War Campaign:\n"
            
            for campaing_object in sorted(self.campaign, key=lambda c: c['planet']['statistics']['playerCount'], reverse=True):
                planet = campaing_object['planet']
                defense = True if planet['event'] else False 
                defence_icon = "🛡️" if defense else "⚔️"
                player_count = planet['statistics']['playerCount']

                remaining_time = ""
                
                if defense:
                    percentage = planet['event']['health'] / planet['event']['maxHealth'] * 100 
                    faction = self.faction_icon(planet['event']['faction'])
                    event_end_time = planet['event']['endTime']
                    
                    timestamp = convert_to_datetime(event_end_time)
                    delta = delta_to_now(timestamp)
                    event_end_time = formatted_delta(delta)
                    remaining_time = f" ({str(event_end_time)})"
                    
                else:
                    percentage = planet['health'] / planet['maxHealth'] * 100
                    faction = self.faction_icon(planet['currentOwner'])
                    event_end_time = None
                    
                text += f"{faction}{defence_icon} {planet['name']}{remaining_time}: liberation: {percentage:3.2f}%, active Helldivers: {player_count}\n"
            
            helldivers_online_total = self.get_current_onlie_players()
            text += f"\nHelldivers active: {helldivers_online_total}"
                
            return text
        else:
            return f"No campaign data available."
        
    def get_news(self, days=1):
        if self.news:
            entries = get_recent_messages(self.news, days) 
            message = "NEWS:\n"
            for e_msg in entries:
                message += e_msg + "\n"
                
            return message
                
        else:
            return "No News!"
            

def main():
    data = HD2DataService()
        
    print(data.get_major_order())
    print(data.get_campaign())
    
    print(data.get_news(1))


if __name__ == "__main__":
    main()
