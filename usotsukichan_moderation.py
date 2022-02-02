from discord.ext import commands
import usotsukichan_init

class usomod(commands.Cog):
    def __init__(self, usobot):
        self.usobot = usobot
    # Guild member joining and leaving reactions
    # Chat purging
    # Chat Monitoring / Word Blacklisting, URL Blacklisting

class usolog(commands.Cog):
    logconf_error_response = '(Syntax: !logconf ON/OFF Channel_ID)'

    def __init__(self, usobot):
        self.usobot = usobot

    # pushes log entry to logging get_channel
    async def push_entry(self, entry):
        await self.usobot.get_channel(usotsukichan_init.logging_channel).send(entry)

    # log new messages
    @commands.Cog.listener()
    async def on_message(self, message):
        # if logging data is on, log data into guild channel
        if message.author.id == self.usobot.user.id:
            return
        if (usotsukichan_init.logging_true):
            dt = message.created_at
            dy = dt.year
            dm = dt.month
            dd = dt.day
            th = dt.hour
            tm = dt.minute
            ts = dt.second
            log_entry = '{datetime} \n**{author}** ( *user ID {author_ID}* )\n__said__ ( *message ID {message_ID}* ) : \n```{message}```in #{channel}'.format(
            datetime = '{}/{}/{} - {}:{}:{} UTC'.format(
            dy, dm, dd, th, tm, ts
            ),
            author = message.author.name,
            author_ID = message.author.id,
            message_ID = message.id,
            message = message.content,
            channel = message.channel
            )
            await self.push_entry(log_entry)

    # log edited messages
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # if logging data is on, and edit is tripped, log data into guild channel
        if (usotsukichan_init.logging_true):
            edit_entry = '**{author}** ( *user ID {author_ID}* )\n__edited__ ( *message ID {message_ID}* ) from :\n```{old_message}```to\n```{new_message}```in #{channel}'.format(
            author = before.author.name,
            author_ID = before.author.id,
            message_ID = before.id,
            #old_message = self.old_message_lookup(ctx, ctx.message_id),
            old_message = before.content,
            new_message = after.content,
            channel = before.channel
            )
            await self.push_entry(edit_entry)

    # log deleted messages
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # if logging data is on, and delete is tripped, log data into guild channel
        if (usotsukichan_init.logging_true):
            edit_entry = '**{author}** ( *user ID {author_ID}* )\n__deleted__ ( *message ID {message_ID}* ) :\n```{old_message}```in #{channel}'.format(
            author = message.author.name,
            author_ID = message.author.id,
            message_ID = message.id,
            # old_message = self.old_message_lookup(ctx, ctx.message_id),
            old_message = message.content,
            channel = message.channel,
            )
            await self.push_entry(edit_entry)

    # log users coming / going

    # configure logging
    @commands.command(name='logconf')
    async def logging_config(self, ctx, status, channel_id):
        if status == 'on' or status == 'ON' or status == 'On' or status == 'yes' or status == 'YES' or status == 'Yes' or status == 'y' or status == 'Y':
            usotsukichan_init.logging_true = True
            try:
                logging_channel = channel_id
            except:
                await ctx.channel.send('Baka!! No channel ID was given. How am I supposed to know what channel I\'m supposed to log to?\n {}'.format(logconf_error_response))
        elif status == 'off' or status == 'OFF' or status == 'Off' or status == 'no' or status == 'NO' or status == 'No' or status == 'n' or status == 'N':
            usotsukichan_init.logging_true = False
        else:
            await ctx.channel.send('I-I guess you don\'t know how to use this command, right? =w=\'\'\n {}'.format(logconf_error_response))

def setup(bot: commands.Bot):
    bot.add_cog(usomod(bot))
    bot.add_cog(usolog(bot))
