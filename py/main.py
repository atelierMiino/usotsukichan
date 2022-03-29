'''This file is responsible for loading extensions and running the bot.'''


import discord
from discord.ext import commands

import obj_public.variables
import obj.private_user_data

# bot instantiation and Intent configuration
bot_intents = discord.Intents(  messages=True,
                                message_content=True,
                                reactions=True,
                                guilds=True,
                                members=True,
                                voice_states=True,
                                webhooks=True,
                                typing=True)

bot = commands.Bot(  command_prefix=obj_public.variables.Metadata.cmd_pre,
                        description=obj_public.variables.Metadata.description,
                        intents=bot_intents)

extensions = {
    'base' : True,
    'moderation' : False,
    'entertainment' : False,
    'voice' : True,
    'stocks' : False,
    'mail' : False,
    'misc' : True
}

moderation_levels = {
    'mod_commands' : False,
    'log_message' : False,
    'log_guild_movement' : False
}

mod_lvl = moderation_levels.values()
for lvl in mod_lvl:
    extensions['moderation'] = extensions['moderation'] or lvl

for ext in extensions:
    if extensions[ext]:
        bot.load_extension(ext)
        print('{} has been loaded.\n'.format(ext))

token = obj.private_user_data.Token.discord_token
bot.run(token)
