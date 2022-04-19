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
from discord.ext import commands

bot = commands.Bot("n!", intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready() -> None:
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await tree.sync()


async def load_modules(bot: commands.Bot) -> None:
    for file in os.listdir("./src"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"src.{file[:-3]}")


async def main():
    async with bot:
        await load_modules(bot)
        await jishaku.async_setup(bot)  # e
        await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
