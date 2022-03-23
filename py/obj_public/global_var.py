# public variables for bots

# BOT VARIABLES
class BotDescription:
    cmd_pre = '!'
    cmd_link = 'https://www.google.com'
    description = '''This is the Bot Description'''
    hello = 'This is meant to introduce others when they enter a guild'
    goodbye = 'This is meant to introduce myself when someone leaves a guild'
    introduce = 'This is meant to introduce myself when I join a guild'

# user-toggled VARIABLES
class ExtenConfig:
    # has config been init
    is_init = False
    # has moderation powers
    is_mod = False
    is_log_msg = False
    is_log_user = False
    # has extra powers
    is_entertainment = False
    is_v_chat = True
    is_stock = False
    is_mail = False
    is_misc = True

class Flags:
    is_box_active = False
    box_channel_id = 0
    is_dl = False
    is_muplyr_active = False
