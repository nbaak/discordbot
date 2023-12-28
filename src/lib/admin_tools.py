import discord
from discord import app_commands
import random


def is_owner():

    def predicate(interaction: discord.interactions):
        if interaction.user.id == interaction.guild.owner_id:
            return True
        return False

    return app_commands.check(predicate)


def access_denied_message():
    messages = [
        'not allowed', 
        'not for you', 
        'sorry bro', 
        'sorry bra', 
        ':(', 
        'STOP, Hammertime!',
        '🛑',
        'no rights, no access..'
        ]
    return random.choice(messages)
