import sys

import aiofiles
import aiohttp
import discord
from discord.ext import commands

sys.path.append("src")
import datetime
import typing

import utils.json
import utils.logger
import utils.profanity_checker
import utils.stuffs


class AutoMod(commands.Cog, name="Auto Moderation"):
    def __init__(self, bot):
        self.bot = bot
        self.time_window = 200
        self.author_checks = {}

    """ async def spam_checker(self, message: discord.Message) -> bool:
        async with aiofiles.open("db/automod.json") as f:
            db = await utils.json.load(f)
        try:
            if db[str(message.guild.id)]["prevent_spam"] == False:
                return
        except KeyError:
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        try:
            self.author_checks[message.author.id].append(
                {
                    "when": message.created_at,
                }
            )
        except KeyError:
            self.author_checks[message.author.id] = [
                {
                    "when": message.created_at,
                }
            ]
        try:
            if (
                self.author_checks[-2]["when"] - self.author_checks[-1]["when"]
            ).total_seconds() < self.time_window:
                await message.delete()
                await message.author.send(
                    embed=discord.Embed(
                        title="AutoMod",
                        description="You have been automatically timedout for 5 minutes for spamming.",
                    )
                )
                d = utils.stuffs.random_id()
                await message.author.timeout(datetime.timedelta(minutes=5))
                await utils.logger.log(
                    d,
                    message.guild.id,
                    utils.logger.Types.spam,
                    self.bot.user.id,
                    message.author.id,
                    "muted",
                    "automatically muted for spamming",
                )
                del self.author_checks[message.author.id]
                await self.log(
                    message,
                    "auto moderated - muted",
                    d,
                    "automatically muted for spamming",
                    message.author,
                )
                return True
                return True
        except IndexError:
            pass
        except KeyError:
            pass
        return False """

    async def profanity_checker(self, message: discord.Message) -> bool:
        async with aiofiles.open("db/automod.json") as f:
            db = await utils.json.load(f)
        try:
            if db[str(message.guild.id)]["prevent_swearing"] == False:
                return
        except KeyError:
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        if await utils.profanity_checker.is_profane(message.content):
            await message.delete()
            await message.author.send(
                embed=discord.Embed(
                    title="AutoMod",
                    description="You have been automatically timedout for 1 minutes for using profanity.",
                )
            )
            try:
                await message.author.timeout(datetime.timedelta(minutes=1))
            except discord.Forbidden:
                return
            d = utils.stuffs.random_id()
            await utils.logger.log(
                d,
                utils.logger.Types.profanity,
                self.bot.user.id,
                message.guild.id,
                message.author.id,
                "muted",
                "automatically muted for profanity",
            )
            await self.log(
                message,
                "auto moderated - muted",
                d,
                "automatically muted for profanity",
                message.author,
            )
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """if await self.spam_checker(message):
        return"""
        # spam checker still wip
        await self.profanity_checker(message)

    @commands.hybrid_command(name="prevent_swearing", aliases=["prevent_swear", "ps"])
    async def prevent_swearing(
        self, ctx: commands.Context, toggle: bool = None
    ) -> None:
        """
        Enable or disable the prevent swearing feature
        """
        async with aiofiles.open("db/automod.json") as f:
            db = await utils.json.load(f)
        try:
            if toggle is None:
                try:
                    db[str(ctx.guild.id)]["prevent_swearing"] = not db[
                        str(ctx.guild.id)
                    ]["prevent_swearing"]
                    await ctx.send(
                        embed=discord.Embed(
                            title="AutoMod",
                            description="Prevent Swearing has been {}".format(
                                "enabled"
                                if db[str(ctx.guild.id)]["prevent_swearing"]
                                else "disabled"
                            ),
                        )
                    )
                except KeyError:
                    db[str(ctx.guild.id)] = {
                        "prevent_swearing": True,
                    }
                    await ctx.send(
                        embed=discord.Embed(
                            title="AutoMod",
                            description="Prevent Swearing has been enabled",
                        )
                    )
            elif toggle.lower() in ("true", "on"):
                db[str(ctx.guild.id)]["prevent_swearing"] = True
                await ctx.send(
                    embed=discord.Embed(
                        title="AutoMod",
                        description="Prevent Swearing has been enabled",
                    )
                )
            elif toggle.lower() in ("false", "off"):
                db[str(ctx.guild.id)]["prevent_swearing"] = False
                await ctx.send(
                    embed=discord.Embed(
                        title="AutoMod",
                        description="Prevent Swearing has been disabled",
                    )
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="AutoMod",
                        description="Invalid argument",
                    )
                )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "prevent_swearing": True,
            }
            await ctx.send(
                embed=discord.Embed(
                    title="AutoMod",
                    description="Prevent Swearing has been enabled",
                )
            )
        except AttributeError:  # bool
            try:
                db[str(ctx.guild.id)]["prevent_swearing"] = toggle
            except KeyError:
                db[str(ctx.guild.id)] = {
                    "prevent_swearing": toggle,
                }
            await ctx.send(
                embed=discord.Embed(
                    title="AutoMod",
                    description="Prevent Swearing has been {}".format(
                        "enabled"
                        if db[str(ctx.guild.id)]["prevent_swearing"]
                        else "disabled"
                    ),
                )
            )

        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    async def log(
        self, ctx: commands.Context, action: str, id: str, reason, target: discord.User
    ) -> None:
        async with aiofiles.open("db/logging.json") as fp:
            db = await utils.json.load(fp)
        try:
            channel = ctx.guild.get_channel(
                int(db[str(ctx.guild.id)]["config"]["logging"])
            )
        except KeyError:
            return
        if channel is None:
            return
        embed = discord.Embed(
            title="Action {}".format(action),
            description="{} has been {} from {}\nActioner: {}\nReason: {}\nWhen: {}\nLog ID: {}".format(
                target.name + "#" + target.discriminator,
                action,
                ctx.guild.name,
                ctx.author.mention,
                reason,
                datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
                id,
            ),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)


async def setup(bot) -> None:
    """
    Setup the cog
    """
    await bot.add_cog(AutoMod(bot))
