# this file is the absolute minimum required 'extension' for bot

from discord.ext import commands
import random

class base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot: {} is now Online.'.format(self.bot.user))

    # bot on_disconnect
    @commands.Cog.listener()
    async def on_disconnect(self):
        print('Bot: {} is now Offline.'.format(self.bot.user))

def setup(bot: commands.Bot):
    bot.add_cog(base(bot))
