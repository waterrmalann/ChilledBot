# Discord.
import discord
# Command Handler.
from discord.ext import commands
# JSON Parser.
from utils import default


class ModerationCog(commands.Cog):
    """Server Administration and Management Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.bot_prefix = '.'
    
    @commands.command()
    async def test_mod(self, ctx):
        await ctx.send("Moderation Cog")

def setup(bot):
    bot.add_cog(ModerationCog(bot))