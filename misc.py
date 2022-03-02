from discord.ext import commands

class amychancommands(commands.Cog):

    raikohex_id = 0 # add number

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # bully and tease raikoh
    async def bully_raikoh(self, ctx):
        # listen for raikoh's discord ID
        if ctx.author.id == raikohex_id:
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
        if ctx.author.id == self.bot.user.id:
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
