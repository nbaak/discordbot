from lib.Dice import Dice as D
import discord
from discord import app_commands
from discord.ext import commands


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    @commands.command(brief='!roll <dice:optional> - Roll some dice, default 1d6', aliases=['r'])
    async def roll(self, ctx, dice='1d6'):
        dice, result = D.roll(dice)
        await ctx.send(f"{ctx.message.author.display_name} used a {dice} and got {result}")

    @app_commands.command(name='roll')
    @app_commands.describe(dice='Roll a dice. Default 1d6. (dices)d(eyes)')
    async def s_roll(self, interaction: discord.Interaction, dice:str='1d6'):
        dice, result = D.roll(dice)
        await interaction.response.send_message(f"{interaction.user} used a {dice} and got {result}")


async def setup(bot):
    await bot.add_cog(Dice(bot))
