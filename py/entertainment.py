'''Misc user-interaction based commands'''

from discord.ext import commands
import random
import json
from types import SimpleNamespace
from obj_public.variables import Metadata
from exceptions import EntertainmentError

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx : commands.Context, *, ndn : str):
        '''Used to roll dice.'''

        if num_diff_die == 0:
            raise EntertainmentError('(Syntax: {}roll NdN NdN NdN ...)'.format(Metadata.cmd_pre))

        start = 0
        num_diff_die = ndn.count('d')
        total_roll_yield = '{}\'s {} roll result:\n'.format(ctx.author.name, ndn)
        # for each roll instance (NdN), roll a certain amount of times, defined by the variable num_rolls
        # find d's position in the string, and once found, find NdN positions and save integer values into num_rolls & dice_size
        # generate random number between 1 and dice_size until num_rolls reaches 0
        while num_diff_die > 0:
            try:
                d_position = ndn.index('d', start, len(ndn))
            except:
                raise EntertainmentError('(Syntax: {}roll NdN NdN NdN ...)'.format(Metadata.cmd_pre))

            try:
                num_rolls = int(ndn[d_position - 1])
                dice_size = int(ndn[d_position + 1])
            except:
                raise EntertainmentError('(Syntax: {}roll NdN NdN NdN ...)'.format(Metadata.cmd_pre))

            while num_rolls > 0:
                try:
                    roll_yield = random.randint(1, dice_size)
                except:
                    raise EntertainmentError('(Syntax: {}roll NdN NdN NdN ...)'.format(Metadata.cmd_pre))

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

    @commands.command(name='8ball')
    async def _8ball(self, ctx : commands.Context, *, question : str):
        '''Returns random 8ball responses to user questions.'''

        if len(question) <= 0:
            raise EntertainmentError('(Syntax: {}8ball <question>)'.format(Metadata.cmd_pre))

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

    @commands.command()
    async def quote(self, ctx):
        file = open('quotes.json')
        data = json.load(file, object_hook = lambda d : SimpleNamespace(**d))
        rint = random.randint(0, 36)
        phrase = ('```{}```\n**{}**, *{}.*'.format(data.Compilation[rint].Quote, data.Compilation[rint].Author, data.Compilation[rint].Occupation))
        if data.Compilation[rint].Works != 'Null':
            phrase += ' *Known for {}*'.format(data.Compilation[rint].Works)
        await ctx.channel.send(phrase)

def setup(bot :  commands.Bot):
    bot.add_cog(Entertainment(bot))
