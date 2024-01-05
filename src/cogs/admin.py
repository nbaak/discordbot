from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord import Embed, Member
from discord.ext import commands

from lib.admin_tools import is_owner, access_denied_message
from discord.interactions import Interaction


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    @commands.command(name='userinfo', brief='Userinfo', help='get info for user')
    @commands.is_owner()
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        panel = self.build_user_info(target)

        await ctx.send(embed=panel)

    @app_commands.command(name='userinfo')
    @app_commands.describe(target='User')
    @is_owner()
    async def s_user_info(self, interaction:Interaction, target: Optional[Member]):
        target = target or interaction.user

        panel = self.build_user_info(target)

        await interaction.response.send_message(embed=panel)

    @s_user_info.error
    async def s_user_info_error(self, interaction:Interaction, error):
        await interaction.response.send_message(access_denied_message())

    def build_user_info(self, user:Member) -> Embed:
        panel = Embed(title="User Information", color=user.color, timestamp=datetime.utcnow())
        panel.set_thumbnail(url=user.avatar)

        panel.set_author(name=user.display_name)
        panel.add_field(name='ID', value=user.id)
        panel.add_field(name='Bot', value=user.bot)

        panel.add_field(name='Created at', value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        if hasattr(user, 'joined_at'):
            panel.add_field(name='Joined at', value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"))

        return panel

    @commands.command(name='clear', brief='delete <x> messages', help='delete last <x> messages')
    @commands.is_owner()
    async def purge_messages(self, ctx, count:Optional[int]):
        deleted = await ctx.channel.purge(limit=count)
        await ctx.author.send('Deleted {} Messages'.format(len(deleted)))

    @app_commands.command(name='clear')
    @app_commands.describe(count='the amount of messages you want to delete')
    @app_commands.checks.has_permissions(administrator=True)
    async def s_purge_messges(self, interaction:Interaction, count:Optional[int]):
        await interaction.response.defer()
        deleted = await interaction.channel.purge(limit=count+1)
        await interaction.channel.send('deleting...', ephemeral=True)
        await interaction.user.send(f'Deleted {len(deleted)} Messaged')

    @app_commands.command()
    async def servertime(self, interaction:Interaction):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await interaction.response.send_message(f"it is {current_time}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
