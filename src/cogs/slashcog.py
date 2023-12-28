
import discord
from discord import app_commands
from discord.ext import commands


class TestSlashesWithSlaps(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ab geht's mit slashes")

    @app_commands.command(description="slap")
    async def slap(self, interaction: discord.Interaction, reason:str):
        await interaction.response.send_message(f"{interaction.user} slaps around for a good reason: '{reason}' !!")


async def setup(bot):
    await bot.add_cog(TestSlashesWithSlaps(bot))
