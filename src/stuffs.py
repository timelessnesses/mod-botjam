import platform
from datetime import datetime

import discord
import psutil
from discord import app_commands
from discord.ext import commands


class Stuff(
    commands.Cog,
):
    """
    Miscellaneous commands and stuffs that don't fit anywhere else.
    """

    def __init__(self, bot):
        self.bot = bot

    @property
    def display_emoji(self):
        return "💭"

    @commands.hybrid_command(name="credits", aliases=["c"])
    async def credits(self, ctx):
        """
        Shows the credits.
        """
        embed = discord.Embed(
            title="Credits", description="Thanks to everyone who using this bot!"
        )

        embed.add_field(name="Creator", value="[Unpredictable#9443] ")
        embed.add_field(name="Contributors", value="None")
        embed.add_field(
            name="Special thanks",
            value="[X19Z10#1125] for modal idea (modal still sucks and very limited so no)",
        )

        embed.add_feld(
            name="The bot is also open-source!",
            value="https://github.com/timelessnesses/mod-botjam",
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping", aliases=["p"])
    async def ping(self, ctx):
        """
        Pong!
        """
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.bot.latency * 1000)}ms from API websocket",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="status")
    async def status(self, ctx):
        """
        Status of bot like uptime, memory usage, etc.
        """
        embed = discord.Embed(
            title="Status", description="Bot status", color=discord.Color.green()
        )
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Disk", value=f"{psutil.disk_usage('/').percent}%")
        embed.add_field(
            name="Uptime",
            value=f"{round((datetime.utcnow() - self.bot.start_time).total_seconds() / 60)} minutes",
        )
        embed.add_field(name="Python", value=f"{platform.python_version()}")
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="Bot version", value=f"{self.bot.version_}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stuff(bot))
