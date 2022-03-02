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

# run with barebones component
bot.load_extension('base')
bot.run(global_var.token)

# configure extensions

# moderation
# toggle message logging
# toggle user entry / departure logging_true
# "X commands are <ON/OFF>. Toggle <OFF/ON?"
# if toggle true & command on, then toggle off, else toggle on
# if toggle on true, toggle specific commands
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
