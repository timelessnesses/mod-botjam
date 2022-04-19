import sys

import discord
from discord.ext import commands

sys.path.append("src")
import datetime

import aiofiles

import utils.embedgen
import utils.json
import utils.logger
import utils.stuffs
import utils.views


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="hackban", aliases=["hb"])
    @commands.has_permissions(ban_members=True)
    async def hackban(
        self,
        ctx: discord.Interaction,
        user: int = None,
        reason: str = "No reason provided",
        disable_asking: str = "false",
    ) -> None:
        """
        Ban user before they joined the server
        Very useful for prevent raids

        Required arguments:
        user: The user to ban (ID)
        reason: The reason for the ban (default: No reason provided)
        """
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
        if user is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You need to specify a user (user ID) to ban!",
                )
            )
        try:
            user = self.bot.fetch_user(user)
        except discord.NotFound:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="User not found",
                    color=discord.Color.red(),
                )
            )
        except discord.HTTPException:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Failed to fetch user from API",
                    color=discord.Color.red(),
                )
            )
        if user.id == ctx.bot.user.id:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Why you want to ban me :(",
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
            await view.wait()
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
        await ctx.guild.ban(user, reason=reason)
        d = utils.stuffs.random_id()
        await ctx.send(
            embed=discord.Embed(
                title="{} has been hackbanned".format(user.name),
                description="{} have been hackbanned from {}\nActioner: {}\nReason: {}\nWhen: {}\nLog ID: {}".format(
                    user.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                    d,
                ),
                color=discord.Color.green(),
            )
        )

        await self.log(ctx, db, "hackban", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.hackban,
            ctx.author.id,
            user.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
        )

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
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
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
            await view.wait()
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
        d = utils.stuffs.random_id()
        await ctx.send(
            embed=discord.Embed(
                title="{} has been kicked".format(member.name),
                description="{} have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}\nLog ID: {}".format(
                    member.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                    d,
                ),
                color=discord.Color.green(),
            )
        )

        await self.log(ctx, db, "kick", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.kick,
            ctx.author.id,
            member.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
        )

    async def log(self, ctx: commands.Context, db: dict, action: str, id: str) -> None:
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
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
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
            await view.wait()
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
        d = utils.stuffs.random_id()
        await ctx.send(
            embed=discord.Embed(
                title="{} has been banned".format(member.name),
                description="{} have been banned from {}\nActioner: {}\nReason: {}\nWhen: {}\nLog ID: {}".format(
                    member.name,
                    ctx.guild.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                    d,
                ),
                color=discord.Color.green(),
            )
        )
        await self.log(ctx, db, "ban", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.ban,
            ctx.author.id,
            member.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
        )

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
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
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
            await view.wait()
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
        d = utils.stuffs.random_id()
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

        await self.log(ctx, db, "unban", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.unban,
            ctx.author.id,
            member.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
        )

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
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
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
            await view.wait()
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
            await view.wait()
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
        d = utils.stuffs.random_id()
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

        await self.log(ctx, db, "mute", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.mute,
            ctx.author.id,
            member.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
            duration,
        )

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
            await view.wait()
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
        d = utils.stuffs.random_id()
        await ctx.send(
            embed=discord.Embed(
                title="{} has been unmuted".format(member.name),
                description="{} have been unmuted\nActioner: {}".format(
                    member.name, ctx.author.name
                ),
                color=discord.Color.green(),
            )
        )

        await self.log(ctx, db, "unmute", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.unmute,
            ctx.author.id,
            member.id,
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        )

    @commands.command(name="warn")
    @commands.has_permissions(manage_roles=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        reason: str = "No reason provided",
        disable_asking: str = "true",
    ) -> None:
        """
        Warn the member

        Required arguments:
        member: The member to warn
        reason: The reason for the warn
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
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
            await view.wait()
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
        d = utils.stuffs.random_id()
        await ctx.send(
            embed=discord.Embed(
                title="{} has been warned".format(member.name),
                description="{} have been warned\nActioner: {}\nReason: {}\nTime: {}\nLog ID: {}".format(
                    member.name,
                    ctx.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                    d,
                ),
                color=discord.Color.green(),
            )
        )

        await self.log(ctx, db, "warn", d)
        await utils.logger.log(
            d,
            ctx.guild.id,
            utils.logger.Types.warn,
            ctx.author.id,
            member.id,
            now.strftime("%Y/%m/%d %H:%M:%S"),
            reason,
        )

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
        if disable_asking.lower() not in ("true", "false"):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="If you want to type a phrases consider wrap them in \" or ' due to command parsing problems!",
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await ctx.send(
                embed=discord.Embed(
                    title="Are you sure you want to delete this warning?",
                    color=discord.Color.red(),
                ),
                view=view,
            )
            await view.wait()
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
            db = await utils.json.load(fp)
        g = None
        try:
            for i in db[str(ctx.guild.id)]["logs"]:
                if i["id"] == id:
                    g = i
                    if i["type"] != "warn":
                        return await ctx.send(
                            embed=discord.Embed(
                                title="This isn't a warning",
                                description="This isn't a warning",
                                color=discord.Color.red(),
                            )
                        )
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
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="The warning doesn't exist",
                    description="The warning doesn't exist",
                    color=discord.Color.red(),
                )
            )
        await self.log(ctx, db, "delwarn", id)
        await utils.logger.log(
            id,
            ctx.guild.id,
            utils.logger.Types.delwarn,
            ctx.author.id,
            g["user"],
            datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            None,
            g["duration"],
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
            db = await utils.json.load(fp)
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
            warns = [i for i in warns if i["user"] == member.id and i["type"] == "warn"]
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
        async with aiofiles.open("db/logging.json") as fp:
            db = await utils.json.load(fp)
        try:
            db[str(ctx.guild.id)]["logs"].append(
                {
                    "id": utils.stuffs.random_id(),
                    "type": "purge",
                    "user": ctx.author.id,
                    "amount": amount,
                    "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(ctx.guild.id)] = {
                "logs": [
                    {
                        "id": utils.stuffs.random_id(),
                        "type": "purge",
                        "user": ctx.author.id,
                        "amount": amount,
                        "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        async with aiofiles.open("db/logging.json", "w") as fp:
            await utils.json.dump(fp, db)

        await self.log(ctx, db, "purge")

    @commands.command(name="getlogs", aliases=["log"])
    @commands.has_permissions(manage_messages=True)
    async def getlog(self, ctx: commands.Context, id: str = None):
        """
        Get log with ID

        Required arguments:
        id: The id of the log to get
        """
        if id is None:
            return await ctx.send(embed=utils.embedgen.error_required_arg("id"))
        async with aiofiles.open("db/logging.json") as fp:
            db = await utils.json.load(fp)
        try:
            logs = db[str(ctx.guild.id)]["logs"]
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no logs",
                    description="There are no logs",
                    color=discord.Color.red(),
                )
            )
        try:
            logs = [i for i in logs if i["id"] == id]
        except KeyError:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no logs",
                    description="There are no logs",
                    color=discord.Color.red(),
                )
            )
        if not logs:
            return await ctx.send(
                embed=discord.Embed(
                    title="There are no logs",
                    description="There are no logs",
                    color=discord.Color.red(),
                )
            )
        embed = discord.Embed(
            title="Log with ID {}".format(id),
            description="Log with ID {}".format(id),
            color=discord.Color.red(),
        )
        for i in logs:
            embed.add_field(name="Reason", value=i["reason"], inline=False)
            embed.add_field(
                name="Moderator",
                value=ctx.guild.get_member(i["moderator"]).name,
                inline=False,
            )
            embed.add_field(name="When", value=i["when"], inline=False)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Function to setup the cog
    """
    await bot.add_cog(Moderation(bot))
