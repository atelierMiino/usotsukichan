from discord.ext import commands
# Voicechat ID Response and recognition
# Playing Music HQ, queueing, skipping, Stop, Pause
class usocommandsvoice(commands.Cog):
        def __init__(self, usobot):
            self.usobot = usobot
            self._last_member = None

def setup(bot: commands.Bot):
    bot.add_cog(usocommandsvoice(bot))
