
from lib.Wikipedia import WikipediaWrapper

from discord.ext import commands
from discord import app_commands
import discord


class Wikipedia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    @commands.command(name="wiki", brief="wiki <topic>", help='Search Wikipedia for a topic')
    async def wiki(self, ctx, topic):
        await ctx.send(WikipediaWrapper.search(topic))

    @app_commands.command(name='wiki')
    @app_commands.describe(topic='The topic you want to look for')
    async def swiki(self, interaction: discord.Interaction, topic:str):
        await interaction.response.send_message(WikipediaWrapper.search(topic))


async def setup(bot):
    await bot.add_cog(Wikipedia(bot))
