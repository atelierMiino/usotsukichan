# truly random commands, suggested by friends

# discord dependancies
import discord
from discord.ext import commands
# random dependancy
import random
# asyncio dependancy
import asyncio
# project dependancy
import obj.userIDs
import obj_public.global_var

class friend(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # bully and tease raikoh
    async def bully_raikoh(self, ctx):
        # listen for raikoh's discord ID
        raikoh = obj.userIDs.user()
        if ctx.author.id == raikoh.get_id('raikoh'):
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

    # samurai die
    async def die(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        src = await discord.FFmpegOpusAudio.from_probe('kzdeath.wav')
        voice_channel = ctx.author.voice.channel
        try:
            v_client = await voice_channel.connect(timeout=2)
            v_client.play(src)
            while v_client.is_playing():
                await asyncio.sleep(1)
            await v_client.disconnect()
        except asyncio.TimeoutError:
            pass
        except discord.errors.ClientException:
            pass

    # classic box dog
    async def boxdog(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return

        voice_channel = discord.utils.get(ctx.guild.voice_channels, members=[])
        if voice_channel == None:
            return
        try:
            v_client = await voice_channel.connect(timeout=None, reconnect=True)
            obj_public.global_var.ExtenConfig.box_channel_id = v_client.channel.id
            obj_public.global_var.ExtenConfig.is_box_active = True
        except AttributeError:
            pass

    # message events
    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.bully_raikoh(ctx)
        await self.guhhh(ctx)
        if 'die' in ctx.content:
            await self.die(ctx)
        if 'box dog' in ctx.content:
            await self.boxdog(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(friend(bot))
