import sys

import aiofiles
import discord
from discord.ext import commands

sys.path.append("src")
import utils.json


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_servers()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.check_servers()

    async def check_servers(self):
        async with aiofiles.open("db/logging.json", "r") as f:
            db = await utils.json.load(f)
        for server in self.bot.guilds:
            if str(server.id) not in db.keys():
                db[str(server.id)] = {
                    "config": {
                        "logging": None,
                    },
                    "logs": [],
                }

        async with aiofiles.open("db/logging.json", "w") as f:
            await utils.json.dump(f, db)


async def setup(bot):
    await bot.add_cog(Events(bot))
