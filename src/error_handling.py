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
                    f'Command "{ctx.invoked_with}" not found, maybe you meant "{matches[0]}"?'
                )
            else:
                await ctx.send(
                    f'Command "{ctx.invoked_with}" not found, use the help command to know what commands are available'
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
