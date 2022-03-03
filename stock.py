# used to track stocks

from discord.ext import commands
import polygon
import json
from types import SimpleNamespace

import global_var

class stock(commands.Cog):

    # token will be read from a json in the future to avoid security threats
    token = 'x'

    def __init__(self, bot):
        self.bot = bot

    # queue stock for monitoring by putting stack onto json

    # list stonks detail
    # watch stonks detail (every hour)
    # good morning stonks notif / good night stonks notif
