
import discord
import pytz
from discord.ext import commands, tasks
from datetime import datetime, time
from discord import app_commands
from typing import Optional
from lib.admin_tools import is_owner, load, save
from enum import Enum
from lib.calendar import Calendar
from lib.birthdayreminder import BirthdayReminder

cet = pytz.timezone('CET')
trigger_time = time(hour=6, minute=10, tzinfo=cet)


class BirthdayModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.birthdays_file = 'birthdays.dat'
        self.birthdays = BirthdayReminder(self.birthdays_file)
        self.channels_file = 'birthday_channels.dat'
        self.channels = load(self.channels_file) or {}
        self.daily_countdown.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    @tasks.loop(time=trigger_time)
    async def daily_countdown(self):
        # do the birthday checks here
        current_month = datetime.today().month
        current_day = datetime.today().day

        check_day = f"{current_month}-{current_day}"
        pass

    def add_birthday_to_reminder(self, guild, user, year, month, day, show):
        try:
            self.birthdays.add_birthday(guild, user, year, month, day, show)
            self.birthdays.save()
        except Exception as e:
            print(e)

    class ShowOrNot(Enum):
        no = 0
        yes = 1

    @app_commands.command(name='addbirthday')
    @app_commands.describe(day='the day as number',
                           month='the month as number',
                           year='the year as number',
                           display_birthyear='Show it or not (Optional)')
    async def add_birthday(self, interaction: discord.Interaction, day:int, month:int, year:Optional[int], display_birthyear:ShowOrNot):
        user_id = interaction.user.id
        year = year or datetime.today().year
        
        print(interaction.user, year, month, day, display_birthyear, display_birthyear.value)
        
        if Calendar.is_valid(day, month, year):

            self.add_birthday_to_reminder(interaction.guild.id, user_id, year, month, day, bool(display_birthyear.value))
            await interaction.response.send_message(f"{interaction.user.display_name}")

        else:
            await interaction.response.send_message(f"birthday ({day}-{month}-{year}) is not valid..")

    @app_commands.command(name='removebirthday')
    async def remove_birthday(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        # todo: check if user is in list
        # remove user from list
        # return success
        print(interaction.user.display_name)
        await interaction.response.send_message(f"{interaction.user}")

    @app_commands.command(name='debugaddbirthday')
    @app_commands.describe(user='the user you want to add',
                           day='the day as number',
                           month='the month as number',
                           year='the year as number (optional)')
    @is_owner()
    async def debug_add_birthday(self, interaction: discord.Interaction, user:discord.Member, day:int, month:int, year:Optional[int]):
        user_id = interaction.user.id
        
        print(interaction.user.display_name, user_id, year)
        await interaction.response.send_message(f"{interaction.user.display_name}")
    
    @app_commands.command(name="setbirthdaychannel")
    @app_commands.describe(channel='Birthday Channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def set_birthday_channel(self, interaction: discord.Interaction, channel:Optional[discord.channel.TextChannel]):
        channel = channel or interaction.channel
        guild = interaction.guild

        try:
            if guild not in self.channels:
                self.channels[guild.id] = channel.id

            save(self.channels_file, self.channels)

        except Exception as e:
            print(e)

        await interaction.response.send_message(f'Xmas Channel is now {channel}')


async def setup(bot):
    await bot.add_cog(BirthdayModule(bot))


def test():
    pass


if __name__ == "__main__":
    test()
