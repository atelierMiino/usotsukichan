'''Voicechat commands, mainly used to play music or sounds.'''


import discord
import discord.ui.view
from discord.ext import commands
import asyncio
import functools
import itertools
import math
import youtube_dl
from async_timeout import timeout
from exceptions import YTDLError
from exceptions import VoiceError

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda:''


class YTDL(discord.PCMVolumeTransformer):
    YTDL_opt = {
        'format':'worstaudio/worst',
        'extractaudio':True,
        'audioformat':'mp3',
        'outtmpl':'%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames':True,
        'noplaylist':True,
        'nocheckcertificate':True,
        'ignoreerrors':False,
        'logtostderr':False,
        'quiet':True,
        'no_warnings':True,
        'default_search':'ytsearch',
        'source_address':'0.0.0.0',
    }

    FFMPEG_opt = {
        'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options':'-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_opt)

    def __init__(self, ctx : commands.Context, src : discord.FFmpegPCMAudio, *, data : dict, volume : float = 0.5):
        super().__init__(src, volume)

        self.requester = ctx.author
        self.channel = ctx.channel

        self.metadata = data
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.web_url = data.get('web_url')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def init_src(cls, ctx : commands.Context, keywords : str, *, loop : asyncio.BaseEventLoop = None):
        '''Converts keywords to PCM Audio streams.'''

        loop = loop or asyncio.get_event_loop()

        # Attempt to retrieve web data based off search keywords. If Multiple entries, save first entry. 
        # Else, if single entry, simply save. If no entry, raise error.
        partial = functools.partial(cls.ytdl.extract_info, keywords, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('No matches for `{}`'.format(keywords))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('No matches for `{}`'.format(keywords))

        # Attempt to retrieve stream data based off web url. If Multiple entries, save first entry. 
        # Else, if single entry, simply save. If no entry, raise error.
        web_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, web_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Unable to fetch `{}`'.format(web_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Unable to fetch `{}` from index'.format(web_url))
        
        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_opt), data=info)

    @staticmethod
    def parse_duration(dur : int):
        '''Converts integer seconds into human-readable d/h/m/s string format.'''

        if dur > 0:
            mins, secs = divmod(dur, 60)
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)

            dur = []
            if days > 0:
                dur.append('{}'.format(days))
            if hours > 0:
                dur.append('{}'.format(hours))
            if mins > 0:
                dur.append('{}'.format(mins))
            if secs > 0:
                dur.append('{}'.format(secs))
            
            value = ':'.join(dur)
        
        elif dur == 0:
            value = "LIVE"
        
        return value


class Sound:
    __slots__ = ('src', 'requester')

    def __init__(self, src:YTDL):
        self.src = src
        self.requester = src.requester
    
    def create_embed(self):
        embed = (discord.Embed(title='Now playing', description='```css\n{0.src.title}\n```'.format(self), color=discord.Color.blurple())
                .add_field(name='Duration', value=self.src.duration)
                .add_field(name='Requested by', value=self.requester.mention)
                .add_field(name='Uploader', value='[{0.src.uploader}]({0.src.uploader_url})'.format(self))
                .add_field(name='URL', value='[Click]({0.src.stream_url})'.format(self))
                .set_thumbnail(url=self.src.thumbnail)
                .set_author(name=self.requester.name, icon_url=self.requester.avatar.url))
        return embed


class SoundQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def remove(self, index : int):
        del self._queue[index]


class VoiceView(discord.ui.view.View):
    def __init__(self, ctx : commands.Context):
        super().__init__(timeout=180)
        self._ctx = ctx
        self._style = discord.ButtonStyle.blurple

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value : discord.ButtonStyle):
        self._style = value

    async def on_timeout(self):
        self.stop()

    @discord.ui.button(style = style, emoji = '⏯')
    async def play_pause(self, button:discord.ui.Button, interaction:discord.Interaction):
        '''Toggle play / pause'''

        if self._ctx.voice_state.is_playing and self._ctx.voice_state.voice.is_playing():
            self._ctx.voice_state.voice.pause()
        else:
            self._ctx.voice_state.voice.resume()
    
    @discord.ui.button(style = style, emoji = '⏭')
    async def skip(self, button:discord.ui.Button, interaction:discord.Interaction):
        '''Call the skip function in VoiceCMD'''

        self._skip(self.ctx)
        self.disabled = True

    @discord.ui.button(style = style, emoji = '🔁')
    async def loop(self, button:discord.ui.Button, interaction:discord.Interaction):
        '''Call the loop function in VoiceCMD'''

        self._loop(self.ctx)
        
    @discord.ui.button(style = style, emoji = '⏹')
    async def stop(self, button:discord.ui.Button, interaction:discord.Interaction):
        '''Clear the view items, then call the stop function in VoiceCMD.
        Once done, disable all buttons in VoiceView'''

        await self._ctx.voice_state.voice.stop()
        self.disabled = True
        self.stop()


