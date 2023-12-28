from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord import Embed, Member
from discord.ext import commands


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

        panel = Embed(title="User Information", color=target.color, timestamp=datetime.utcnow())
        panel.set_thumbnail(url=target.avatar)

        panel.set_author(name=target.display_name)
        panel.add_field(name='ID', value=target.id)
        panel.add_field(name='Bot', value=target.bot)

        panel.add_field(name='Created at', value=target.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        if hasattr(target, 'joined_at'):
            panel.add_field(name='Joined at', value=target.joined_at.strftime("%d/%m/%Y %H:%M:%S"))

        await ctx.send(embed=panel)

    @commands.command(name='clear', brief='delete <x> messages', help='delete last <x> messages')
    @commands.is_owner()
    async def purge_messages(self, ctx, count: Optional[int]):
        deleted = await ctx.channel.purge(limit=count)
        await ctx.author.send('Deleted {} Messages'.format(len(deleted)))

    @app_commands.command()
    async def serverinfo(self, interaction: discord.Interaction):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await interaction.response.send_message(f"it is {current_time}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
