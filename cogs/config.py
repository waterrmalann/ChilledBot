import discord
from discord.ext import commands
from utils import default


class ConfigCog(commands.Cog):
    """Guild Specific Bot Configuration Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.bot_prefix = '.'
    
    @commands.command()
    async def test_config(self, ctx):
        await ctx.send("Config Cog")

def setup(bot):
    bot.add_cog(ConfigCog(bot))