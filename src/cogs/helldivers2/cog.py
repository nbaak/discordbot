import discord
from discord.ext import commands, tasks

import cogs.helldivers2.api as api


class Helldivers2(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        test()


def test():
    print(api.get_news())
    


async def setup(bot):
    await bot.add_cog(Helldivers2(bot))