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
        raikoh_obj = obj.userIDs.User()
        raikoh = raikoh_obj.get_id('raikoh')
        if str(ctx.author.id) == raikoh:
        # 5% chance to reply with bully
            bully_meter = random.randint(0, 19)
            if bully_meter == 19:
                mean_phrase = [
                    '🤔',
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
                await ctx.reply(mean_phrase[chaos_meter])

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
                    if c == 'g' or c == 'u':
                        state = 2
                    else:
                        state = 0
                case 2:
                    if c == 'u' or c == 'h':
                        # if message contains guhhh..., guhhh back
                        await ctx.channel.send('guhhh')
                        return
                    else:
                        state = 0

    # samurai die
    async def voice_trigger(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        try:
            voice_channel = ctx.author.voice.channel
            v_client = await voice_channel.connect(timeout=2)
            if 'die' in ctx.content:
                v_client.play(discord.FFmpegPCMAudio('voice/misc/kzdeath.wav'))
            elif 'waow' in ctx.content:
                chaos_meter = random.randint(0, 2)
                wow = ['waow', 'waowww', 'woaw']
                v_client.play(discord.FFmpegPCMAudio('voice/misc/' + wow[chaos_meter] + '.wav'))
            while v_client.is_playing():
                await asyncio.sleep(1)
            await v_client.disconnect()
        except asyncio.TimeoutError:
            pass
        except discord.errors.ClientException:
            pass
        # user who triggered was not in a voice channel, so there is no point
        except AttributeError:
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
            obj_public.global_var.Flags.box_channel_id = v_client.channel.id
            obj_public.global_var.Flags.is_box_active = True
        except AttributeError:
            pass
        except discord.errors.ClientException:
            pass

    # message events
    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.bully_raikoh(ctx)
        await self.guhhh(ctx)
        await self.voice_trigger(ctx)
        if 'box dog' in ctx.content:
            await self.boxdog(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(friend(bot))
