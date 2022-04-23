import sys
import typing

import aiofiles
import discord
from discord.ext import commands

sys.path.append("src")
import datetime
import traceback

import utils.json
import utils.logger
import utils.profanity_checker
import utils.stuffs


class dummy:
    def __init__(self, member: discord.Member, bot: commands.Bot):
        self.guild = member.guild
        self.author = bot.user


class Automod(commands.Cog, name="Auto moderation"):
    """
    Automatically do most of your tasks so you can take a rest.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @property
    def display_emoji(self):
        return "😎"

    async def log(
        self,
        ctx: commands.Context,
        action: str,
        id: str,
        reason,
        target: discord.User,
        actioner: discord.User = None,
    ) -> None:

        async with aiofiles.open("db/logging.json") as fp:
            db = await utils.json.load(fp)
        try:
            channel = ctx.guild.get_channel(
                int(db[str(ctx.guild.id)]["config"]["logging"])
            )
        except KeyError:
            return
        except TypeError:
            return
        if channel is None:
            return
        embed = discord.Embed(
            title="Action {}".format(action),
            description="{} has been {} from {}\nActioner: {}\nReason: {}\nWhen: {}\nLog ID: {}".format(
                target.mention,
                action,
                ctx.guild.name,
                actioner.mention if actioner is not None else ctx.author.mention,
                reason,
                datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
                id,
            ),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)

    @commands.hybrid_command(name="autoban")
    async def autoban(
        self,
        ctx: discord.Interaction,
        toggle: bool = None,
    ):
        """
        Automatically ban user if user account oldness isn't reached (default: 7 days)
        """
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            if db[str(ctx.guild.id)]["autokick"]:
                await ctx.send(
                    embed=discord.Embed(
                        title="Auto-kick is already enabled",
                        description="You can disable it with `{}autokick`".format(
                            ctx.prefix
                        ),
                        color=discord.Color.red(),
                    )
                )
        except KeyError:
            pass
        if toggle is None:
            try:
                db[str(ctx.guild.id)]["autoban"] = (
                    not db[str(ctx.guild.id)]["autoban"]
                    if not db[str(ctx.guild.id)].get("autoban") is None
                    else True
                )
            except KeyError:
                db[str(ctx.guild.id)] = {"autoban": True}
        else:
            try:
                db[str(ctx.guild.id)]["autoban"] = toggle
            except KeyError:
                db[str(ctx.guild.id)] = {"autoban": toggle}
        await ctx.send(
            embed=discord.Embed(
                title="Auto ban",
                description=f"Auto ban is now {'enabled' if db[str(ctx.guild.id)]['autoban'] else 'disabled'}",
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    @commands.hybrid_command(name="autokick")
    async def autokick(
        self,
        ctx: discord.Interaction,
        toggle: bool = None,
    ):
        """
        Automatically kick user if user account oldness isn't reached (default: 7 days)
        """
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            if db[str(ctx.guild.id)]["autoban"]:
                await ctx.send(
                    embed=discord.Embed(
                        title="Auto-ban is already enabled",
                        description="You can disable it with `{}autoban`".format(
                            ctx.prefix
                        ),
                        color=discord.Color.red(),
                    )
                )
                return
        except KeyError:
            pass
        if toggle is None:
            try:
                db[str(ctx.guild.id)]["autokick"] = (
                    not db[str(ctx.guild.id)]["autokick"]
                    if not db[str(ctx.guild.id)].get("autokick") is None
                    else True
                )
            except KeyError:
                db[str(ctx.guild.id)] = {"autokick": True}
            await ctx.send(
                embed=discord.Embed(
                    title="Auto kick",
                    description=f"Auto kick is now {'enabled' if db[str(ctx.guild.id)]['autokick'] else 'disabled'}",
                    color=discord.Color.green(),
                )
            )
        else:
            try:
                db[str(ctx.guild.id)]["autokick"] = toggle
            except KeyError:
                db[str(ctx.guild.id)] = {"autokick": toggle}
        await ctx.send(
            embed=discord.Embed(
                title="Auto kick",
                description=f"Auto kick is now {'enabled' if db[str(ctx.guild.id)]['autokick'] else 'disabled'}",
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    @commands.hybrid_command(name="set_account_old")
    async def set_account_old(
        self,
        ctx: discord.Interaction,
        days: int = 7,
    ):
        """
        Set the account oldness (default: 7 days)
        """
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            db[str(ctx.guild.id)]["account_old"] = days
        except KeyError:
            db[str(ctx.guild.id)] = {"account_old": days}
        await ctx.send(
            embed=discord.Embed(
                title="Account oldness",
                description=f"Account oldness is now {days} days. Any account lower than that will be kicked/banned",
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    async def check_account_old(self, member: discord.Member):
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            if (discord.utils.utcnow() - member.created_at).days < db[
                str(member.guild.id)
            ]["account_old"]:
                return True
            return False
        except KeyError:
            return False

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            if db[str(member.guild.id)]["autoban"]:
                if await self.check_account_old(member):
                    await member.send(
                        embed=discord.Embed(
                            title="Account oldness",
                            description=f"Your account is too young, you have now been banned due to security reasons.\n",
                            color=discord.Color.red(),
                        )
                    )

                    context = dummy(member, self.bot)
                    d = utils.stuffs.random_id()
                    await self.log(
                        context,
                        "banned",
                        d,
                        "Account oldness",
                        member,
                    )
                    await utils.logger.log(
                        d,
                        context.guild.id,
                        utils.logger.Types.ban,
                        self.bot.user.id,
                        member.id,
                        datetime.datetime.utcnow(),
                        "Automatic ban for account oldness is lower than {} days".format(
                            db[str(member.guild.id)]["account_old"]
                        ),
                    )
                    await member.ban(reason="Account oldness")
            return
        except KeyError as e:
            traceback.print_exc()
        try:
            if db[str(member.guild.id)]["autokick"]:
                if await self.check_account_old(member):
                    await member.send(
                        embed=discord.Embed(
                            title="Account oldness",
                            description=f"Your account is too young, you have now been kicked due to security reasons.\n",
                            color=discord.Color.red(),
                        )
                    )
                    context = dummy(member, self.bot)
                    d = utils.stuffs.random_id()
                    await self.log(
                        context,
                        "kicked",
                        d,
                        "Account oldness",
                        member,
                    )
                    await utils.logger.log(
                        d,
                        context.guild.id,
                        utils.logger.Types.kick,
                        self.bot.user.id,
                        member.id,
                        datetime.datetime.utcnow(),
                        "Automatic kick for account oldness is lower than {} days".format(
                            db[str(member.guild.id)]["account_old"]
                        ),
                    )
                    await member.kick(reason="Account oldness")
        except KeyError:
            pass

    @commands.hybrid_command(name="autoswear")
    async def autoswear(
        self,
        ctx: discord.Interaction,
        toggle: bool = None,
    ):
        """
        Automatically mute member for specific amount of time if they said profane word (default: 5 minutes)
        """
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        if toggle is None:
            try:
                db[str(ctx.guild.id)]["autoswear"] = (
                    not db[str(ctx.guild.id)]["autoswear"]
                    if not db[str(ctx.guild.id)].get("autoswear") is None
                    else True
                )
            except KeyError:
                db[str(ctx.guild.id)] = {"autoswear": True}
        else:
            try:
                db[str(ctx.guild.id)]["autoswear"] = toggle
            except KeyError:
                db[str(ctx.guild.id)] = {"autoswear": toggle}
        await ctx.send(
            embed=discord.Embed(
                title="Auto swear",
                description=f"Auto swear is now {'enabled' if db[str(ctx.guild.id)]['autoswear'] else 'disabled'}",
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    def _parse_time(self, time: str) -> datetime.timedelta:
        """
        Parsing the time
        Required arguments:
        time: The time to parse
        """
        if time.endswith("s"):
            return datetime.timedelta(seconds=int(time[:-1]))
        elif time.endswith("m"):
            return datetime.timedelta(minutes=int(time[:-1]))
        elif time.endswith("h"):
            return datetime.timedelta(hours=int(time[:-1]))
        elif time.endswith("d"):
            return datetime.timedelta(days=int(time[:-1]))
        elif time.endswith("w"):
            return datetime.timedelta(weeks=int(time[:-1]))
        else:
            raise commands.BadArgument(f"{time} is not a valid time")

    @commands.hybrid_command(name="set_swear_time")
    async def set_swear_time(
        self,
        ctx: discord.Interaction,
        time: str = "1m",
    ):
        """
        Amount of time for muting when member said any profanity word (default: 1 minute)
        """
        time = self.parse_time(time)
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        try:
            db[str(ctx.guild.id)]["swear_time"] = time.total_seconds()
        except KeyError:
            db[str(ctx.guild.id)] = {"swear_time": time.total_seconds()}
        await ctx.send(
            embed=discord.Embed(
                title="Swear time",
                description=f"Swear time is now {str(time)}",
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/automod.json", "w") as f:
            await utils.json.dump(f, db)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        async with aiofiles.open("db/automod.json", "r") as f:
            db = await utils.json.load(f)
        if message.author.bot:
            return
        if message.guild is None:
            return
        try:
            if db[str(message.guild.id)]["autoswear"]:
                try:
                    time = datetime.timedelta(
                        seconds=db[str(message.guild.id)]["swear_time"]
                    )
                except KeyError:
                    time = datetime.timedelta(minutes=5)
                if await utils.profanity_checker.is_profane(message.content):
                    d = utils.stuffs.random_id()
                    ctx = await self.bot.get_context(message)
                    try:
                        await message.author.timeout(time, reason="Swearing")
                        await message.delete()
                    except discord.Forbidden:
                        await self.log(
                            ctx,
                            "failed to mute for swearing",
                            d,
                            "I don't have permission to mute this member",
                            message.author,
                            self.bot.user,
                        )
                        await message.author.send(
                            embed=discord.Embed(
                                title="Swearing",
                                description=f"Stop swearing! Yes I can't mute you but this is warning.",
                                color=discord.Color.red(),
                            )
                        )
                        await utils.logger.log_mute(
                            d,
                            message.guild.id,
                            utils.logger.Types.swear,
                            self.bot.user.id,
                            message.author.id,
                            datetime.datetime.utcnow(),
                            "I don't have permission to mute this member",
                            str(time),
                        )
                    except discord.HTTPException:
                        await self.log(
                            ctx,
                            "failed to mute for swearing",
                            d,
                            "Operation failed",
                            message.author,
                            self.bot.user,
                        )
                        await message.author.send(
                            embed=discord.Embed(
                                title="Swearing",
                                description=f"Stop swearing! Yes I can't mute you but this is warning.",
                                color=discord.Color.red(),
                            )
                        )
                        await utils.logger.log_mute(
                            d,
                            message.guild.id,
                            utils.logger.Types.swear,
                            self.bot.user.id,
                            message.author.id,
                            datetime.datetime.utcnow(),
                            "Operation failed",
                            str(time),
                        )

                    else:
                        await self.log(
                            ctx,
                            "muted for swearing",
                            d,
                            "Muted for swearing",
                            message.author,
                            self.bot.user,
                        )
                        await message.author.send(
                            embed=discord.Embed(
                                title="Swearing",
                                description=f"You have been muted for {str(time)} because you said a profanity word",
                                color=discord.Color.red(),
                            )
                        )
                        await utils.logger.log_mute(
                            d,
                            message.guild.id,
                            utils.logger.Types.swear,
                            self.bot.user.id,
                            message.author.id,
                            datetime.datetime.utcnow(),
                            "Member muted",
                            str(time),
                        )
        except KeyError:
            pass


async def setup(bot: commands.Bot):
    """
    Setting up the cog
    """
    await bot.add_cog(Automod(bot))
