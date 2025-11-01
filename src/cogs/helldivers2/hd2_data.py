from cogs.helldivers2 import api
from typing import Union, Dict, List, Tuple
from cogs.helldivers2.hd2_tools import convert_to_datetime, get_recent_messages, \
    delta_to_now, formatted_delta, time_to_seconds
import statistics
import time
from cogs.helldivers2.progress_prediction import ProgressPrediction
import cogs.helldivers2.hd2_major_order as hd2_major_order


class HD2DataService():

    def __init__(self, initial_update:bool=True, contact:str=None):
        # api endpoint params
        api.X_SUPER_CLIENT = "Discord-Bot"
        api.X_SUPER_CONTACT = contact or ""

        hd2_major_order.hd2_data = self

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

        self.news.sort(key=lambda item: item["id"], reverse=True)

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

    def faction_icon(self, faction_id:Union[int, str]) -> str:
        if isinstance(faction_id, int):
            factions = {0: "🌎", 1: "🪲", 2: "🤖", 3: "🦑"}
        else:
            factions = {"Humans": "🌎", "Terminids": "🪲", "Automaton": "🤖", "Illuminate": "🦑", "Automatons": "🤖", "Illuminates": "🦑"}
            
        # return blank if unkown
        return factions.get(faction_id, " ")

    def faction_name(self, faction_id:int) -> str:
        factions = {0: "Any Enemies", 1: "Terminids", 2: "Automaton", 3: "Illuminate"}
        # factions = self.war_statistics["factions"]
        return factions.get(faction_id, "Unknown_Faction")

    def target_faction(self, faction_id:int) -> str:
        factions = {0: "Any Enemies", 1: "Humans", 2: "Terminids", 3: "Automaton", 4: "Illuminate"}
        return factions.get(faction_id, "Unknown_Faction")

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

    def mo_progress(self, major_order:dict) -> str:
        try:
            progress = major_order["progress"]
            tasks = major_order["tasks"]
            text = ""

            for task, prog in zip(tasks, progress):
                text += hd2_major_order.mission(task["type"], prog, task)

            return text

        except Exception as e:
            print(f"Unkown MO!")
            print(e)
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
            text = ""
            last = len(self.major_order)
            for i, mo in enumerate(self.major_order):
                progress = self.mo_progress(mo)

                title = mo.get("title")
                if title == None:
                    continue

                briefing = mo.get("briefing", "")
                description = mo.get("description", "")
                if not description:
                    description = ""

                if briefing == description:
                    head = f"# {title}\n{briefing}"
                else:
                    head = f"# {title}\n{briefing}\n{description}"

                text += f"{head}\n{progress}"
                if mo['reward']:
                    text += f"Reward: {mo['reward']['amount']} 🏅\n"
                text += f"ends in {self.mo_time_remaining(mo)}"
                if i != last:
                    text += "\n"

            return text

        else:
            return f"MAJOR ORDER\nNo Major Order active!"

    def get_current_online_players(self):
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
        # trend = None

        # if entry does not exist, create
        if not planet_name in self.planet_defense_progress:
            self.planet_defense_progress[planet_name] = ProgressPrediction(current_health, current_time)

        else:
            pp = self.planet_defense_progress[planet_name]
            p_time = pp.calculate_progress(current_health, current_time)
            # trend = pp.mean()
            # print("trend", planet_name, trend, current_health)
            if defense and p_time is not None:
                # print(planet_name, formatted_delta(p_time), "defense")

                if p_time < mission_ends_in.total_seconds():
                    succeesing = f", SUCCEEDING {formatted_delta(p_time)}"
                else:
                    succeesing = f", FAILING {formatted_delta(p_time)}"

            # offense
            elif not defense and p_time is not None and p_time >= 0 and p_time < time_to_seconds(days=1):
                # print(planet_name, formatted_delta(p_time), "offense")
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

    def get_campaign(self, top_n:int=10) -> str:
        if self.campaign:
            total_war_planets = len(self.campaign)
            printable_campaign_objects:List[str] = []
            
            for idx, campaing_object in enumerate(sorted(self.campaign, key=lambda c: c["planet"]["statistics"]["playerCount"], reverse=True)):
                planet = campaing_object["planet"]
                planet_id = planet["index"]
                defense, percentage, faction, remaining_time, time_delta = self.planet_info(planet_id)
                defense_icon = "🛡️" if defense else "⚔️"

                holder_icon = self.faction_icon(faction)
                player_count = planet["statistics"]["playerCount"]

                succeeding = self.campaign_succeesing(defense, planet, time_delta) or ""
                if succeeding or idx < top_n:
                    text = f"{holder_icon}{defense_icon} {planet['name']}{remaining_time}: liberation: {percentage:3.2f}%, active Helldivers: {player_count}{succeeding}"
                    printable_campaign_objects.append(text)
            
            visible_war_planets = len(printable_campaign_objects)
                    
            text = ("# War Campaign\n"        
                    f"first {visible_war_planets} planets of total {total_war_planets}\n"
                    )
            text += "\n".join(printable_campaign_objects) + "\n"
                    
            remaining_war_planets = total_war_planets - visible_war_planets
            text += f"{remaining_war_planets} more planets in war..\n"
            
            helldivers_online_total = self.get_current_online_players()
            text += f"\nHelldivers active: {helldivers_online_total}"

            return text
        else:
            return f"No campaign data available."

    def get_news(self, days=1):
        if self.news:
            entries = get_recent_messages(self.news, days)
            message = "NEWS:\n"
            message += "\n\n".join(entries)

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
    mo_body = data.get_major_order()
    campaign_body = data.get_campaign()
    
    print(mo_body)
    print(f"Body MO Length: {len(mo_body)}")
    print()
    print(campaign_body)
    print(f"Body Campaign Length: {len(campaign_body)}")
    print()

    print(data.get_news(2))

    # print(data.statistics())


if __name__ == "__main__":
    main()
