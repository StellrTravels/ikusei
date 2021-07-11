import discord
from discord.ext import commands
import platform
import praw
import random
from praw import reddit

from praw.reddit import Submission

import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    reddit = praw.Reddit(
        client_id='deR1ApeQ_O0iO4wG3LbhyQ',
        client_secret='WijUJsR6z3mw5Z7M_NqqDOvC7iE3hA',
        user_agent='memescript by u/Laszlohh'
    )


    @commands.command()
    async def meme(self, ctx):
        memes_submissions = reddit.Subreddit('me_irl')
        post_to_pick = random.randint(1, 10)
        for i in range(1, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url)

    @commands.command()
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        
        embed = discord.Embed(
            title=f'{self.bot.user.name} Stats',
            description='\uFEFF',
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at
        )

        embed.add_field(name='Bot Version', value=self.bot.version)
        embed.add_field(name='Python Version', value=pythonVersion)
        embed.add_field(name='Discord.py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds', value=serverCount)
        embed.add_field(name='Total Users', value=memberCount)
        embed.add_field(name='Bot Developer', value="<@!257252196926750720>")

        embed.set_footer(text=f"To Nurture | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre='ik.'):
        """
        Set a custom prefix for a guild
        """
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')
        await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}prefix <prefix>` to change it again!")


def setup(bot):
    bot.add_cog(Commands(bot))