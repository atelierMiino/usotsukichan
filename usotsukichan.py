# main usotsukichan file. used to load and unload cogs based on configuration
import discord
from discord.ext import commands
# usotsukichan dependencies
import usotsukichan_init
import usotsukichan_commands
# Bot instantiation and Intent configuration
bot_intents = discord.Intents(  messages=True,
                                reactions=True,
                                guilds=True,
                                members=True)
usobot = commands.Bot(  command_prefix=usotsukichan_init.bot_command_prefix,
                        description=usotsukichan_init.bot_description,
                        intents=bot_intents)

usobot.load_extension('usotsukichan_configuration')

usobot.load_extension('usotsukichan_commands')
usobot.load_extension('usotsukichan_commands_voice')
usobot.load_extension('usotsukichan_moderation')

usobot.run(usotsukichan_init.DISCORD_BOT_TOKEN)
