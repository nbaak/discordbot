from discord.ext import commands
from ai.Bottler import Bottler
import CONFIG

class AI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        MODEL_FILE_NAME = 'model/chatbot.model'
        TOKEN_FILE_NAME = 'pattern.tokens'
        LABELS_FILE_NAME = 'labels.tokens'
        INTENTS_FILE = 'intents.json'
        self.ai = Bottler(MODEL_FILE_NAME, TOKEN_FILE_NAME, LABELS_FILE_NAME, INTENTS_FILE)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Extension {self.__class__.__name__} loaded')

    
    @commands.Cog.listener('on_message')
    async def answer(self, message):
        if not message.author.bot and not message.content.startswith(self.bot.command_prefix):
            channel = message.channel.name
            if not CONFIG.AI_CHANNELS:
                await self._answer(message)
            elif channel in CONFIG.AI_CHANNELS:
                await self._answer(message)               
                
                
    async def _answer(self, message):
        content = message.content
        channel = message.channel
        author  = message.author.display_name
        
        reply = self.ai.answer(content.lower(), author)
        if reply:
            await channel.send(reply)



def setup(bot):
    bot.add_cog(AI(bot))