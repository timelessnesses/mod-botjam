import discord

def error_required_arg(name:str) -> discord.Embed:
    return discord.Embed(title="Error", description=f"You must provide a {name}.", color=discord.Color.red())