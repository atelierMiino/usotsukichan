from discord.ext import commands
import random
import json
from types import SimpleNamespace

import global_var

class entertainment(commands.Cog):
    roll_error_response = '(Syntax: {}roll NdN NdN NdN ...)'.format(global_var.cmd_pre)
    _8ball_error_response = '(Syntax: {}8ball <question>)'.format(global_var.cmd_pre)

    def __init__(self, bot):
        self.bot = bot

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
    async def quote(self, ctx):
        file = open('quotes.json')
        data = json.load(file, object_hook = lambda d: SimpleNamespace(**d))
        rint = random.randint(0, 36)
        phrase = ('```{}```\n**{}**, *{}.*'.format(data.Compilation[rint].Quote, data.Compilation[rint].Author, data.Compilation[rint].Occupation))
        if data.Compilation[rint].Works != 'Null':
            phrase += ' *Known for {}*'.format(data.Compilation[rint].Works)
        await ctx.channel.send(phrase)

def setup(bot: commands.Bot):
    bot.add_cog(usocommands(bot))
    bot.add_cog(amychancommands(bot))
