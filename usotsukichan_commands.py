from discord.ext import commands
import random
import json
from types import SimpleNamespace

import usotsukichan_init
# bot rolling die feature
# Inspirational hitler quotes disguised as modern celebrity quotes

class usocommands(commands.Cog):
    roll_error_response = 'I couldn\'t roll those numbers. Please list rolls in NdN format >__<\'\' \n(Syntax: {}roll NdN NdN NdN ...)'.format(usotsukichan_init.bot_command_prefix)
    _8ball_error_response = 'W-what did you want to ask the 8ball? @__@ \n(Syntax: {}8ball <question>)'.format(usotsukichan_init.bot_command_prefix)

    def __init__(self, usobot):
        self.usobot = usobot
        self._last_member = None

    # bot on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot: {} is now Online.'.format(self.usobot.user))

    # bot on_disconnect
    @commands.Cog.listener()
    async def on_disconnect(self):
        print('Bot: {} is now Offline.'.format(self.usobot.user))

    # roll NdN NdN NdN ...
    @commands.command()
    async def roll(self, ctx, *, ndn: str):
        if num_diff_die == 0:
            await ctx.channel.send(roll_error_response)
            return
        # declare variables and lists
        start = 0
        num_diff_die = ndn.count('d')
        total_roll_yield = '{}\'s {} roll result:\n'.format(ctx.author.name, ndn)
        # for each roll instance (NdN), roll a certain amount of times, defined by the variable num_rolls
        while num_diff_die > 0:
            try:
                # find d's position in the string, and once found, find NdN positions and save integer values into num_rolls & dice_size
                d_position = ndn.index('d', start, len(ndn))
            except:
                await ctx.channel.send(roll_error_response)
                return
            try:
                num_rolls = int(ndn[d_position - 1])
                dice_size = int(ndn[d_position + 1])
            except:
                await ctx.channel.send(roll_error_response)
                return
            # generate random number between 1 and dice_size until num_rolls reaches 0
            while num_rolls > 0:
                try:
                    roll_yield = random.randint(1, dice_size)
                except:
                    await ctx.channel.send(error_response)
                    return
                # format phrasing
                declaration_phrase = '{}d{} : {} \n'.format(num_rolls, dice_size, roll_yield)
                total_roll_yield += declaration_phrase
                num_rolls -= 1
            # next starting position for index function is after the previous index
            start = d_position + 1
            # decrement roll instance
            num_diff_die -= 1
        # return full phrasing
        await ctx.channel.send(total_roll_yield)

    # 8ball response
    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question: str):
        if len(question) <= 0:

            await ctx.channel.send(_8ball_error_response)
        # 0-9 affirmative answers
        # 10-14 non-commital answers
        # 15-19 negative answers
        possible_answers = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        await ctx.channel.send(possible_answers[random.randint(0, 19)])

    # inspirtational quotes
    @commands.command()
    async def inspiration(self, ctx):
        file = open('quotes.json')
        data = json.load(file, object_hook = lambda d: SimpleNamespace(**d))
        rint = random.randint(0, 36)
        phrase = ('```{}```\n**{}**, *{}.*'.format(data.Compilation[rint].Quote, data.Compilation[rint].Author, data.Compilation[rint].Occupation))
        if data.Compilation[rint].Works != 'Null':
            phrase += ' *Known for {}*'.format(data.Compilation[rint].Works)
        await ctx.channel.send(phrase)

class amychancommands(commands.Cog):
    def __init__(self, usobot):
        self.usobot = usobot
        self._last_member = None

    # bully and tease raikoh
    async def bully_raikoh(self, ctx):
        # listen for raikoh's discord ID
        if ctx.author.id == usotsukichan_init.raikohex_id:
        # 5% chance to reply with bully
            bully_meter = random.randint(0, 19)
            if bully_meter == 19:
                mean_phrase = [
                    '{thinking_emoji}'.format('\U0001F914'),
                    'Of course you would say that..',
                    'just like the simulations..',
                    'oh here we go again xd',
                    'toxic... and mean!!',
                    'sounds homoerotic',
                    'typical raikoh',
                    'cute..',
                    'Hi',
                    '?'
                ]
                chaos_meter = random.randint(0, 9)
                ctx.reply(mean_phrase[chaos_meter])

    # guhhh responder
    async def guhhh(self, ctx):
        # if a character is g, continue if g or u
        # if a character is u, continue if u or h
        # if at any point a character breaks, return to case g
        if ctx.author.id == self.usobot.user.id:
            return
        state = 0
        for c in ctx.content:
            match state:
                case 0:
                    if c == 'g':
                        state = 1
                case 1:
                    if c == 'g':
                        pass
                    elif c == 'u':
                        state = 2
                    else:
                        state = 0
                case 2:
                    if c == 'u':
                        pass
                    elif c == 'h':
                        # if message contains guhhh..., guhhh back
                        await ctx.channel.send('guhhh')
                        return
                    else:
                        pass

    # message events
    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bully_raikoh(message)
        await self.guhhh(message)

def setup(bot: commands.Bot):
    bot.add_cog(usocommands(bot))
    bot.add_cog(amychancommands(bot))
