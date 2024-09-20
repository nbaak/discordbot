from cogs.helldivers2 import api
from typing import Union, Dict, List, Tuple
from cogs.helldivers2.hd2_tools import convert_to_datetime, get_recent_messages, \
    delta_to_now, formatted_delta, time_to_seconds
import statistics
import time
from cogs.helldivers2.progress_prediction import ProgressPrediction
from cogs.helldivers2.hd2_units import get_enemy
from cogs.helldivers2.hd2_major_order import mo_task_paramerts, MOTaskTypes, MOMissionTypes


class HD2DataService():
    
    def __init__(self, initial_update=True):
        self.war_statistics: Union[Dict, None] = None
        self.campaign: Union[List[Dict], None] = None
        self.major_order: Union[Dict, None] = None
        self.planets: Union[Dict, None] = None
        self.news: List = []
        
        self.planet_defense_progress: Dict = {}
        
        if initial_update:
            self.update_all()
        
    def update_dispatch(self):
        new_dispatch = api.dispatch()
        self.news = []
        for news in new_dispatch:
            published_int = convert_to_datetime(news["published"])
            news["published"] = published_int
            self.news.append(news)  
        
    def update_major_order(self):
        self.major_order = api.get_major_order()
        
    def update_campaign(self):
        new_campaign = api.get_campaign()
        if new_campaign:
            self.campaign = new_campaign
    
    def update_war_statistics(self):
        new_war_data = api.get_war_statistics()
        if new_war_data:
            self.war_statistics = new_war_data
            
    def update_planets(self):
        new_planets = api.planets()
        if new_planets:
            self.planets = new_planets
        
    def update_all(self):
        self.update_planets()
        time.sleep(.5)
        self.update_campaign()
        time.sleep(.5)
        self.update_major_order()
        time.sleep(.5)
        self.update_war_statistics()
        time.sleep(.5)
        self.update_dispatch()
        
    def find_in_campaign_dict(self, search_key, search_value:str) -> Union[Dict, None]: 
        for planet in self.campaign:
            for k, v in planet.items():
                if k == search_key and v == search_value:
                    return planet        
        return None
    
    def is_planet_in_campaign(self, planet_name):
        for campaign_object in self.campaign:
            if campaign_object['planet']['name'] == planet_name:
                return True
            
        return False
    
    def get_faction_for_planet(self, planet_id:int) -> Tuple[int, str]:
        try:
            owner_id:int = self.planets[planet_id]["currentOwner"]
            icon:str = self.faction_icon(owner_id)
            return owner_id, icon
        except KeyError:
            return 0, "?"
    
    def faction_icon(self, faction:Union[int, str]) -> str:
        if isinstance(faction, int):
            factions = {0: "🌎", 1: "🪲", 2: "🤖", 3: "🦑"}
        else:
            factions = {"Humans": "🌎", "Terminids": "🪲", "Automaton": "🤖", "Illuminate": "🦑", "Automatons": "🤖", "Illuminates": "🦑"}
        
        return factions[faction] if faction in factions else "?"
    
    def faction_name(self, faction_id:int) -> str:
        factions = {0: "Any Enemies", 1: "Terminids", 2: "Automatons", 3: "Illuminates"}
        # factions = self.war_statistics["factions"]
        return factions[faction_id]
    
    def target_faction(self, faction_id:int) -> str:
        factions = {0: "Any Enemies", 1: "Humans", 2: "Terminids", 3: "Automatons", 4: "Illuminates"}
        return factions[faction_id] if faction_id in factions else "UNKOWN"
    
    def units(self, unit_id:int) -> str:
        return get_enemy(unit_id)
    
    def planet_info(self, planet_id:int) -> tuple:
        planet = self.planets[planet_id]        
        defense = True if planet["event"] else False
        percentage = 0
        remaining_time = ""
        
        if defense:
            hp = planet["event"]["health"]
            max_hp = planet["event"]["maxHealth"]
            percentage = (1 - hp / max_hp) * 100 if hp > 0 else 100 
            faction = planet["event"]["faction"]
            event_end_time = planet["event"]["endTime"]
            
            timestamp = convert_to_datetime(event_end_time)
            delta = delta_to_now(timestamp)
            event_end_time = formatted_delta(delta)
            remaining_time = f" ({str(event_end_time)})"
            
        else:
            hp = planet["health"]
            max_hp = planet["maxHealth"]
            percentage = (1 - hp / max_hp) * 100 if hp > 0 else 100
            # percentage = planet["health"] / planet["maxHealth"] * 100
            faction = planet["currentOwner"]
            delta = None
            event_end_time = None
        
        return defense, percentage, faction, remaining_time, delta
    
    def mo_attack_planet(self, progress:int, task:dict) -> str:
        planet_id = task["values"][2]
        planet_name = self.planets[planet_id]["name"]
        
        defense, percentage, faction, _, _ = self.planet_info(planet_id)
        
        if progress:
            defense_icon = "  "
            percentage = 100
            
        else:
            defense_icon = "🛡️" if defense else "⚔️"                
            
        holder_icon = self.faction_icon(faction)
            
        text = f"{holder_icon}{defense_icon} {planet_name}: {abs(percentage):3.2f}%\n"
        
        return text
    
    def mo_defend_planet(self, progress:int, task:dict) -> str:
        task_d = mo_task_paramerts(task)
        # planet_id = task_d[MOTaskTypes.PLANET]
        target = task_d[MOTaskTypes.TARGET_COUNT]
        faction_id = task_d[MOTaskTypes.FACTION]
        # unit_type_id = task_d[MOTaskTypes.UNIT_TYPE]
        
        faction = self.target_faction(faction_id)
        text = f"Defend Planets against {faction}: {progress}/{target}\n"
        
        return text
    
    def mo_kill_enemies(self, progress:int, task:dict) -> str:
        task_d = mo_task_paramerts(task)
        # planet_id = task_d[MOTaskTypes.PLANET]
        target = task_d[MOTaskTypes.TARGET_COUNT]
        faction_id = task_d[MOTaskTypes.FACTION]
        unit_type_id = task_d[MOTaskTypes.UNIT_TYPE]
        progress_percent = progress / target * 100
        faction = self.target_faction(faction_id)        
        unit = f" ({self.units(unit_type_id)}s)" if unit_type_id else ""
        icon = self.faction_icon(faction)
        
        return f"{icon}   {faction}{unit} killed {progress:,}/{target:,} ({progress_percent:.2f}%)\n"
    
    def mo_extract_samples(self, progress:int, task:dict) -> str:
        task_d = mo_task_paramerts(task)
        planet_id = task_d[MOTaskTypes.PLANET]
        target = task_d[MOTaskTypes.TARGET_COUNT]
                
        progress_percent = progress / target * 100
        
        return f"{self.planets[planet_id]['name']}: {progress:,}/{target:,} ({progress_percent:.2f}%)\n"
    
    def mo_hold_planet(self, progress:int, task:dict) -> str:
        task_d = mo_task_paramerts(task)
        planet_id = task_d[MOTaskTypes.PLANET]
        planet_name = self.planets[planet_id]["name"]
        
        defense, percentage, faction, _, _ = self.planet_info(planet_id)
            
        if progress:
            defense_icon = "  "
            percentage = 100
            faction = 0
            
        else:
            defense_icon = "🛡️" if defense else "⚔️" 
        
        holder_icon = self.faction_icon(faction)
        
        return f"{holder_icon}{defense_icon} {planet_name}: {abs(percentage):3.2f}%\n"
    
    def mo_liberate_more_planets_than_lost(self, progress:int, task:dict) -> str:
        task_d = mo_task_paramerts(task)        
        return f"Liberate more Planets than Lost: {progress}\n"
    
    def mo_progress(self, major_order:dict) -> str:
        try:
            progress = major_order["progress"]
            tasks = major_order["tasks"]
            text = f""
            
            for task, prog in zip(tasks, progress):
                if task["type"] == MOMissionTypes.EXTRACT_SAMPLES:
                    text += self.mo_extract_samples(prog, task)
                elif task["type"] == MOMissionTypes.KILL_ENEMIES:
                    text += self.mo_kill_enemies(prog, task)
                elif task["type"] == MOMissionTypes.ATTACK_PLANET: 
                    text += self.mo_attack_planet(prog, task)
                elif task["type"] == MOMissionTypes.DEFENT_PLANET:
                    text += self.mo_defend_planet(prog, task)
                elif task["type"] == MOMissionTypes.HOLD_PLANET:
                    text += self.mo_hold_planet(prog, task)
                elif task["type"] == MOMissionTypes.LIBERTAE_MORE_PLANETS_THAN_LOST:
                    text += self.mo_liberate_more_planets_than_lost(prog, task)
            
            return text
        except:
            print(f"Unkown MO!")
            print(major_order)
    
    def mo_time_remaining(self, major_order:dict=None) -> str:
        if major_order:
            major_order = major_order
        elif major_order == None and self.major_order:
            major_order = self.major_order[0]
        else:
            major_order = None
            
        if major_order: 
            remaining = convert_to_datetime(major_order["expiration"])
            delta = delta_to_now(remaining)
            return formatted_delta(delta)
        else:
            return "---"
        
    def get_major_order(self) -> str:
        if self.major_order:
            mo = self.major_order[0]
            progress = self.mo_progress(mo)
            
            title = f"{mo['title']}"
            if mo['briefing']:
                title += f"\n{mo['briefing']}\n"
            if mo['description'] and mo['description'] != mo['briefing']:
                title += f"{mo['description']}\n"
                
            text = f"{title}\n{progress}" 
            text += f"Reward: {mo['reward']['amount']} 🏅\n"
            text += f"ends in {self.mo_time_remaining(mo)}\n"
            return text
        
        else:
            return f"MAJOR ORDER\nNo Major Order active!"
    
    def get_current_onlie_players(self):
        return self.war_statistics["statistics"]["playerCount"] if self.war_statistics else 0
    
    def campaign_succeesing(self, defense:bool, campaign_planet:dict, mission_ends_in):
        planet_name = campaign_planet['name']
        
        if defense:
            current_health = campaign_planet['event']['health']
        else:
            # offense
            current_health = campaign_planet['health']
            
        current_time = int(time.time())
        
        succeesing = None
        trend = None
        
        # if entry does not exist, create
        if not planet_name in self.planet_defense_progress: 
            self.planet_defense_progress[planet_name] = ProgressPrediction(current_health, current_time)
            
        else:
            pp = self.planet_defense_progress[planet_name]
            p_time = pp.calculate_progress(current_health, current_time)
            trend = pp.mean()
            # print("trend", planet_name, trend)
            if defense and p_time is not None:
                print(planet_name, formatted_delta(p_time), "defense")
                
                if p_time < mission_ends_in.total_seconds():
                    succeesing = f", SUCCEEDING {formatted_delta(p_time)}"
                else:
                    succeesing = f", FAILING {formatted_delta(p_time)}"
                    
            # offense    
            elif not defense and p_time is not None and p_time >= 0 and p_time < time_to_seconds(days=1):
                print(planet_name, formatted_delta(p_time), "offense")
                succeesing = f", SUCCEEDING {formatted_delta(p_time)}"
            else:
                succeesing = None
    
        return succeesing
    
    def campaign_succeesing_cleanup(self):
        for planet_name in self.planet_defense_progress:
            if not self.is_planet_in_campaign(planet_name):
                value = self.planet_defense_progress.pop(planet_name, None)
                
                if value:
                    print(f"removed {planet_name} from defence dict")
                else:
                    print(f"error on dropping key {planet_name}")
        
    def get_campaign(self) -> str:
        if self.campaign:
            text = "War Campaign:\n"
            
            for campaing_object in sorted(self.campaign, key=lambda c: c["planet"]["statistics"]["playerCount"], reverse=True):
                planet = campaing_object["planet"]
                planet_id = planet["index"]
                defense, percentage, faction, remaining_time, time_delta = self.planet_info(planet_id)
                defense_icon = "🛡️" if defense else "⚔️"
                
                holder_icon = self.faction_icon(faction)
                player_count = planet["statistics"]["playerCount"]
                
                succeeding = self.campaign_succeesing(defense, planet, time_delta) or ""
                
                text += f"{holder_icon}{defense_icon} {planet['name']}{remaining_time}: liberation: {percentage:3.2f}%, active Helldivers: {player_count}{succeeding} \n"
            
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
        
    def statistics(self):
        if self.war_statistics:
            statistics = self.war_statistics["statistics"]
            
            text = "*Helldivers 2 Statistics*\n\n"
            
            # Missions
            missions_won = statistics["missionsWon"]
            missions_lost = statistics["missionsLost"]
            win_loss_ratio = (1 - missions_lost / missions_won) * 100
            
            text += f"Mission Won:  {missions_won:,}\nMissions Lost: {missions_lost:,}\nWin Rate: {win_loss_ratio:.2f}%\n\n"
            
            # KD
            terminids_killed = statistics["terminidKills"]
            automatons_killed = statistics["automatonKills"]
            illuminates_killed = statistics["illuminateKills"]
            helldiver_deaths = statistics["deaths"]
            
            kill_death_ratio = (1 - helldiver_deaths / (terminids_killed + automatons_killed + illuminates_killed)) * 100
            
            text += f"Terminids Killed: {terminids_killed:,}\nAutomatons Killed: {automatons_killed:,}\nIlluminates killed: {illuminates_killed:,}\nHelldivers Killed: {helldiver_deaths:,}\n"
            text += f"Kill Rate: {kill_death_ratio:.2f}%\n\n"
            
            # friendly fire
            friendly = statistics["friendlies"]
            friendly_to_total_deaths = (friendly / helldiver_deaths) * 100
            
            text += f"Friendly Fire kills: {friendly:,} Ratio: {friendly_to_total_deaths:.2f}%\n"
            
            return text
        
        else:
            return "no data available!"
            

def main():
    data = HD2DataService()
        
    print(data.get_major_order())
    print(data.get_campaign())
    
    # print(data.get_news(1))
    
    # print(data.statistics())


if __name__ == "__main__":
    main()
