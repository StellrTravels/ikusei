
import random
import discord
import aiohttp
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(description="Roll a random number between 1 and 100!")
    async def roll(self, ctx):
        n = random.randrange(1, 101)
        await ctx.send(n)

    @commands.command(description="Roll a dice!")
    async def dice(self, ctx):
        n = random.randrange(1, 7)
        await ctx.send(n)

    @commands.command(description="Flips a coin!")
    async def coinflip(self, ctx):
        n = random.randrange(0, 1)
        await ctx.send("Heads" if n == 1 else "Tails")

    @commands.command(description="Generate a random image of a cat!")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://aws.random.cat/meow") as r:
                data = await r.json()

                embed = discord.Embed(title="Meow", description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
                embed.set_image(url=data['file'])
                embed.set_footer(text="To Nurture | Ikusei")

                await ctx.send(embed=embed)

    @commands.command(description="Generate a random image of a dog!")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()

                embed = discord.Embed(
                    title="Woof",
                    description='\uFEFF',
                    colour=ctx.author.colour,
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=data['url'])
                embed.set_footer(text="To Nurture | Ikusei")

                await ctx.send(embed=embed)

    @commands.command(description="Generate a random joke!")
    async def joke(self, ctx):
        api = 'https://icanhazdadjoke.com/'
        async with aiohttp.request('GET', api, headers={'Accept': 'text/plain'}) as r:
            result = await r.text()
            embed = discord.Embed(
                title="Here's your dad joke:",
                description='\uFEFF',
                colour=ctx.author.colour,
                timestamp=ctx.message.created_at
            )
            embed.add_field(name="-", value=result)
            embed.set_footer(text="To Nurture | Ikusei")

            await ctx.send(embed=embed)

    

    @commands.command(description="Generate a random image of a fox!")
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                data = await r.json()

                embed = discord.Embed(
                    title="Floof",
                    description='\uFEFF',
                    colour=ctx.author.colour,
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=data['image'])
                embed.set_footer(text="To Nurture | Ikusei")

                await ctx.send(embed=embed)

    @commands.command(description="Relay a provided message back through the bot!")
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)



def setup(bot):
    bot.add_cog(Fun(bot))
