import random
import re


class Dice:
    
    def __init__(self):
        pass    
    
    @staticmethod
    def roll(dice = None):
        result = Dice.is_valid(dice)
        
        if dice == None:
            return "1d6", random.randint(1,6)
        
        elif result:            
            dices = int(result[1])
            eyes = int(result[2])
            
            if isinstance(dices, int) and isinstance(eyes, int) and dices >= 0 and eyes >= 0 and dices <= 100 and eyes <= 1000:
                results = []
                output = ""
                for _ in range(dices):
                    d = random.randint(1, eyes)
                    results.append(d)
                    
                results.sort(reverse=True)
                output = Dice.to_string(results)
                string = f"{output} total: {sum(results)}" 
                return f"{dices}d{eyes}", string
            
        else:
            return None, "no valid dice"
    
    @staticmethod
    def to_string(contents):
        output = ""
        for value in contents:
            output += f"{value} "
           
        return output
           
           
    @staticmethod
    def is_valid(dice):
        if dice:
            pattern = "([0-9]+)d([0-9]+)"
            return re.match(pattern, dice)
        
        else:
            return False
        