# voicechat based commands

# discord dependancy
from discord.ext import commands
# queue dependancy
from queue import LifoQueue
# youtube dependancy
import youtube_dl
# os dependancy
import os
# project dependancy
import obj_public.global_var
import obj_public.error as err
# Voicechat ID Response and recognition
# Playing Music HQ, queueing, skipping, Stop, Pause
class v_music(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            # contains local directory paths of music
            self.music_queue = LifoQueue(maxsize=50)

        def song_dl(self, ctx, url : str):
            #download the song
            ytdl_opts = {
                'format' : 'bestaudio/best',
                'postprocessors' : [{
                    'key' : 'FFmpegExtractAudio',
                    'preferredcodec' : 'mp3',
                    'preferredquality' : '192',
                }],
            }
            youtube_dl.YoutubeDL(ytdl_opts).download([url])
            # organize download
            ytdl_filename = None
            os.mkdir('./voice/' + ctx.guild.id)
            with os.scandir() as files:
                for file in files:
                    if '.mp3' in file
                    ytdl_filename = file
            new_name = './voice/' + ctx.guild.id + '/' + ytdl_filename
            self.music_queue.put(new_name)
            os.rename('*.mp3', new_name)

        @commands.command()
        async def play(self, ctx, url : str):
            # try connect
            try:
                v_client = ctx.author.voice.channel.connect()
                # if no client was found, give error
                if v_client == None:
                    ctx.channel.send(err.VoiceError.join_error)
                # remove previous song download
                os.remove(prio_song)
                # play music
                prio_song = self.music_queue.get()

            except discord.errors.ClientException:
                pass

        @commands.command()
        async def queue(self, ctx, url):
            # add to queue

        @commands.command()
        async def skip(self, ctx):
            # stop playing music
            v_client = discord.utils.get(bot.voice_clients, guild=ctx.author.guild.name)
            if v_client == None:
                ctx.channel.send(err.VoiceError.absent_error)
            if v_client.is_playing() or v_client.is_paused():
                v_client.stop()
            # play next music

        @commands.command()
        async def stop(self, ctx):
            # refresh queue
            while ~self.music_queue.empty():
                self.music_queue.get()
            # try disconnect
            v_client = discord.utils.get(bot.voice_clients, guild=ctx.author.guild.name)
            if v_client == None:
                ctx.channel.send(err.VoiceError.absent_error)
            elif v_client.is_connected():
                if v_client.is_playing():
                    # halt music playing
                    v_client.stop()
                await v_client.disconnect()

        @commands.command()
        async def pause(self, ctx):
            # halt music playing
            v_client = discord.utils.get(bot.voice_clients, guild=ctx.author.guild.name)
            if v_client == None:
                ctx.channel.send(err.VoiceError.absent_error)
            elif v_client.is_playing():
                v_client.pause()
            else:
                ctx.channel.send(err.VoiceError.pause_error)

        @commands.command()
        async def resume(self, ctx):
            # continue music playing
            v_client = discord.utils.get(bot.voice_clients, guild=ctx.author.guild.name)
            if v_client == None:
                ctx.channel.send(err.VoiceError.absent_error)
            elif v_client.is_paused():
                v_client.resume()
            else:
                ctx.channel.send(err.VoiceError.resume_error)

class v_misc(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_voice_state_update(self, member, before, after):
            # if the box flag is active, and a member has joined, then have box leave
            if obj_public.global_var.ExtenConfig.is_box_active and member.id != self.bot.user.id:
                if before.channel == None and (after.channel.id == obj_public.global_var.ExtenConfig.box_channel_id):
                # find the client that "box dog" has been connected to. Then, disconnect and reset global var
                    for vc in self.bot.voice_clients:
                        if vc.channel.id == obj_public.global_var.ExtenConfig.box_channel_id:
                            await vc.disconnect()
                            obj_public.global_var.ExtenConfig.box_channel_id = 0
                            obj_public.global_var.ExtenConfig.is_box_active = False

def setup(bot: commands.Bot):
    bot.add_cog(v_music(bot))
    bot.add_cog(v_misc(bot))
