import io
import sys
import traceback
from difflib import get_close_matches

import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, exception: Exception
    ) -> None:
        if isinstance(exception, commands.CommandNotFound):
            cmds = [cmd.name for cmd in self.bot.commands]
            # cmds = [cmd.name for cmd in bot.commands if not cmd.hidden] # use this to stop showing hidden commands as suggestions
            matches = get_close_matches(ctx.invoked_with, cmds)
            if len(matches) > 0:
                await ctx.send(
                    embed=discord.Embed(
                        title="Command not found",
                        description=f"Did you mean `{matches[0]}`?",
                        color=discord.Color.red(),
                    )
                )

            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Command not found",
                        description=f"Did you mean `{ctx.invoked_with}`?",
                        color=discord.Color.red(),
                    )
                )
        elif isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(
                    title="Missing argument",
                    description=f"You are missing the `{exception.param.name}` argument.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(exception, commands.BadArgument):
            await ctx.send(
                embed=discord.Embed(
                    title="Bad argument",
                    description=f"The `{exception.param.name}` argument is invalid.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(exception, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Missing permissions",
                    description=f"You do need the `{', '.join(exception.missing_permissions)}` permission.",
                    color=discord.Color.red(),
                )
            )
        else:
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(exception), exception, exception.__traceback__, file=sys.stderr
            )
            error = "".join(
                traceback.TracebackException.from_exception(exception).format()
            )
            await ctx.send(
                embed=discord.Embed(
                    title="Command errors out!, please contact Timelessnesses (aka Unpredictable)",
                    description="```\n" + error + "\n```",
                    color=discord.Color.red(),
                )
            )


async def setup(bot):
    await bot.add_cog(Errors(bot))