class VoiceState:
    def __init__(self, bot : commands.Bot, ctx : commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.sounds = SoundQueue()
        self.exists = True

        self._loop = False
        self._autoplay = True
        self._volume = 0.25
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value : bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value : float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()
            self.now = None

            if self.loop == False:
                # Disconnect if queue is empty after a minute
                try:
                    async with timeout(60):
                        self.current = await self.sounds.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    self.exists = False
                    return
                
                self.current.src.volume = self._volume
                self.voice.play(self.current.src, after=self.play_next_song)
                '''button_view = VoiceView(self._ctx)'''
                await self.current.src.channel.send(embed=self.current.create_embed())
                '''await self.current.src.channel.send(view=button_view)'''
            
            # If the song is looped, just play song over
            elif self.loop == True:
                self.now = discord.FFmpegPCMAudio(self.current.src.stream_url, **YTDL.FFMPEG_opt)
                self.voice.play(self.now, after=self.play_next_song)
            
            await self.next.wait()

    def play_next_song(self, error = None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.sounds.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class VoiceCMD(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx : commands.Context):
        '''Returns VoiceState instance that is associated with guild.'''

        # If no VoiceState instances are associated with guild, initialize
        # a new VoiceState.
        state = self.voice_states.get(ctx.guild.id)
        if not state or not state.exists:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx : commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx : commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx : commands.Context, error:commands.CommandError):
        await ctx.send('An error occurred:{}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx : commands.Context):
        '''If not in voice channel, join voice channel
        associated with command user.'''

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    async def _leave(self, ctx : commands.Context):
        '''Dismiss queue and exits.'''

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='pause', aliases=['pa'])
    async def _pause(self, ctx : commands.Context):
        '''Pauses voice output.'''

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('✅')

    @commands.command(name='resume', aliases=['re', 'res'])
    async def _resume(self, ctx : commands.Context):
        '''Resumes voice output.'''

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('✅')

    @commands.command(name='stop')
    async def _stop(self, ctx : commands.Context):
        '''Dismiss queue.'''

        ctx.voice_state.sounds.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('✅')

    @commands.command(name='skip', aliases=['s'])
    async def _skip(self, ctx : commands.Context):
        '''Skip current voice output'''

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        ctx.voice_state.skip()
        await ctx.message.add_reaction('✅')

    @commands.command(name='queue')
    async def _queue(self, ctx : commands.Context, *, page : int = 1):
        '''Shows registered items.'''

        if len(ctx.voice_state.sounds) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.sounds) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.sounds[start:end], start=start):
            queue += '`{0}.` [**{1.src.title}**]({1.src.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.sounds), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='loop')
    async def _loop(self, ctx : commands.Context):
        '''Loops current Sound instance.'''

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')
        await ctx.send('Looping a song is now turned ' + ('on' if ctx.voice_state.loop else 'off') )

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx : commands.Context, *, search : str):
        '''Registers Sounds onto the queue.
        youtube_dl compatible sites: https://rg3.github.io/youtube-dl/supportedsites.html
        '''

        async with ctx.typing():
            try:
                src = await YTDL.init_src(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request:{}'.format(str(e)))
            else:
                if not ctx.voice_state.voice:
                    await ctx.invoke(self._join)

                song = Sound(src)
                await ctx.voice_state.sounds.put(song)
                await ctx.send('{} Registered'.format(str(src)))
            
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx : commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')


def setup(bot : commands.Bot):
    bot.add_cog(VoiceCMD(bot))
