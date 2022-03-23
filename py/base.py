# this file is the absolute minimum required 'extension' for bot

# discord dependancy
from discord.ext import commands
# os dependancy
import shutil
# base dependancy
import random

class base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        # make sure all connections are cleanly disconnected
        for v_client in self.bot.voice_clients:
            await v_client.disconnect()
        try:
            shutil.rmtree('voice/music')
        except FileNotFoundError:
            pass
        print('Bot: {} is now Online.'.format(self.bot.user))
        # if bot has not been initialized, DM whoever invited the bot


    # bot on_disconnect
    @commands.Cog.listener()
    async def on_disconnect(self):
        print('Bot: {} is now Offline.'.format(self.bot.user))

def setup(bot: commands.Bot):
    bot.add_cog(base(bot))
