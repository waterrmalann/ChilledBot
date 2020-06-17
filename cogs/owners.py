import discord
from discord.ext import commands
import time
import inspect
from datetime import datetime

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = 'load', hidden = True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command to load cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.load_extension(cog)
        except Exception as ex:
            await ctx.send(f"<:red_mark:694527415904370799> **Error loading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"<:green_tick:694527417410125844> **Successfully loaded {cog}**")
    
    @commands.command(name = 'unload', hidden = True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command to unload cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.unload_extension(cog)
        except Exception as ex:
            await ctx.send(f"<:red_mark:694527415904370799> **Error unloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"<:green_tick:694527417410125844> **Successfully unloaded {cog}**")
        
    @commands.command(name = 'reload', hidden = True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command to reload cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.reload_extension(cog)
        except Exception as ex:
            await ctx.send(f"<:red_mark:694527415904370799> **Error reloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"<:green_tick:694527417410125844> **Successfully reloaded {cog}**")
    
    @commands.command(aliases = ['eval'], hidden = True)
    @commands.is_owner()
    async def ev(self, ctx, *, command):
        """Evaluates Python Code"""

        code = command.strip("`")

        start = time.perf_counter()
        res = eval(code)
        end = time.perf_counter()
        duration = (end - start) * 1000

        if inspect.isawaitable(res):
            embed = discord.Embed(title=f"<:green_tick:694527417410125844> Evaluated in {duration:.2f}ms")
            embed.add_field(name="Code", value=f"```py\n{code}```", inline=False)
            
            if res: embed.add_field(name="Return", value=f"```py\n{await res}```", inline=False)
            embed.timestamp = datetime.utcnow()

            await ctx.send(embed=embed)
        else:		
            embed = discord.Embed(title=f"<:green_tick:694527417410125844> Evaluated in {duration:.2f}ms")
            embed.add_field(name="Code", value=f"```py\n{code}```", inline=False)
            if res: embed.add_field(name="Return", value=f"```py\n{res}```", inline=False)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)

def setup(bot):
    """Sets up the cog."""
    bot.add_cog(OwnerCog(bot))