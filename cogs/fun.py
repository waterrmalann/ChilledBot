import discord
from discord.ext import commands
from utils import default


class FunCog(commands.Cog):
    """Entertainment / Fun Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.bot_prefix = '.'
    
    @commands.command()
    async def fun_test(self, ctx):
        await ctx.send("Fun Cog")

def setup(bot):
    bot.add_cog(FunCog(bot))