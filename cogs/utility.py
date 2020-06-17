import discord
from discord.ext import commands
from utility import default
import time

class UtilityCog(commands.Cog):
    """Utility Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.bot_prefix = '.'

    @commands.command(name = 'ping')
    async def ping(self, ctx):
        """Check the bot's latency."""

        # Calculates ping between sending a message and editing it, giving a nice round-trip latency.
        # The second ping is an average latency between the bot and the websocket server (one-way, not round-trip)
        start = time.perf_counter()
        msg = await ctx.send('Ping?')
        end = time.perf_counter()
        duration = (end - start) * 1000
        await msg.edit(content=f':ping_pong: Pong! Latency is {duration:.2f}ms. API Latency is {(client.latency * 1000):.2f}ms.')

    @commands.command(aliases = ['updates', 'changes', 'whats_new', 'whatsnew'])
    async def changelog(self, ctx):
        """Changelog of the current version of the bot."""
        changel = f"""
            {self.config.bot_name} {self.config.bot_version} Changelog

            __**1. Complete Rewrite*__
            ChilledBot has completely been rewritten from scratch, and is now better optimized.
            It also utilizes new functionality such as command cooldowns and sharding.
            """
        
        await ctx.send(changel)
    
    @commands.command()
    async def reverse(self, ctx, *, text = None):

def setup(bot):
    bot.add_cog(UtilityCog(bot))
    
    
        





def setup(bot):
    """Sets up the cog."""
    bot.add_cog(UtilityCog(bot))