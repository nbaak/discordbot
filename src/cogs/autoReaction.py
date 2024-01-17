import random
import discord
from discord.ext import commands
from discord import app_commands
from lib.admin_tools import load, save


def random_reaction():
    reactions = ['👍', '✅', '🙂', '🐷']

    return random.choice(reactions)


class AutoReaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_file = 'autolike.dat'
        self.enabled_servers = load(self.channel_file) or set()
        self.reaction_threshold = .05

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.guild.id in self.enabled_servers and self.reaction_threshold >= round(random.random(), 2):
            try:
                await message.add_reaction(random_reaction())
            except discord.errors.HTTPException:
                print(f"Bot doesn't have the permission to add reactions in {message.guild.name}")

    @app_commands.command(name='enableautolike', description='Enable automatic liking for the server.')
    @app_commands.checks.has_permissions(administrator=True)
    async def enable_auto_like(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id not in self.enabled_servers:
            self.enabled_servers.add(guild_id)
            save(self.channel_file, self.enabled_servers)
            await interaction.response.send_message('Automatic liking enabled for this server. ✅', ephemeral=True)
        else:
            await interaction.response.send_message('Automatic liking is already enabled for this server. ✅', ephemeral=True)

    @enable_auto_like.error
    async def enable_auto_like_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("You need administrator permissions to enable automatic liking for this server. ❌", ephemeral=True)

    @app_commands.command(name='disableautolike', description='Disable automatic liking for the server.')
    @app_commands.checks.has_permissions(administrator=True)
    async def disable_auto_like(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        if guild_id in self.enabled_servers:
            self.enabled_servers.remove(guild_id)
            save(self.channel_file, self.enabled_servers)
            await interaction.response.send_message('Automatic liking disabled for this server. ❌', ephemeral=True)
        else:
            await interaction.response.send_message('Automatic liking is already disabled for this server. ❌', ephemeral=True)

    @disable_auto_like.error
    async def disable_auto_like_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("You need administrator permissions to disable automatic liking for this server. ❌", ephemeral=True)


async def setup(bot):
    await bot.add_cog(AutoReaction(bot))
