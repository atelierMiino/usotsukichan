from discord.ext import commands

class mail(commands.Cog):
    def __init__(self, company, tracking_number):
        self.company = company
        self.tracking_number = tracking_number
        self.user_id = user_id

def setup(bot: commands.Bot):
    bot.add_cog(usomailcommands(bot))
