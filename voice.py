from discord.ext import commands
# Voicechat ID Response and recognition
# Playing Music HQ, queueing, skipping, Stop, Pause
class v_entertainment(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

class v_misc(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            
def setup(bot: commands.Bot):
    bot.add_cog(usocommandsvoice(bot))
