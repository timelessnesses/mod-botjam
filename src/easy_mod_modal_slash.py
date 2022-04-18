import discord
import modals
from discord import app_commands


class easy_mod(commands.Cog, app_commands.Group, name="modal_mod"):
    """
    Moderation in very easiest way possible!
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command(name="kick", aliases=["k"])
    async def kick(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.kick())

    @commands.command(name="ban", aliases=["b"])
    async def ban(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.ban())

    @commands.command(name="mute", aliases=["m"])
    async def mute(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.mute())

    @commands.command(name="unmute", aliases=["um"])
    async def unmute(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.unmute())

    @commands.command(name="warn", aliases=["w"])
    async def warn(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.warn())

    @commands.command(name="unwarn", aliases=["uw"])
    async def unwarn(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.unwarn())
