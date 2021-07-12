import discord
from discord.ext import commands
import platform
import random
import aiohttp
import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("Please check with ik.help for the usage of this command!")


    @commands.command(description="Provides statistics of the bot!")
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

    @commands.command(description="Set a custom prefix for the guild!")
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

    @commands.command(description="Create an invite link to the server!")
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

    @commands.command(description="Gather statistics about the server!")
    @commands.guild_only()
    async def serverstats(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + " Server Information",
            description=description if description != description else "No description set for the server.",
            color=random.choice(self.bot.color_list)
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))
