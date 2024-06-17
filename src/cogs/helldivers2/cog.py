import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.interactions import Interaction

from lib.admin_tools import load, save, access_denied_message
import cogs.helldivers2.api as api
from cogs.helldivers2.tmt import TrainingManualTips
from typing import Optional

from cogs.helldivers2.hd2_data import HD2DataService


class Helldivers2(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels_file = 'hd2_channels.dat'
        self.channels = load(self.channels_file) or {}
        self.messages_file = 'hd2_message_ids.dat'
        self.messages = load(self.messages_file) or {}
        self.tmt = TrainingManualTips()
        self.hd2dataservice = HD2DataService()
        self.countdown.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')
        
    async def update_warsatus(self):
        try:
            self.hd2dataservice.update_all()
            
            message_mo = self.hd2dataservice.get_major_order()  
            await self.send_channel_message(message_mo, 'major_order')
            
            message_campaign = self.hd2dataservice.get_campaign()
            await self.send_channel_message(message_campaign, 'campaign')
        except Exception as e:
            print(e)
        
    @tasks.loop(minutes=5.0)
    async def countdown(self):
        await self.update_warsatus()
        
    async def send_channel_message(self, message:str, identifier:str):
        for cid in self.channels.values():
            channel = discord.utils.get(self.bot.get_all_channels(), id=cid)
            recycled_message = False
            
            if channel:
                channel_to_message_identifier = (channel.guild.id, channel.id, identifier)
                if channel_to_message_identifier in self.messages:
                    try:
                        msg = await channel.fetch_message(self.messages[channel_to_message_identifier])
                        recycled_message = True
                    except Exception as e:
                        msg = await channel.send(content=message)
                        self.messages[channel_to_message_identifier] = msg.id
                        save(self.messages_file, self.messages)
                        recycled_message = False
                    
                    if recycled_message:
                        await msg.edit(content=f'{message}')                        
                    
                else:
                    msg = await channel.send(content=message)
                    self.messages[channel_to_message_identifier] = msg.id
                    save(self.messages_file, self.messages)
                           
    @app_commands.command(name="sethelldiverschannel")
    @app_commands.describe(channel='Helldivers 2 Channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def set_helldivers2_channel(self, interaction: discord.Interaction, channel:Optional[discord.channel.TextChannel]):
        channel = channel or interaction.channel
        guild = interaction.guild

        try:
            if guild not in self.channels:
                self.channels[guild.id] = channel.id

            save(self.channels_file, self.channels)

        except Exception as e:
            print(e)

        await interaction.response.send_message(f'HD2 Channel is now {channel}')
    
    @app_commands.command(name="updatewarstatus")
    @app_commands.checks.has_permissions(administrator=True)
    async def update_warstatus_now(self, interaction: discord.Interaction):
        await self.update_warsatus()
        await interaction.response.send_message('updating war status', ephemeral=True)
    
    @app_commands.command(name='trainingmanualtips')
    async def trainingmanualtips(self, interaction:Interaction):
        message = self.tmt.random()
        await interaction.response.send_message(message, ephemeral=True)


def test():
    print(api.get_news())


async def setup(bot):
    await bot.add_cog(Helldivers2(bot))
