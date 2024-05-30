from cogs.helldivers2 import api
import pickle


class HD2DataService():
    
    def __init__(self):
        self.war_status = None
        self.war_info = None
        self.news = None
        self.campaign = None
        self.planet_index = None
        self.major_order = None
        self.planets = api.planets()
        
    def update_major_order(self):
        self.major_order = api.get_major_order()
        
    def update_campaign(self):
        self.campaign = api.get_campaign()
        
    def update_war_status(self):
        self.war_status = api.get_war_status()
        
    def update_war_info(self):
        self.war_info = api.get_war_info()
        
    def update_all(self):
        self.update_campaign()
        self.update_major_order()
        self.update_war_info()
        self.update_war_status()
        
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
        
    def get_major_order(self):
        mo = self.major_order[0]
        expires = int(self.major_order[0]['expiresIn'])
        progress = self.major_order[0]['progress']
        
        title = f"{self.major_order[0]['setting']['overrideTitle']}\n{self.major_order[0]['setting']['overrideBrief']}\n"
        text = f"{title}\n"
        
        return text
            

def main():
    data = HD2DataService()
    # data.update_all()
    # data.save_all()
    data.load_all()
    for k,v in data.major_order[0].items():
        print(k, v)

    print()        
    print(data.get_major_order())
    

if __name__ == "__main__":
    main()