import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.interactions import Interaction

from lib.admin_tools import load, save, access_denied_message
import cogs.helldivers2.api as api
from cogs.helldivers2.tmt import TrainingManualTips
from typing import Optional


class Helldivers2(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels_file = 'hd2_channels.dat'
        self.channels = load(self.channels_file) or {}
        self.tmt = TrainingManualTips()
        
    @app_commands.command(name="sethelldiverschannel")
    @app_commands.describe(channel='Helldivers 2 Channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def set_helldivers2_channel(self, interaction: discord.Interaction, channel:Optional[discord.channel.TextChannel]):
        channel = channel or interaction.channel
        guild = interaction.guild

        try:
            if guild not in self.channels:
                self.channels[guild.id] = channel.id

            save(self.channels_file, self.channels)

        except Exception as e:
            print(e)

        await interaction.response.send_message(f'HD2 Channel is now {channel}')
    
    @app_commands.command(name='trainingmanualtips')
    async def trainingmanualtips(self, interaction:Interaction):
        message = self.tmt.random()
        print(message)
        await interaction.response.send_message(message, ephemeral=True)


def test():
    print(api.get_news())


async def setup(bot):
    await bot.add_cog(Helldivers2(bot))
