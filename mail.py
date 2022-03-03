# monitors packages. Should be used only in a private channel. Make private thread?

from discord.ext import commands
import shippo
import json
from types import SimpleNamespace

import global_var

class mail(commands.Cog):

    # token will be read from a json in the future to avoid security threats
    token = 'x'

    def __init__(self, bot):
        self.bot = bot
        self.company = ''
        self.tracking_number = ''
        shippo.config.api_key = token

    # track package
    # syntax: track #carrier #track_number #package_name
    @commands.command()
    async def track(self, ctx):
        arg = ctx.message.content.split(' ')
        carrier = arg[1]
        track_number = arg[2]
        package_name = arg[3]
        try:
            tracking = shippo.Track.get_status(carrier, track_number)
            # print(tracking) in channel
        except:
            # print error message

        # continue to monitor tracking_number

    # untrack package
    @commands.command()
    async def untrack(self, ctx):

def setup(bot: commands.Bot):
    bot.add_cog(mail(bot))
