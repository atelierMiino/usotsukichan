# this file is dedicated to user moderation. This information ideally should only be available to server moderators and admins

from discord.ext import commands
import usotsukichan_init

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Chat purging
    # Chat Monitoring / Word Blacklisting, URL Blacklisting

class message_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pushes log entry to logging get_channel
    async def push_entry(self, entry):
        await self.bot.get_channel(global_var.log_channel).send(entry)

    # log new messages
    @commands.Cog.listener()
    async def on_message(self, message):
        # if logging data is on, log data into guild channel
        if message.author.id == self.bot.user.id:
            return

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
        if message.author.id != self.bot.user.id:
            await message.channel.send('{}. Welcome to {}, {}', global_var.hello, message.guild.id, message.author.id)
        else:
            await message.channel.send('{}. Thank you for inviting me to {}', global_var.introduce, message.guild.id)

    @commands.Cog.listener()
    async def on_member_remove(self, message):
        if message.author.id != self.bot.user.id:
            await message.channel.send('{}, {}', global_var.goodbye, message.author.id)

def setup(bot: commands.Bot):
    if global_var.is_mod:
        bot.add_cog(moderation(bot))
    if global_var.is_log_msg:
        bot.add_cog(message_log(bot))
    if global_var.is_log_user:
        bot.add_cog(user_log(bot))
