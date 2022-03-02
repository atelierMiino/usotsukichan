# this file is responsible for managing what cogs are loaded

# discord dependencies
import discord
from discord.ext import commands
# other project files
import global_var
import entertainment

# bot instantiation and Intent configuration
bot_intents = discord.Intents(  messages=True,
                                reactions=True,
                                guilds=True,
                                members=True)
usobot = commands.Bot(  command_prefix=usotsukichan_init.bot_command_prefix,
                        description=usotsukichan_init.bot_description,
                        intents=bot_intents)
# barebones component
usobot.load_extension('base')
usobot.run(usotsukichan_init.DISCORD_BOT_TOKEN)

# configure extensions

# moderation
# toggle message logging
# toggle user entry / departure logging_true
# "X commands are <ON/OFF>. Toggle <OFF/ON?"
# if toggle true & command on, then toggle off, else toggle on
# if toggle on true, toggle specific commands
usobot.load_extension('mod')
# entertainment
usobot.load_extension('entertainment')
# voicechat
usobot.load_extension('voice')
# stonks

# mail
usobot.load_extension('mail')
# misc
