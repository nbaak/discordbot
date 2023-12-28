from lib.Dice import Dice as D
from discord.ext import commands
from discord import app_commands
import discord


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')
        
        # try:
        #     synced = await self.bot.tree.sync()
        #     print('synced', len(synced), 'from', self.__class__.__name__)
        # except Exception as e:
        #     print(e)
    
    @commands.command(brief='!roll <dice:optional> - Roll some dice, default 1d6', aliases=['r'])
    async def roll(self, ctx, dice = '1d6'):
        dice, result = D.roll(dice)
        await ctx.send(f"{ctx.message.author.display_name} used a {dice} and got {result}")
        
    @app_commands.command(name='roll')
    async def s_roll(self, interaction: discord.Interaction, dice:str='1d6'):
        dice, result = D.roll(dice)
        await interaction.response.send_message(f"{interaction.user} used a {dice} and got {result}")
        
        


async def setup(bot):
    await bot.add_cog(Dice(bot))
