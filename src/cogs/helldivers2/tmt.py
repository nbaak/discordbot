import random


class TrainingManualTips:
    
    def __init__(self):
        self.tips = ["Did you know tips are shown during these transition sequences?",
                    "Don't die!",
                    "Pay attention to these tips. They've been carefully calibrated to ensure your success.",
                    "Nine out of ten doctors agree that a wound to the chest will make you bleed out if unattended.",
                    "Don't Panic.",
                    "Super Earth recommends spending 2.4 seconds per mission enjoying the scenery. A happy Helldiver is a deadly Helldiver.",
                    "The Automatons are equipped with hyper reactive protocols, making them susceptible to suppressive fire. The more you shoot at them, the less accurate they'll be.",
                    "If at first you don’t succeed, dive, dive again. ... And again. And again. And again. And again. And again. And again. And again. And again. And again. And again. And again. And again. And again. And again...",
                    "As a last resort, you can use melee attacks to fend off enemies. Remember: death is better than cowardice!",
                    "Remember: Freedom!",
                    "Unhappy with who you are? Change your appearance, voice, and personality in the customization chamber. It's that easy!",
                    "Friendly Fire isn't.",
                    "If an enemy ever attempts to engage in diplomacy, SHOOT THEM. We mustn't believe their lies.",
                    "Most enemies have both weak spots and armored spots. The S.E.A.F. training manual recommends aiming for the weak spots.",
                    "When you're up against the bots, remember the 3 Cs: Cover, Courage, and more Cover.",
                    "Don't forget to take breaks! ... That is, if you want to be remembered as a coward.",
                    "Remember to fill in your C-01 permit before any act that could result in a child.",
                    "Failure to complete mission objectives will NOT result in you being sent to a freedom camp, those are merely dissent rumours.",
                    "Don’t drink and drive!",
                    "You are Super Earth's Elite. Remember that.",
                    "If you notice a squad mate sympathizing with an enemy, report them to your democracy officer. Thoughtcrimes kill!",
                    "Practice your daily desensitization exercises to ensure you remain unfazed by enemy atrocities!",
                    "It pays to be a straight shooter-angled fire might glance off your target or even ricochet into your squad mates!",
                    "Diving to the ground can be a lifesaver, but it also makes you an easy target for melee units.",
                    "The longer you stay in a mission, the heavier the enemy presence becomes.",
                    "Most weapons have different fire modes or functions -- Hold Reload to access them.",
                    "If the enemies just keep coming, find out where they're coming from and unleash hell. Bug hive? Destroy! Bot factory? Destroy!",
                    "All Stratagems have their strengths and weaknesses. Choose your Stratagem loadout to best fit the mission and your squad companions.",
                    "Day and night sides of a planet are visible during mission selection, allowing you to choose the mission that's right for you!",
                    "More challenging missions yield greater rewards.",
                    "Every citizen is equally important to the war effort, but Helldivers are the most important.",
                    "Check your Ammo by holding the Reload button.",
                    "Grenades detonation time starts when you pull back for a throw -- time your throw for an air-burst detonation.",
                    "Helldivers traveling the galaxy might come across ancient ruins and other curiosities. Just remember: Only a traitor is curious about alien artifacts!"]
                    
    def random(self):
        return random.choice(self.tips)
    
    
def test():
    tmt = TrainingManualTips('./hd2_tmt.txt')
    print(tmt.random())
    
    
if __name__ == '__main__':
    test()
