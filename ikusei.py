import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('ik.')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

# Defining a few things
intents = discord.Intents.default()
intents.members=True
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=257252196926750720, help_command=None, intents=intents)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.version = '0.0.3'
bot.blacklisted_users = []
bot.cwd = cwd

bot.colors = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x349BD8,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
}

bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: ik.\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, I'm {bot.user.name}.\nUse ik. to interact with me!"))

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.author.id in bot.blacklisted_users:
        return

    if f"<@!{bot.user.id}>" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = 'ik.'
        prefixMsg = await message.channel.send(f"My prefix here is `{prefix}`")
        await prefixMsg.add_reaction(':eyes:')

    await bot.process_commands(message)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)
