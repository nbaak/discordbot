from datetime import datetime
from typing import Optional

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

        e = Embed(title="User Information", color=target.color, timestamp=datetime.utcnow())
        e.set_thumbnail(url=target.avatar_url)

        e.set_author(name=target.display_name)
        e.add_field(name='ID', value=target.id)
        e.add_field(name='Bot', value=target.bot)

        e.add_field(name='Created at', value=target.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        if hasattr(target, 'joined_at'):
            e.add_field(name='Joined at', value=target.joined_at.strftime("%d/%m/%Y %H:%M:%S"))

        await ctx.send(embed=e)

    @commands.command(name='clear', brief='delete <x> messages', help='delete last <x> messages')
    @commands.is_owner()
    async def purge_messages(self, ctx, count: Optional[int]):
        deleted = await ctx.channel.purge(limit=count)
        await ctx.author.send('Deleted {} Messages'.format(len(deleted)))


async def setup(bot):
    await bot.add_cog(Admin(bot))
