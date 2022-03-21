# this file is responsible for managing what cogs are loaded

# discord dependencies
import discord
from discord.ext import commands
# project files
import obj_public.global_var
import obj.tokens

# bot instantiation and Intent configuration
bot_intents = discord.Intents(  messages=True,
                                reactions=True,
                                guilds=True,
                                members=True,
                                voice_states=True)
bot = commands.Bot(  command_prefix=obj_public.global_var.BotDescription.cmd_pre,
                        description=obj_public.global_var.BotDescription.description,
                        intents=bot_intents)

token_request = obj.tokens.BotToken()
token = token_request.get_token('discord')

# run with barebones component
bot.load_extension('base')

# configure extensions
if (obj_public.global_var.ExtenConfig.is_init == False):
    # call configuration function, configure
    obj_public.global_var.ExtenConfig.is_init = True;

# moderation
if  obj_public.global_var.ExtenConfig.is_mod or\
    obj_public.global_var.ExtenConfig.is_log_msg or\
    obj_public.global_var.ExtenConfig.is_log_user:
    bot.load_extension('mod')
# entertainment
if obj_public.global_var.ExtenConfig.is_entertainment:
    bot.load_extension('entertainment')
# voicechat
if obj_public.global_var.ExtenConfig.is_v_chat:
    bot.load_extension('voice')
# stonks
if obj_public.global_var.ExtenConfig.is_stock:
    bot.load_extension('stock')
# mail
if obj_public.global_var.ExtenConfig.is_mail:
    bot.load_extension('mail')
# misc
if obj_public.global_var.ExtenConfig.is_misc:
    bot.load_extension('misc')

bot.run(token)
