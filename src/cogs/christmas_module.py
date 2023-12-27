
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta


class ChristmasModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.christmas_countdown = ChristmasCountdown()
        self.daily_countdown.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user.name}')
        # Ensure that the Christmas channel exists or create it
        await self.ensure_christmas_channel()

    async def ensure_christmas_channel(self):
        # Access the guild ID from the command context
        guild_id = self.bot.guilds[0].id  # Assuming the bot is only in one guild, adjust accordingly

        # Replace 'christmas' with your actual channel name
        channel_name = 'christmas'

        # Check if the channel already exists
        guild = self.bot.get_guild(guild_id)
        christmas_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

        if christmas_channel is None:
            # The Christmas channel doesn't exist, create it
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True)
            }
            christmas_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            print(f"Created Christmas channel: {christmas_channel.name}")
        else:
            print(f"Christmas channel found: {christmas_channel.name}")

        # Check if the bot has the necessary permissions in the channel
        bot_member = guild.get_member(self.bot.user.id)
        if not christmas_channel.permissions_for(bot_member).read_messages:
            print(f"Bot doesn't have read message permissions in {christmas_channel.name}, fixing...")
            await christmas_channel.set_permissions(bot_member, read_messages=True)

    @tasks.loop(hours=24)  # Run the task every 24 hours
    async def daily_countdown(self):
        # Get the Christmas countdown message
        days_remaining = self.christmas_countdown.calculate_days_remaining()
        if days_remaining == 0:
            message = "Merry Christmas! 🎄🎅🎁"
        elif days_remaining == 1:
            message = "Only 1 day left until Christmas! 🎄🎅🎁"
        else:
            message = f"{days_remaining} days left until Christmas! 🎄🎅🎁"

        # Get the channel where you want to send the countdown message
        guild_id = self.bot.guilds[0].id  # Assuming the bot is only in one guild, adjust accordingly
        channel_name = 'christmas'
        guild = self.bot.get_guild(guild_id)
        christmas_channel = discord.utils.get(guild.channels, name=channel_name, type=discord.ChannelType.text)

        # Send the countdown message to the channel
        await christmas_channel.send(message)

    @daily_countdown.before_loop
    async def before_daily_countdown(self):
        # Calculate the time until the next day (midnight)
        now = datetime.now()
        tomorrow = datetime(now.year, now.month, now.day) + timedelta(days=1)
        time_until_midnight = (tomorrow - now).seconds
        # Sleep until midnight
        await discord.utils.sleep_until(datetime.now() + timedelta(seconds=time_until_midnight))


class ChristmasCountdown:

    def __init__(self):
        self.current_date = datetime.now()
        self.christmas_date = datetime(self.current_date.year, 12, 25)

        # Check if Christmas already passed this year, if yes, calculate for the next year
        if self.current_date > self.christmas_date:
            self.christmas_date = datetime(self.current_date.year + 1, 12, 25)

    def calculate_days_remaining(self):
        # Calculate the remaining days until Christmas
        remaining_time = self.christmas_date - self.current_date
        return remaining_time.days
    

async def setup(bot):
    await bot.add_cog(ChristmasModule(bot))


def test():
    cc = ChristmasCountdown()
    print(cc.christmas_date)
    print(cc.calculate_days_remaining())


if __name__ == "__main__":
    test()
