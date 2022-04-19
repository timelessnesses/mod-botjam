try:
    import uvloop

    uvloop.install()
except ImportError:
    pass

import asyncio

from dotenv import load_dotenv

load_dotenv()
import os
import subprocess
from datetime import datetime

import discord
import jishaku
from discord import app_commands
from discord.ext import commands, tasks

bot = commands.Bot(
    "n!", intents=discord.Intents.all(), owner_id=int(os.getenv("OWNER_ID"))
)
bot.remove_command("help")


@bot.event
async def on_ready() -> None:
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await bot.change_presence(activity=discord.Game(name="n!help"))
    await bot.tree.sync()


async def load_modules(bot: commands.Bot) -> None:
    for file in os.listdir("./src"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"src.{file[:-3]}")


def get_git_revision_short_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("ascii")
        .strip()
    )


bot.start_time = datetime.utcnow()
bot.version_ = os.getenv("DEPLOY_TYPE") + " " + get_git_revision_short_hash()


async def main():
    global bot
    async with bot:
        await load_modules(bot)
        await jishaku.cog.async_setup(bot)  # e
        await bot.start(os.getenv("DISCORD_TOKEN"))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nExiting...")
    exit(0)
