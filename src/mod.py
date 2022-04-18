import sys

import discord
from discord.ext import commands

sys.path.append("src")
import datetime

import aiofiles

import utils.embedgen
import utils.json
import utils.stuffs
import utils.views


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="hackban", aliases=["hb"])
    @commands.has_permissions(ban_members=True)
    async def hackban(
        self,
        ctx: commands.Context,
        user: discord.User = None,
        reason: str = "No reason provided",
    ) -> None:
        """
        Ban user before they joined the server
        Very useful for prevent raids

        Required arguments:
        user: The user to ban (ID)
        reason: The reason for the ban (default: No reason provided)
        """

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        reason: str = "No reason specified",
        disable_asking: str = "false",
    ) -> None:
        """
        Kicking the member

        Required arguments:
        member: The member to kick
        reason: The reason for kicking the member (default: No reason specified) (warning: Please wrap the reason in double quote or single quote.)
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if member == ctx.author:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't kick yourself", color=discord.Color.red()
                )
            )
        if member == self.bot.user:
            return await ctx.send(
                embed=discord.Embed(
                    title="Why you want to kick me. :( I am sad now.",
                    color=discord.Color.red(),
                )
            )
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't kick someone who has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to kick {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the kick", color=discord.Color.red()
                    )
                )

        now = datetime.datetime.now()
        await member.send(
            embed=discord.Embed(
                title="You have been kicked from {}".format(ctx.guild.name),
                description="You have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.red(),
            )
        )
        await member.kick(reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="{} has been kicked".format(member.name),
                description="{} have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    member.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "kick",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "kick",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(ctx, db)
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    async def log(ctx: commands.Context, db: dict, action: str) -> None:
        try:
            channel = ctx.guild.get_channel(
                int(db[str(ctx.guild.id)]["config"]["logging"])
            )
        except KeyError:
            return
        if channel is None:
            return
        embed = discord.Embed(
            title="Member {}".format(action),
            description="{} has been {} from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                ctx.author.name,
                action,
                ctx.guild.name,
                ctx.author.name,
                reason,
                now.strftime("%Y/%m/%d %H:%M:%S"),
            ),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        reason: str = "No reason specified",
        disable_asking: str = "false",
    ) -> None:
        """
        Banning the member

        Required arguments:
        member: The member to ban
        reason: The reason for banning the member (default: No reason specified) (warning: Please wrap the reason in double quote or single quote.)
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if member == ctx.author:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't ban yourself", color=discord.Color.red()
                )
            )
        if member == self.bot.user:
            return await ctx.send(
                embed=discord.Embed(
                    title="Why you want to ban me. :( I am sad now.",
                    color=discord.Color.red(),
                )
            )
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't ban someone who has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to ban {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the ban", color=discord.Color.red()
                    )
                )
        now = datetime.datetime.now()
        await member.send(
            embed=discord.Embed(
                title="You have been banned from {}".format(ctx.guild.name),
                description="You have been banned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.red(),
            )
        )
        await member.ban(reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="{} has been banned".format(member.name),
                description="{} have been banned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    member.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "ban",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "ban",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(ctx, db, "ban")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        member: discord.User = None,
        reason: str = "No reason specified",
        disable_asking: str = "false",
    ) -> None:
        """
        Unbanning the member

        Required arguments:
        member: The member to unban
        reason: The reason for unbanning the member (default: No reason specified) (warning: Please wrap the reason in double quote or single quote.)
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to unban {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the unban", color=discord.Color.red()
                    )
                )
        now = datetime.datetime.now()
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(
            embed=discord.Embed(
                title="{} has been unbanned".format(member.name),
                description="You have been unbanned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "unban",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "unban",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(ctx, db, "unban")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

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
        elif time.endswith("y"):
            return datetime.timedelta(days=int(time[:-1]) * 365)
        else:
            return datetime.timedelta(seconds=int(time))

    @commands.command(name="mute", aliases=["timeout", "tm", "m"])
    @commands.has_permissions(manage_roles=True)
    async def mute(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        duration: str = "6h",
        reason: str = "No reason specified",
        disable_asking: str = "false",
    ) -> None:
        """
        Muting the member

        Required arguments:
        member: The member to mute
        duration: The duration of the mute (default: 6 hours) (TIP: you can specify time as 0 so you can remove the timeout for that member or use unmute command instead)
        reason: The reason for muting the member (default: No reason specified) (warning: Please wrap the reason in double quote or single quote.)
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to mute {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the mute", color=discord.Color.red()
                    )
                )
        if self._parse_time(duration) == datetime.timedelta(seconds=0):
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="WARNING",
                    color=discord.Color.red(),
                    description="You're forcing the mute to be removed for {}\n Are you sure about that?".format(
                        member.name
                    ),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the unmute process!",
                        color=discord.Color.red(),
                    )
                )

        if (
            self._parse_time(duration).total_seconds() >= 2419200
        ):  # 28 days due to discord's time limit
            return await ctx.send(
                embed=discord.Embed(
                    title="You need to specify a duration",
                    color=discord.Color.red(),
                    description="The duration must be less than 28 days.\nExample: `{}mute @user 1h`".format(
                        ctx.prefix
                    ),
                )
            )
        now = datetime.datetime.now()
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't mute this user",
                    description="The user has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        await member.timeout(self._parse_time(duration))
        await ctx.send(
            embed=discord.Embed(
                title="{} has been muted".format(member.name),
                description="{} have been muted in {}\nActioner: {}\nReason: {}\nDuration: {}\nWhen: {}".format(
                    member.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    duration,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)

        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "mute",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    "duration": duration,
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "mute",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                        "duration": duration,
                    }
                ]
            }
        await self.log(ctx, db, "mute")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @commands.command(name="unmute", aliases=["untimeout", "untm", "um"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        disable_asking: str = "false",
    ) -> None:
        """
        Unmuting the member

        Required arguments:
        member: The member to unmute
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to unmute {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the unmute", color=discord.Color.red()
                    )
                )
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't unmute this user",
                    description="The user has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        await member.timeout(datetime.timedelta(seconds=0))
        await ctx.send(
            embed=discord.Embed(
                title="{} has been unmuted".format(member.name),
                description="{} have been unmuted\nActioner: {}".format(
                    member.name, ctx.author.name
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)

        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "unmute",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "unmute",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(ctx, db, "unmute")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @commands.command(name="warn")
    @commands.has_permissions(manage_roles=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        reason: str = "No reason provided",
        disable_asking: str = "false",
    ) -> None:
        """
        Warn the member

        Required arguments:
        member: The member to warn
        reason: The reason for the warn
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to warn {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the warn", color=discord.Color.red()
                    )
                )
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(
                embed=discord.Embed(
                    title="You can't warn this user",
                    description="The user has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        now = datetime.datetime.now()
        await member.send(
            embed=discord.Embed(
                title="You have been warned",
                description="You have been warned by {} for the reason: {}\nTime: {}".format(
                    ctx.author.name, reason, now.strftime("%Y/%m/%d %H:%M:%S")
                ),
                color=discord.Color.red(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)

        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "warn",
                    "user": member.id,
                    "moderator": ctx.author.id,
                    "reason": reason,
                    "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "warn",
                        "user": member.id,
                        "moderator": ctx.author.id,
                        "reason": reason,
                        "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(ctx, db, "warn")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @commands.command(name="delwarn")
    @commands.has_permissions(manage_roles=True)
    async def delwarn(
        self,
        ctx: commands.Context,
        id: str,
        reason: str = "No reason provided",
        disable_asking: str = "false",
    ) -> None:
        """
        Delete a warning

        Required arguments:
        id: The id of the warning to delete
        reason: The reason for the deletion
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to delete this warning?",
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await ctx.send(
                    embed=discord.Embed(
                        title="You cancelled the deletion", color=discord.Color.red()
                    )
                )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            for i in db[str(ctx.guild.id)]["logs"]:
                if i["id"] == id:
                    db[str(ctx.guild.id)]["logs"].remove(i)
                    await ctx.send(
                        embed=discord.Embed(
                            title="The warning has been deleted",
                            description="The warning has been deleted\nActioner: {}".format(
                                ctx.author.name
                            ),
                            color=discord.Color.green(),
                        )
                    )
                    async with aiofiles.open("db/logging.json", "w") as fp:
                        await util.json.dump(fp, db)
                    return
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="The warning doesn't exist",
                    description="The warning doesn't exist",
                    color=discord.Color.red(),
                )
            )
        await ctx.send(
            embed=discord.Embed(
                title="The warning doesn't exist",
                description="The warning doesn't exist",
                color=discord.Color.red(),
            )
        )

    @commands.command(name="warns", aliases=["warnings"])
    @commands.has_permissions(manage_roles=True)
    async def warns(self, ctx: commands.Context, member: discord.Member = None) -> None:
        """
        Get the warnings of a member

        Required arguments:
        member: The member to get the warnings of
        """
        if member is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("member"))
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            warns = db[str(ctx.guild.id)]["logs"]
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no warnings",
                    description="There are no warnings",
                    color=discord.Color.red(),
                )
            )
        try:
            warns = [i for i in warns if i["user"] == member.id]
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no warnings",
                    description="There are no warnings",
                    color=discord.Color.red(),
                )
            )
        if not warns:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no warnings",
                    description="There are no warnings",
                    color=discord.Color.red(),
                )
            )
        embed = discord.Embed(
            title="Warnings of {}".format(member.name),
            description="Warnings of {}".format(member.name),
            color=discord.Color.red(),
        )
        for i in warns:
            embed.add_field(name="Reason", value=i["reason"], inline=False)
            embed.add_field(
                name="Moderator",
                value=ctx.guild.get_member(i["moderator"]).name,
                inline=False,
            )
            embed.add_field(name="When", value=i["when"], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="purge", aliases=["bulkdel", "del", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = None):
        """
        Purge messages
        """
        if amount is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("amount"))
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(
            embed=discord.Embed(
                title="Purged {} messages".format(amount), color=discord.Color.red()
            )
        )


async def setup(bot: commands.Bot) -> None:
    """
    Function to setup the cog
    """
    await bot.add_cog(Moderation(bot))
