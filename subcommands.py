import discord
from discord.ext import commands

class Groups(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print("SubCommands Cog has been loaded\n-----")

        @commands.group()
        async def secret(self, ctx):
            if ctx.invoked_subcommand is None:
                await ctx.send("You found the secret. But are there more?", delete_after=15)


        @secret.group()
        async def finalsecret(self, ctx):
            await ctx.send("Your mom is gay")

def setup(bot):
    bot.add_cog(Groups(bot))