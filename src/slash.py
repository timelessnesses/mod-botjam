import sys

import discord
from discord.ext import commands

sys.path.append("src")
import datetime

import aiofiles
from discord import app_commands

import utils.embedgen
import utils.json
import utils.stuffs
import utils.views


class Slashes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help")
    async def help(self, interaction, command: str = None):
        """Shows help about a command or the bot"""
        print(command)
        if command is None:
            embed = discord.Embed(
                title="Help", description="", color=discord.Color.blue()
            )
            for command in self.bot.commands:
                if command.hidden:
                    continue
                if command.aliases:
                    aliases = " | ".join(command.aliases)
                    embed.add_field(
                        name=f"{command.name} | {aliases}",
                        value=command.help,
                        inline=True,
                    )
                else:
                    embed.add_field(name=command.name, value=command.help, inline=True)
            await interaction.response.send_message(embed=embed)

        else:
            command = self.bot.get_command(command)
            if command is None:
                await interaction.response.send_message("That command does not exist.")
                return
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Usage", value=command.usage)
            embed.add_field(
                name="Aliases",
                value=", ".join(command.aliases) if command.aliases else "None",
            )
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", aliases=["p"])
    async def ping(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.bot.latency * 1000)}ms from API websocket",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="status")
    async def status(self, interaction: discord.Interaction) -> None:
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="credits", aliases=["c"])
    async def credits(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Credits", description="Thanks to everyone who using this bot!"
        )

        embed.add_field(name="Creator", value="[Unpredictable#9443] ")
        embed.add_field(name="Contributors", value="None")
        embed.add_field(
            name="Special thanks",
            value="[X19Z10#1125] for modal idea (modal is kinda sucks rn so yea i won't add it)",
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hackban", aliases=["hb"])
    @commands.has_permissions(ban_members=True)
    async def hackban(
        self,
        interaction: discord.Interaction,
        user: int,
        reason: str = "No reason provided",
    ) -> None:
        """
        Ban user before they joined the server
        Very useful for prevent raids

        Required arguments:
        user: The user to ban (ID)
        reason: The reason for the ban (default: No reason provided)
        """
        try:
            user = self.bot.fetch_user(user)
        except discord.NotFound:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="User not found",
                    color=discord.Color.red(),
                )
            )
        except discord.HTTPException:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="Failed to fetch user from API",
                    color=discord.Color.red(),
                )
            )
        if user.id == interaction.bot.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="Why you want to ban me :(",
                    color=discord.Color.red(),
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to kick {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the kick", color=discord.Color.red()
                    )
                )
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been kicked".format(user.name),
                description="{} have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    user.name,
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "kick",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "kick",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "hackbanned")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @app_commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
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
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if member == interaction.author:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't kick yourself", color=discord.Color.red()
                )
            )
        if member == self.bot.user:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Why you want to kick me. :( I am sad now.",
                    color=discord.Color.red(),
                )
            )
        if member.top_role.position >= interaction.author.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't kick someone who has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to kick {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the kick", color=discord.Color.red()
                    )
                )

        now = datetime.datetime.now()
        await member.send(
            embed=discord.Embed(
                title="You have been kicked from {}".format(interaction.guild.name),
                description="You have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.red(),
            )
        )
        await member.kick(reason=reason)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been kicked".format(member.name),
                description="{} have been kicked from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    member.name,
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "kick",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "kick",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "kicked")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    async def log(interaction: discord.Interaction, db: dict, action: str) -> None:
        try:
            channel = interaction.guild.get_channel(
                int(db[str(interaction.guild.id)]["config"]["logging"])
            )
        except KeyError:
            return
        if channel is None:
            return
        embed = discord.Embed(
            title="Member {}".format(action),
            description="{} has been {} from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                interaction.author.name,
                action,
                interaction.guild.name,
                interaction.author.name,
                reason,
                now.strftime("%Y/%m/%d %H:%M:%S"),
            ),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed)

    @app_commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
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
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if member == interaction.author:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't ban yourself", color=discord.Color.red()
                )
            )
        if member == self.bot.user:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Why you want to ban me. :( I am sad now.",
                    color=discord.Color.red(),
                )
            )
        if member.top_role.position >= interaction.author.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't ban someone who has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to ban {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the ban", color=discord.Color.red()
                    )
                )
        now = datetime.datetime.now()
        await member.send(
            embed=discord.Embed(
                title="You have been banned from {}".format(interaction.guild.name),
                description="You have been banned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.red(),
            )
        )
        await member.ban(reason=reason)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been banned".format(member.name),
                description="{} have been banned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    member.name,
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "ban",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "ban",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "ban")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @app_commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        member: discord.User,
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
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to unban {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the unban", color=discord.Color.red()
                    )
                )
        now = datetime.datetime.now()
        await interaction.guild.unban(member, reason=reason)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been unbanned".format(member.name),
                description="You have been unbanned from {}\nActioner: {}\nReason: {}\nWhen: {}".format(
                    interaction.guild.name,
                    interaction.author.name,
                    reason,
                    now.strftime("%Y/%m/%d %H:%M:%S"),
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "unban",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "unban",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "unban")
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

    @app_commands.command(name="mute", aliases=["timeout", "tm", "m"])
    @commands.has_permissions(manage_roles=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
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
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to mute {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the mute", color=discord.Color.red()
                    )
                )
        if self._parse_time(duration) == datetime.timedelta(seconds=0):
            view = utils.views.Confirm()
            await interaction.response.send_message(
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
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the unmute process!",
                        color=discord.Color.red(),
                    )
                )

        if (
            self._parse_time(duration).total_seconds() >= 2419200
        ):  # 28 days due to discord's time limit
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You need to specify a duration",
                    color=discord.Color.red(),
                    description="The duration must be less than 28 days.\nExample: `{}mute @user 1h`".format(
                        interaction.prefix
                    ),
                )
            )
        now = datetime.datetime.now()
        if member.top_role.position >= interaction.author.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't mute this user",
                    description="The user has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        await member.timeout(self._parse_time(duration))
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been muted".format(member.name),
                description="{} have been muted in {}\nActioner: {}\nReason: {}\nDuration: {}\nWhen: {}".format(
                    member.name,
                    interaction.guild.name,
                    interaction.author.name,
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
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "mute",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                    "duration": duration,
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "mute",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": now.strftime("%Y/%m/%d %H:%M:%S"),
                        "duration": duration,
                    }
                ]
            }
        await self.log(interaction, db, "mute")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @app_commands.command(name="unmute", aliases=["untimeout", "untm", "um"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        disable_asking: str = "false",
    ) -> None:
        """
        Unmuting the member

        Required arguments:
        member: The member to unmute
        disable asking: Whether or not to ask for confirmation (default: false)
        """
        if member is None:
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to unmute {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the unmute", color=discord.Color.red()
                    )
                )
        if member.top_role.position >= interaction.author.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="You can't unmute this user",
                    description="The user has a higher role than you",
                    color=discord.Color.red(),
                )
            )
        await member.timeout(datetime.timedelta(seconds=0))
        await interaction.response.send_message(
            embed=discord.Embed(
                title="{} has been unmuted".format(member.name),
                description="{} have been unmuted\nActioner: {}".format(
                    member.name, interaction.author.name
                ),
                color=discord.Color.green(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)

        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "unmute",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "unmute",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "unmute")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @app_commands.command(name="warn")
    @commands.has_permissions(manage_roles=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
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
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        if not disable_asking == "false":
            view = utils.views.Confirm()
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to warn {}?".format(member.name),
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the warn", color=discord.Color.red()
                    )
                )
        if member.top_role.position >= interaction.author.top_role.position:
            return await interaction.response.send_message(
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
                    interaction.author.name, reason, now.strftime("%Y/%m/%d %H:%M:%S")
                ),
                color=discord.Color.red(),
            )
        )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)

        try:
            db[str(interaction.guild.id)]["logs"].append(
                {
                    "id": util.stuffs.random_id(),
                    "type": "warn",
                    "user": member.id,
                    "moderator": interaction.author.id,
                    "reason": reason,
                    "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                }
            )
        except KeyError:
            db[str(interaction.guild.id)] = {
                "logs": [
                    {
                        "id": util.stuffs.random_id(),
                        "type": "warn",
                        "user": member.id,
                        "moderator": interaction.author.id,
                        "reason": reason,
                        "when": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    }
                ]
            }
        await self.log(interaction, db, "warn")
        async with aiofiles.open("db/logging.json", "w") as fp:
            await util.json.dump(fp, db)

    @app_commands.command(name="delwarn")
    @commands.has_permissions(manage_roles=True)
    async def delwarn(
        self,
        interaction: discord.Interaction,
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
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Are you sure you want to delete this warning?",
                    color=discord.Color.red(),
                ),
                view=view,
            )
            if view.value is None:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You're too slow!", color=discord.Color.red()
                    )
                )
            if not view.value:
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="You cancelled the deletion", color=discord.Color.red()
                    )
                )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            for i in db[str(interaction.guild.id)]["logs"]:
                if i["id"] == id:
                    db[str(interaction.guild.id)]["logs"].remove(i)
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="The warning has been deleted",
                            description="The warning has been deleted\nActioner: {}".format(
                                interaction.author.name
                            ),
                            color=discord.Color.green(),
                        )
                    )
                    async with aiofiles.open("db/logging.json", "w") as fp:
                        await util.json.dump(fp, db)
                    return
        except KeyError:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="The warning doesn't exist",
                    description="The warning doesn't exist",
                    color=discord.Color.red(),
                )
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="The warning doesn't exist",
                description="The warning doesn't exist",
                color=discord.Color.red(),
            )
        )

    @app_commands.command(name="warns", aliases=["warnings"])
    @commands.has_permissions(manage_roles=True)
    async def warns(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        """
        Get the warnings of a member

        Required arguments:
        member: The member to get the warnings of
        """
        if member is None:
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("member")
            )
        async with aiofiles.open("db/logging.json") as fp:
            db = await util.json.load(fp)
        try:
            warns = db[str(interaction.guild.id)]["logs"]
        except KeyError:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="There are no warnings",
                    description="There are no warnings",
                    color=discord.Color.red(),
                )
            )
        try:
            warns = [i for i in warns if i["user"] == member.id]
        except KeyError:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="There are no warnings",
                    description="There are no warnings",
                    color=discord.Color.red(),
                )
            )
        if not warns:
            return await interaction.response.send_message(
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
                value=interaction.guild.get_member(i["moderator"]).name,
                inline=False,
            )
            embed.add_field(name="When", value=i["when"], inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge", aliases=["bulkdel", "del", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int = 50):
        """
        Purge messages
        """
        if amount is None:
            return await interaction.response.send_message(
                embed=utils.embedgen.error_required_arg("amount")
            )
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Purged {} messages".format(amount), color=discord.Color.red()
            )
        )


async def setup(bot: commands.Bot) -> None:
    """
    Setup the logging cog
    """
    await bot.add_cog(Slashes(bot))
