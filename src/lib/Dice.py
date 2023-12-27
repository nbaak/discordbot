import random
import re


class Dice:

    def __init__(self):
        pass

    @staticmethod
    def roll(dice=None):
        if dice == None:
            return "1d6", random.randint(1, 6)

        dices = Dice.is_valid(dice)[1]
        eyes = Dice.is_valid(dice)[2]

        valid_dice = dices, eyes = list(map(int, [dices, eyes]))

        if valid_dice:

            if dices in range(1, 101) and eyes in range(1, 201):
                results = []
                output = ""
                for _ in range(dices):
                    d = random.randint(1, eyes)
                    results.append(d)

                results.sort(reverse=True)
                output = Dice.to_string(results)
                string = f"{output} total: {sum(results)}"
                return f"{dices}d{eyes}", string

        return "1d6", random.randint(1, 6)

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
