import discord
from discord.ext import commands
import time
import inspect
from datetime import datetime
from utils import default
import os

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
    
    @commands.command(name = 'load', hidden = True)
    @commands.is_owner()
    async def cogs_load(self, ctx, *, cog: str):
        """Command to load cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.load_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error loading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully loaded {cog}**")
    
    @commands.command(name = 'unload', hidden = True)
    @commands.is_owner()
    async def cogs_unload(self, ctx, *, cog: str):
        """Command to unload cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.unload_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error unloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully unloaded {cog}**")
        
    @commands.command(name = 'reload', hidden = True)
    @commands.is_owner()
    async def cogs_reload(self, ctx, *, cog: str):
        """Command to reload cogs in real-time."""

        if not cog.startswith('cog.'):
            cog = 'cog.' + cog

        try:
            self.bot.reload_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error reloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully reloaded {cog}**")
    
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
            embed = discord.Embed(title = f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.primary)
            embed.add_field(name = "Code", value=f"```py\n{code}```", inline = False)
            
            if res: embed.add_field(name="Return", value=f"```py\n{await res}```", inline=False)
            embed.timestamp = datetime.utcnow()

            await ctx.send(embed=embed)
        else:		
            embed = discord.Embed(title=f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.primary)
            embed.add_field(name="Code", value=f"```py\n{code}```", inline=False)

            if res: embed.add_field(name="Return", value=f"```py\n{res}```", inline=False)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
    
    @commands.command(aliases = ['shell', 'system'])
    @commands.is_owner()
    async def sh(self, ctx, *, command):
        """Evaluates shell commands."""

        code = command.strip()

        start = time.perf_counter()
        res = os.system(code)
        end = time.perf_counter()
        duration = (end - start) * 1000

        embed = discord.Embed(title=f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.primary)
        embed.add_field(name="Code", value=f"```py\n{code}```", inline=False)
        if res: embed.add_field(name="Return", value=f"```py\n{res}```", inline=False)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)

def setup(bot):
    """Sets up the cog."""
    bot.add_cog(OwnerCog(bot))