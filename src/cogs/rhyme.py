 
from lib.Rhymes import Rhymes
from discord.ext import commands


class Rhyme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    @commands.command(brief='!reime <word> - german rhymes')
    async def reime(self, ctx, word):
        await ctx.send(Rhymes.reime(word))
        
    @commands.command(brief='!rhyme <word> - english rhymes')
    async def rhyme(self, ctx, word):
        await ctx.send(Rhymes.rhyme(word))

def setup(bot):
    bot.add_cog(Rhyme(bot))
