# used to track stocks

# discord dependancy
from discord.ext import commands
# stock dependancy
import polygon
# project dependancy
import obj.tokens

import global_var

class stock(commands.Cog):

    token = obj.tokens.BotToken.get_token('stocks')

    def __init__(self, bot):
        self.bot = bot

    # queue stock for monitoring by putting stack onto json

    # list stonks detail
    # watch stonks detail (every hour)
    # good morning stonks notif / good night stonks notif
