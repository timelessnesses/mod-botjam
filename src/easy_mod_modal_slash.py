import discord
from discord import app_commands
import modals


class easy_mod(commands.Cog, app_commands.Group, name="modal_mod"):
    """
    Moderation in very easiest way possible!
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command(name="kick", aliases=["k"])
    async def kick(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.kick)

    @commands.command(name="ban", aliases=["b"])
    async def ban(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(modals.ban)
