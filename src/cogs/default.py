from discord.ext import commands


class Default(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    # Commands
    @commands.command(brief='check Bot-Status')
    async def alive(self, ctx):
        await ctx.message.add_reaction('✅')



def setup(bot):
    bot.add_cog(Default(bot))
