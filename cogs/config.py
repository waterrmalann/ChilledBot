# Discord
import discord
# Command Handler
from discord.ext import commands
# JSON Parser
from utils import default


class ConfigCog(commands.Cog, name = "Configuration"):
    """Guild Specific Bot Configuration Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.bot_prefix = '.'
        self.hidden = True
    
    @commands.command()
    async def test_config(self, ctx):
        await ctx.send("Config Cog")

def setup(bot):
    bot.add_cog(ConfigCog(bot))