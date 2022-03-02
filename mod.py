from discord.ext import commands
import usotsukichan_init

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Chat purging
    # Chat Monitoring / Word Blacklisting, URL Blacklisting

class message_log(commands.Cog):
    logconf_error_response = '(Syntax: !logconf ON/OFF Channel_ID)'

    def __init__(self, bot):
        self.bot = bot

    # pushes log entry to logging get_channel
    async def push_entry(self, entry):
        await self.bot.get_channel(usotsukichan_init.logging_channel).send(entry)

    # log new messages
    @commands.Cog.listener()
    async def on_message(self, message):
        # if logging data is on, log data into guild channel
        if message.author.id == self.bot.user.id:
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

class user_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # log users coming / going
    @commands.Cog.listener()
    async def on_member_join(self, message):
        if message.author.id != self..user.id:
            await message.channel.send('W-Welcome to {}, {}... you bastard!!', message.guild.id, message.author.id)
        else:
            await message.channel.send('H-hewoo. I\'m new here... my name is {}. You can see my commands @ {}', self.bot.user.id, usotsukichan_init.CMD_DOCUMENTATION_WEBSITE)

    @commands.Cog.listener()
    async def on_member_remove(self, message):
        if message.author.id != self.bot.user.id:
            await message.channel.send('CYA {}... you bastard!!',message.author.id)

def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))
    bot.add_cog(message_log(bot))
    bot.add_cog(user_log(bot))
