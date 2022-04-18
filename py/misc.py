'''Random Functions suggested by friends. Not intended for general
use.'''


import discord
from discord.ext import commands

import random

import asyncio

import obj.private_user_data
import obj_public.variables

class friend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def bully_raikoh(self, ctx):
        '''Function suggested by Amy. Objective is to
        bully and tease a friend, by the name Raikoh at random
        messages.'''

        raikoh = obj.private_user_data.UserID.raikoh
        if str(ctx.author.id) == raikoh:
        # 5% chance to bully
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

    async def guhhh(self, ctx):
        '''Function suggested by Amy.Every time any instance of guh
        is mentioned, bot will respond back with a guh.'''

        if ctx.author.id == self.bot.user.id:
            return
        # If a character is g, continue if g or u.
        # If a character is u, continue if u or h.
        # If at any point a character breaks, return to case g.
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
                        await ctx.channel.send('guhhh')
                        return
                    else:
                        state = 0

    async def voice_trigger(self, ctx):
        '''Function suggested by Lexi and Amy respectively. On mention
        of die, plays Katana Zero in relevant chat, else if waow, plays
        waow voicelines.'''

        if ctx.author.id == self.bot.user.id:
            return

        try:
            voice_channel = ctx.author.voice.channel
        # Except catches when author is not in channel
        except AttributeError:
            return
        
        else:
            v_client = None
            v_list = ['die', 'waow', 'hello', 'box eulogy']

            for word in v_list:
                if word in ctx.content:
                    break
                elif word == v_list[-1]:
                    return

            # Katana Zero
            if v_list[0] in ctx.content:
                try:
                    v_client = await voice_channel.connect(timeout=2)
                # Except catches when bot is already in v chat
                except discord.errors.ClientException:
                    pass

                v_client.play(discord.FFmpegPCMAudio('py/v_misc/kz_death.mp3'))

            # Waow
            elif v_list[1] in ctx.content:
                try:
                    v_client = await voice_channel.connect(timeout=2)
                except discord.errors.ClientException:
                    pass

                wow = ['k_waow', 'ar_waow', 'a_waow', 't_waow', 'l_waow', 'ani_waow', 'e_waow']
                chaos_meter = random.randint(0, len(wow) - 1)
                v_client.play(discord.FFmpegPCMAudio('py/v_misc/waow/' + wow[chaos_meter] + '.mp3'))

            # Hello
            elif v_list[2] in ctx.content:
                try:
                    v_client = await voice_channel.connect(timeout=2)
                except discord.errors.ClientException:
                    pass

                v_client.play(discord.FFmpegPCMAudio('py/v_misc/hi_hello.m4a'))

            # Box eulogy
            elif v_list[3] in ctx.content:
                try:
                    v_client = await voice_channel.connect(timeout=2)
                except discord.errors.ClientException:
                    pass

                v_client.play(discord.FFmpegPCMAudio('py/v_misc/box_eulogy.mp3'))
            try:
                while v_client.is_playing():
                    await asyncio.sleep(1)
                await v_client.disconnect()
            except AttributeError:
                pass

    async def boxdog(self, ctx):
        '''Function idea by Kaitlyn. Mimics boxdog's behavior in
        voice chats. Will join a server VC and disconnect if someone
        unfamiliar joins. The only person that is "familiar" would be
        boxdog herself.'''

        if ctx.author.id == self.bot.user.id:
            return

        # Sit in an empty voice channel.
        if 'box dog' in ctx.content:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, members=[])
            if voice_channel == None:
                return
            try:
                v_client = await voice_channel.connect(timeout=None, reconnect=True)
                obj_public.variables.Flags.box_channel_id = v_client.channel.id
                obj_public.variables.Flags.is_box_active = True
            except AttributeError:
                pass
            except discord.errors.ClientException:
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''Meant to work in conjunction with boxdog(). If boxdog flag is set,
        then that means boxdog is in a channel. Thus, boxdog needs to look out
        for people joining voice chats in server.'''

        box_dog = obj.private_user_data.UserID.boxdog
        box_flag = obj_public.variables.Flags.is_box_active
        member_id = member.id
        bot_id = self.bot.user.id

        if box_flag and member_id != bot_id and str(member_id) != box_dog:
            if after.channel.id == obj_public.variables.Flags.box_channel_id:
                for vc in self.bot.voice_clients:
                    if vc.channel.id == obj_public.variables.Flags.box_channel_id:
                        await vc.disconnect()
                        obj_public.variables.Flags.box_channel_id = 0
                        obj_public.variables.Flags.is_box_active = False

        # If box dog leaves chat for some reass
        elif box_flag and member_id == bot_id and after.channel is None:
            obj_public.variables.Flags.box_channel_id = 0
            obj_public.variables.Flags.is_box_active = False
                        
    # message events
    @commands.Cog.listener()
    async def on_message(self, ctx):
        '''On each message, run these function checks.'''

        await self.bully_raikoh(ctx)
        await self.guhhh(ctx)
        await self.voice_trigger(ctx)
        await self.boxdog(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(friend(bot))
