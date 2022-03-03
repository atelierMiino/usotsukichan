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
bot = commands.Bot(  command_prefix=global_var.cmd_pre,
                        description=global_var.description,
                        intents=bot_intents)

# token will be read from a json in the future to avoid security threats
token = 'x'

# run with barebones component
bot.load_extension('base')
bot.run(token)

# configure extensions
if (global_var.is_init == False):
    # call configuration function, configure
    global_var.is_init = True;

# moderation
if global_var.is_mod or global_var.is_log_msg or global_var.is_log_user:
    bot.load_extension('mod')
# entertainment
if global_var.is_entertainment:
    bot.load_extension('entertainment')
# voicechat
if global_var.is_v_chat:
    bot.load_extension('voice')
# stonks
if global_var.is_stock:
    bot.load_extension('stock')
# mail
if global_var.is_mail:
    bot.load_extension('mail')
# misc
if global_var.is_misc:
    bot.load_extension('misc')
