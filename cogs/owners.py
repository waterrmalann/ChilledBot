# Discord.
import discord
# Command Handler.
from discord.ext import commands
# Time Value Manipulation.
import time
# Object Inspector.
import inspect
# DateTime Parser.
from datetime import datetime
# JSON Parser.
from utils import default
# Operating System Functions.
import os

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
    
    @commands.command(name = 'load', hidden = True, usage = "<cogs.name>")
    @commands.is_owner()
    async def cogs_load(self, ctx, *, cog: str):
        """Command to load cogs in real-time."""

        if not cog.startswith('cogs.'):
            cog = 'cogs.' + cog

        try:
            self.bot.load_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error loading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully loaded {cog}**")
    
    @commands.command(name = 'unload', hidden = True, usage = "<cogs.name>")
    @commands.is_owner()
    async def cogs_unload(self, ctx, *, cog: str):
        """Command to unload cogs in real-time."""

        if not cog.startswith('cogs.'):
            cog = 'cogs.' + cog

        try:
            self.bot.unload_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error unloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully unloaded {cog}**")
        
    @commands.command(name = 'reload', hidden = True, usage = "<cogs.name/all>")
    @commands.is_owner()
    async def cogs_reload(self, ctx, *, cog: str):
        """Command to reload cogs in real-time."""

        if cog.lower() == 'all':
            
            progress = []
            start = time.perf_counter()
            cog_count = len(self.config.cogs)
            cog_counter = 0
            for cog in self.config.cogs:
                try:
                    self.bot.reload_extension(cog)
                except Exception as ex:
                    progress.append(f"{self.emojis.cross} | **`Couldn't Reload {cog}`**")
                else:
                    cog_counter += 1
                    progress.append(f"{self.emojis.tick} **`Reloaded {cog}`**`")
            end = time.perf_counter()
            duration = (end - start) * 1000

            embed = discord.Embed(
                title = f"{self.emojis.tick if cog_count == cog_counter else self.emojis.neutral} Reloaded {cog_counter}/{cog_count} cogs.",
                description = '\n'.join(progress),
                color = self.colors.primary
            )
            embed.set_footer(text = f"Reloaded in {duration:.2f}ms")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed = embed)
            
        
        else:

            if not cog.startswith('cogs.'):
                cog = 'cogs.' + cog

            try:
                self.bot.reload_extension(cog)
            except Exception as ex:
                await ctx.send(f"{self.emojis.cross} **Error reloading {cog}** `[ex {type(ex).__name__} - {ex}]`")
            else:
                await ctx.send(f"{self.emojis.tick} **Successfully reloaded {cog}**")
    
    @commands.command(aliases = ['eval'], hidden = True, usage = "<code>")
    @commands.is_owner()
    async def ev(self, ctx, *, command):
        """Evaluates Python Code"""

        code = command.strip("`")

        start = time.perf_counter()
        res = eval(code)
        end = time.perf_counter()
        duration = (end - start) * 1000

        # To-Do: DRY
        if inspect.isawaitable(res):
            embed = discord.Embed(title = f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.secondary)
            embed.add_field(name = "Code", value=f"```py\n{code}```", inline = False)
            embed.add_field(name = "Return", value=f"```py\n{await res}```", inline = False)
            embed.set_footer(text = "Awaited")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed = embed)
        else:		
            embed = discord.Embed(title=f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.primary)
            embed.add_field(name = "Code", value = f"```py\n{code}```", inline = False)
            embed.add_field(name = "Return", value = f"```py\n{res}```", inline = False)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed = embed)
    
    @commands.command(aliases = ['shell', 'system'], hidden = True, usage = "<code>")
    @commands.is_owner()
    async def sh(self, ctx, *, command):
        """Evaluates shell commands."""

        code = command.strip("`")

        start = time.perf_counter()
        res = os.system(code)
        end = time.perf_counter()
        duration = (end - start) * 1000

        embed = discord.Embed(title = f"{self.emojis.tick} Evaluated in {duration:.2f}ms", color = self.colors.primary)
        embed.add_field(name = "Code", value = f"```py\n{code}```", inline = False)
        if res is not None: embed.add_field(name = "Return", value = f"```py\n{res}```", inline = False)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)

def setup(bot):
    """Sets up the cog."""
    bot.add_cog(OwnerCog(bot))