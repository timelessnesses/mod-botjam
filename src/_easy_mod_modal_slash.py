import discord
import modals
from discord import app_app_commands


class easy_mod(app_commands.Cog, app_app_commands.Group, name="modal_mod"):
    """
    Moderation in very easiest way possible!
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="kick", aliases=["k"])
    async def kick(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.kick())

    @app_commands.command(name="ban", aliases=["b"])
    async def ban(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.ban())

    @app_commands.command(name="mute", aliases=["m"])
    async def mute(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.mute())

    @app_commands.command(name="unmute", aliases=["um"])
    async def unmute(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.unmute())

    @app_commands.command(name="warn", aliases=["w"])
    async def warn(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.warn())

    @app_commands.command(name="unwarn", aliases=["uw"])
    async def unwarn(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.unwarn())
