# voicechat based commands

# discord dependancy
import discord
from discord.ext import commands
# queue dependancy
from queue import LifoQueue
# youtube dependancy
import youtube_dl
# os dependancy
import os
# asyncio dependancy
import asyncio
# project dependancy
import obj_public.global_var
import obj.userIDs
import obj_public.error as err
# Voicechat ID Response and recognition
# Playing Music HQ, queueing, skipping, Stop, Pause

# idea: do not call the loop in music player more than one time. Set flag in obj obj_public
# have play only interact to queue
# when started, music player will be independently running. Music player is only allowed to queue

class v_music(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            # contains local directory paths of music
            self.music_queue = LifoQueue(maxsize=50)
            # contains urls of things that are queue'd for download
            self.dl_queue = LifoQueue(maxsize=50)

        # return what client if author is in v_channel
        async def find_guild_client(self, ctx):
            try:
                # try to connect to author's voice channel
                return_val = await ctx.author.voice.channel.connect()
            # if already connected, find the client
            except discord.errors.ClientException:
                return_val = discord.utils.get(self.bot.voice_clients, guild__name=ctx.guild.name)
            # if author is not in voice channel, return Nonetype
            return return_val

        # when called, will queue download
        @commands.command(aliases=['play', 'queue', 'pause', 'resume', 'skip', 'stop'])
        async def interact(self, ctx, url : str):
            # find client
            v_client = await self.find_guild_client(ctx)
            # if there are no clients, then connect
            if v_client is None:
                try:
                    v_client = await ctx.author.voice.channel.connect()
                # if user is not in vchat, then tell them to get into vchat
                except AttributeError:
                    await ctx.reply(err.Voice.join_error)
                return

            cmdcut = ctx.message.content.split(' ')
            cmd = cmdcut[0]

            # only queue music for dl
            if 'play' in cmd or 'queue' in cmd:
                self.dl_queue.put(url)
                if not obj_public.global_var.Flags.is_muplyr_active:
                    await self.music_player(ctx, url, v_client)
                    obj_public.global_var.Flags.is_muplyr_active = True
            # if playing, pause
            elif 'pause' in cmd:
                if v_client.is_playing():
                    v_client.pause()
                else:
                    await ctx.channel.send(obj_public.Voice.pause_error)
            # if pause, then resume
            elif 'resume' in cmd:
                if v_client.is_paused():
                    v_client.resume()
                else:
                    await ctx.channel.send(obj_public.Voice.resume_error)
            # if playing, then stop and play next
            elif 'skip' in cmd:
                pass
            # disconnect
            elif 'stop' in cmd:
                if v_client.is_connected():
                    # clear queues
                    while not self.music_queue.empty():
                        self.music_queue.get()
                    while not self.dl_queue.empty():
                        self.dl_queue.get()
                    await v_client.disconnect()
                    obj_public.global_var.Flags.is_muplyr_active = False
                    ctx.channel.send(obj_public.Voice.stop)
                else:
                    ctx.channel.send(obj_public.Voice.absent_error)

        async def music_player(self, ctx, url : str, v_client):
            # while connected, see if music is queued
            while v_client.is_connected():
                # if dl queue is not empty, dl
                # dl function adds to music queue
                if not self.dl_queue.empty():
                    await self.music_dl(ctx)
                # if music queue is not empty and is not playing, then music
                if not self.music_queue.empty() and not v_client.is_playing() and not v_client.is_paused():
                    await self.music_play(ctx)

        # if dl queue is not empty, download music
        async def music_dl(self, ctx):
            #download the song
            url = self.dl_queue.get()
            os.system('music-dl.bat ' + url)
            # move file to music folder
            ytdl_filename = None
            try:
                os.makedirs('./voice/music/' + str(ctx.guild.id))
            except FileExistsError:
                pass
            for file in os.scandir():
                if file.is_file():
                    if '.py' not in file.name and '.bat' not in file.name:
                        ytdl_filename = file.name
            new_name = './voice/music/' + str(ctx.guild.id) + '/' + ytdl_filename
            # add music path to music queue
            self.music_queue.put(new_name)
            try:
                os.rename(ytdl_filename, new_name)
            except FileExistsError:
                os.remove(ytdl_filename)

        # if music queue is not empty, play music
        async def music_play(self, ctx):
            # if no client, send error
            v_client = await self.find_guild_client(ctx)
            if v_client is None:
                await ctx.channel.send(err.Voice.join_error)
                return
            # if music queue is not empty, get music path and play
            if not self.music_queue.empty():
                prio_song = self.music_queue.get()
                prio_song_split1 = prio_song.split('/')
                prio_song_split2 = prio_song_split1[-1].split('-')
                prio_song_split2.pop(-1)
                try:
                    v_client.play(discord.FFmpegPCMAudio(prio_song))
                    await ctx.channel.send('`' + '-'.join(prio_song_split2) + '`' + err.Voice.playing_prompt)
                except discord.errors.ClientException:
                    await ctx.channel.send(obj_public.error.Voice.absent_error)
                os.remove(prio_song)

class v_misc(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_voice_state_update(self, member, before, after):
            # if the box flag is active, and a member has joined, then have box leave (except box dog)
            box_obj = obj.userIDs.User()
            if obj_public.global_var.Flags.is_box_active and member.id != self.bot.user.id and str(member.id) != box_obj.get_id('boxdog'):
                if after.channel.id == obj_public.global_var.Flags.box_channel_id:
                # find the client that "box dog" has been connected to. Then, disconnect and reset global var
                    for vc in self.bot.voice_clients:
                        if vc.channel.id == obj_public.global_var.Flags.box_channel_id:
                            await vc.disconnect()
                            obj_public.global_var.Flags.box_channel_id = 0
                            obj_public.global_var.Flags.is_box_active = False

def setup(bot: commands.Bot):
    bot.add_cog(v_music(bot))
    bot.add_cog(v_misc(bot))
