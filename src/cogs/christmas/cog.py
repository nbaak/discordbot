
import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import pytz
from discord import app_commands

from cogs.christmas.progressbar import ProgressBar
from cogs.christmas.christmas_countdown import ChristmasCountdown
from lib.calendar import Calendar
from lib.admin_tools import load, save, access_denied_message
from typing import Optional
from discord.interactions import Interaction

cet = pytz.timezone('CET')
trigger_time = time(hour=6, minute=1, tzinfo=cet)


class ChristmasModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.daily_countdown.start()
        self.channel_file = 'christmas_channels.dat'
        self.channels = load(self.channel_file) or {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')
        print(f'{self.christmas_countdown.calculate_days_remaining()}')

    @tasks.loop(time=trigger_time)
    async def daily_countdown(self):
        messages = self.build_xmas_message()
        await self.send_xmas_messages(messages, list(self.channels.values()))

    def build_xmas_message(self, progress=True):
        # Get the Christmas countdown message
        days_remaining = ChristmasCountdown.calculate_days_remaining()
        next_christmas_year = ChristmasCountdown.next_christmas_year()

        # check date
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        
        messages = []
        if days_remaining == 0:
            message = "Merry Christmas Eve! 🎄🎅🎁"
        elif days_remaining == 1:
            message = "Only 1 day left until Christmas Eve! 🎄🎅🎁"
        else:
            message = f"{days_remaining} days left until Christmas Eve! 🎄🎅🎁"

        messages.append(message)

        # AoC Reminder
        if current_month == 12:
            if current_day in range(1, 26):
                aoc_url = f"https://adventofcode.com/{current_year}/day/{current_day}"
                aoc_message = f"Visit the [Advent of Code - {current_year} - Day {current_day}]({aoc_url}) "
                messages.append(aoc_message)

        # Progress Bar
        if progress:
            days_in_year = 366 if Calendar.is_leap_year(next_christmas_year) else 365
            progress_bar = ProgressBar(days_in_year, 50)
            try:
                progress_bar.image(days_in_year - days_remaining, 'progress.png')
            except Exception as e:
                print(e)

        return messages

    async def send_xmas_messages(self, messages:list, channels:list):
        # Send the countdown message to all known Christmas channels
        for cid in channels:
            channel = discord.utils.get(self.bot.get_all_channels(), id=cid)
            if os.path.isfile('progress.png'): 
                await channel.send(content='\n'.join(messages), file=discord.File('progress.png'))
            else:
                await channel.send(content='\n'.join(messages))

        try:
            os.remove('progress.png')
        except Exception as e:
            print(e)

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def testxmas(self, interaction: discord.Interaction):
        try:
            messages = self.build_xmas_message()
            channels = [self.channels[interaction.guild.id]]
            await self.send_xmas_messages(messages, channels)
        except Exception as e:
            await interaction.response.send_message(f'ERROR: {e}', ephemeral=True)
        await interaction.response.send_message('running test...', ephemeral=True)

    @testxmas.error
    async def error_testxmas(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(access_denied_message())

    @app_commands.command(name="setchristmaschannel")
    @app_commands.describe(channel='Christmas Channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def set_christmas_channel(self, interaction: discord.Interaction, channel:Optional[discord.channel.TextChannel]):
        channel = channel or interaction.channel
        guild = interaction.guild

        try:
            if guild not in self.channels:
                self.channels[guild.id] = channel.id

            save(self.channel_file, self.channels)

        except Exception as e:
            print(e)

        await interaction.response.send_message(f'Xmas Channel is now {channel}')

    @set_christmas_channel.error
    async def set_christmas_channel_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(access_denied_message())

    @app_commands.command(name="endchristmas")
    @app_commands.checks.has_permissions(administrator=True)
    async def end_christmas(self, interaction: discord.Interaction):
        guild = interaction.guild

        if guild.id in self.channels:
            del self.channels[guild.id]

            await interaction.response.send_message(f"Christmas Messages are over.. for now")
            save(self.channel_file, self.channels)
        else:
            await interaction.response.send_message(f"no need!")

    @end_christmas.error
    async def error_end_christmas(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(access_denied_message())

    @app_commands.command(name='whenischristmas')
    async def when_is_christmas(self, interaction:Interaction):
        messages = self.build_xmas_message(progress=False)
        await interaction.response.send_message('\n'.join(messages), ephemeral=True)

    @app_commands.command(name='checkchristmaschannel')
    async def check_christmas_channel(self, interaction: discord.Interaction):
        try:
            cid = self.channels[interaction.guild.id]
            channel = discord.utils.get(self.bot.get_all_channels(), id=cid)

            await interaction.response.send_message(f'The Xmas Channel is {channel}')
        except Exception as e:
            await interaction.response.send_message(f'Xmas Channel is not set')

    @commands.command()
    async def hoho(self, ctx):
        await ctx.send(f"HOHO, {ctx.message.author.display_name}!")

    @app_commands.command()
    async def gift(self, interaction: discord.Interaction, recipient:discord.Member):
        await interaction.response.send_message(f"{interaction.user} sends a gift to {recipient.display_name} 🎁")


async def setup(bot):
    await bot.add_cog(ChristmasModule(bot))


def test():
    next_christmas_year = ChristmasCountdown.next_christmas_year()
    pb = ProgressBar(366 if Calendar.is_leap_year(next_christmas_year) else 365, 50)
    days_remaining = ChristmasCountdown.calculate_days_remaining()
    print(days_remaining)
    print(pb.get((366 if Calendar.is_leap_year(next_christmas_year) else 365) - days_remaining))


if __name__ == "__main__":
    test()
