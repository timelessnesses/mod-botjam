import discord
from discord.ext import commands
from discord import app_commands
import psutil


class Stuff(commands.Cog, name="unrelated"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="credits", aliases=["c"])
    async def credits(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Credits", description="Thanks to everyone who using this bot!"
        )

        embed.add_field(name="Creator", value="[Unpredictable#9443] ")
        embed.add_field(name="Contributors", value="None")
        embed.add_field(name="Special thanks", value="[X19Z10#1125] for modal idea")

        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["p"])
    async def ping(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.bot.latency * 1000)}ms from API websocket",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="status")
    async def status(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Status", description="Bot status", color=discord.Color.green()
        )
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Disk", value=f"{psutil.disk_usage('/').percent}%")
        embed.add_field(name="Uptime", value=f"{round(self.bot.uptime / 60)} minutes")
        embed.add_field(name="Python", value=f"{platform.python_version()}")
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="Bot version", value=f"{self.bot.version_}")
        await ctx.send(embed=embed)


class Stuff_Slash(app_commands.Group, commands.Cog, name="stuff"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="ping", aliases=["p"])
    async def ping(self, ctx: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.bot.latency * 1000)}ms from API websocket",
        )
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="status")
    async def status(self, ctx: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Status", description="Bot status", color=discord.Color.green()
        )
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Disk", value=f"{psutil.disk_usage('/').percent}%")
        embed.add_field(name="Uptime", value=f"{round(self.bot.uptime / 60)} minutes")
        embed.add_field(name="Python", value=f"{platform.python_version()}")
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="Bot version", value=f"{self.bot.version_}")
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="credits", aliases=["c"])
    async def credits(self, ctx: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Credits", description="Thanks to everyone who using this bot!"
        )

        embed.add_field(name="Creator", value="[Unpredictable#9443] ")
        embed.add_field(name="Contributors", value="None")
        embed.add_field(name="Special thanks", value="[X19Z10#1125] for modal idea")

        await ctx.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stuff(bot))
    await bot.add_cog(Stuff_Slash(bot))
