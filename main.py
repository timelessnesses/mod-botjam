try:
    import uvloop

    uvloop.install()
except ImportError:
    pass

import asyncio

from dotenv import load_dotenv

load_dotenv()
import os

import discord
import jishaku
from discord import app_commands
from datetime import datetime
from discord.ext import commands

bot = commands.Bot("n!", intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready() -> None:
    global loop_time
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await bot.change_presence(activity=discord.Game(name="n!help"))


async def load_modules(bot: commands.Bot) -> None:
    for file in os.listdir("./src"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"src.{file[:-3]}")


async def main():
    async with bot:
        await load_modules(bot)
        await jishaku.cog.async_setup(bot)  # e
        await bot.start(os.getenv("DISCORD_TOKEN"))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nExiting...")
    exit(0)
