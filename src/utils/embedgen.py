import discord


def error_required_arg(name: str) -> discord.Embed:
    return discord.Embed(
        title="Error",
        description=f"You must provide a {name}.",
        color=discord.Color.red(),
    )


async def perm_error(ctx: discord.Context) -> discord.Embed:
    return discord.Embed(
        title="Error",
        description=f"You do not have permission to use this command.",
        color=discord.Color.red(),
    )
