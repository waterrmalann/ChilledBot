#0x15F153 Changelog Color
import discord
from discord.ext import commands
from utils import default
import time
import aiohttp

class UtilityCog(commands.Cog):
    """Utility Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
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
        await msg.edit(content=f':ping_pong: Pong! Latency is {duration:.2f}ms. API Latency is {(self.bot.latency * 1000):.2f}ms.')

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
    async def color(self, ctx, col = None):
        """Displays a color"""

        col = col.strip()

        if len(col) == 8 and col.startswith('0x'):
            col = int(col, 16)
        elif len(col) == 6 or col.startswith('#'):
            col = int(col[1:], 16)
        elif col.isdigit():
            col = int(col)
        else:
            await ctx.send("Invalid Color.")
            return
        
        embed = discord.Embed(
            title = str(col),
            color = col,
            description = "A preview of the color."
        )

        await ctx.send(embed=embed)
    
    @commands.command()
    async def request(self, ctx, url = None):
        """Sends a request and returns data from an url."""

        url = url or "http://shibe.online/api/cats"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                data = await r.json()

        embed = discord.Embed(
            title = url,
            color = self.colors.secondary,
            description = f"```{data}```"
        )
        await ctx.send(embed=embed)
        
    
    #@commands.command()
    #async def reverse(self, ctx, *, text = None):
    #    if not text:
    #        help_message = get_help_message(reverse)

def setup(bot):
    bot.add_cog(UtilityCog(bot))