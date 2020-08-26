# Discord.
import discord
# Command Handler.
from discord.ext import commands
# Operating System Functions.
import os
from humanize import naturalsize, intcomma, naturaltime
# Object Inspector.
import inspect
# Asynchronous Package.
import asyncio
# Asynchronous Requests.
import aiohttp
# Time Value Manipulation.
import time
# DateTime Parser.
from datetime import datetime
# JSON Parser.
from utils import default, formatting
import base64
import platform

class OwnerCog(commands.Cog, name = "Owners"):

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
        self.session = aiohttp.ClientSession()

        # Cog Info
        self.hidden = True
        self.name = "Developer"
        self.aliases = {'dev', 'owner', 'developer'}
        self.categories = ('bot', 'python', 'cogs')

    @commands.command(name = 'print', hidden = True, usage = "<content>")
    @commands.is_owner()
    async def cout(self, ctx, *, content: str):
        """Prints text to the console."""

        print(content)
        await ctx.send(f"{self.emojis.tick} **Successfully printed content to terminal.**")
    
    @commands.command(brief = 'useful', usage = "<url>")
    @commands.is_owner()
    async def request(self, ctx, url = None, debug : bool = False):
        """Sends a request and returns data from an url."""

        url = url or "http://shibe.online/api/cats"
        start = time.perf_counter()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                if debug: await ctx.send(embed = discord.Embed(description=f"**Debug:**\n```py\n{r}```"))
                data = await r.json(content_type = None)
        end = time.perf_counter()
        duration = (end - start) * 1000
        
        embed = discord.Embed(
            title = url,
            color = self.colors.secondary,
            description = f"{self.emojis.tick} Evaluated in {duration:.2f}ms.",
            timestamp = datetime.utcnow()
        )

        embed.add_field(name = "Retrieved Data", value = f"```py\n{data}```", inline = False)
        if isinstance(data, dict):
            embed.add_field(name = "Keys", value = f"```py\n{', '.join(data.keys())}```", inline = False)
        await ctx.send(embed = embed)
    
    @commands.group(name = 'exceptions', hidden = True, usage = '<list/show/remove>', brief = 'bot')
    async def exceptions(self, ctx):
        """Manage ignored exceptions caught by the bot."""

        if not ctx.invoked_subcommand:
            raise commands.BadArgument('missing subcommand')
    
    @exceptions.command(name = 'list', aliases = ['all'])
    async def exceptions_list(self, ctx):
        """List all exceptions ignored by the bot."""

        if not self.bot.caught_exceptions:
            return await ctx.send(f"{self.emojis.cross} **There are no caught exceptions.**")

        all_errors = [f"{k} - {v['error'][0]} ({naturaltime(v['time'])})" for k, v in self.bot.caught_exceptions.items()]
        await ctx.send(formatting.codeblock('\n'.join(all_errors)))
    
    @exceptions.command(name = 'show', aliases = ['info'])
    async def exceptions_show(self, ctx, err_name: str):
        """Show more information about a particular exception."""

        if not err_name in self.bot.caught_exceptions:
            return await ctx.send(f"{self.emojis.cross} **That exception does not exist!**")

        err = self.bot.caught_exceptions[err_name]

        invocation_data = []
        invocation_data.append(f"Author: {err['author'][0]} ({err['author'][1]})")
        invocation_data.append(f"Guild: {err['guild'][0]} ({err['guild'][1]})")
        invocation_data.append(f"Channel: #{err['channel'][0]} ({err['channel'][1]})")
        invocation_data.append(f"Guild Owner: {err['guild_owner'][0]} ({err['guild_owner'][1]})")

        embed = discord.Embed(title = f"Exception `{err_name}`", color = self.colors.error, timestamp = err['time'])

        embed.add_field(name = "Exception", value = f"`{err['error'][1]}`\n```k\n{err['error'][0]}```", inline = False)
        embed.add_field(name = "Command", value = f"`{err['command'][0]}` from `{err['command'][1]}` cog.", inline = False)
        embed.add_field(name = "Invocation", value = formatting.codeblock('\n'.join(invocation_data)), inline = False)
        embed.add_field(name = f"Message ({err['message'][1]})", value = err['message'][0], inline = False)

        await ctx.send(embed = embed)
    
    @exceptions.command(name = 'clear', aliases = ['delete', 'remove'])
    async def exceptions_clear(self, ctx, err_name: str):

        if err_name == 'all':
            self.bot.caught_exceptions.clear()
            await ctx.send(f"{self.emojis.tick} **All exceptions have been cleared.**")
        elif err_name in self.bot.caught_exceptions:
            self.bot.caught_exceptions.pop(err_name)
            await ctx.send(f"{self.emojis.tick} **Exception `{err_name}` has been successfully removed.**")
        else:
            raise commands.BadArgument('invalid exception id')


    @commands.group(name = 'cogs', hidden = True, usage = '<load/reload/unload/list> [param]')
    async def cogs(self, ctx):
        """Manage bot cogs (modules)."""
        
        if not ctx.invoked_subcommand:
            raise commands.BadArgument('missing subcommand')
            
    @cogs.command(name = 'load', aliases = ['enable'])
    async def cogs_load(self, ctx, *, cog: str):
        """Command to load cogs in real-time."""

        if not cog.startswith('cogs.'): cog = 'cogs.' + cog

        try:
            self.bot.load_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error loading `{cog}`** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully loaded `{cog}`**")
    
    @cogs.command(name = 'unload', aliases = ['disable'])
    async def cogs_unload(self, ctx, *, cog: str):
        """Command to unload cogs in real-time."""

        if not cog.startswith('cogs.'): cog = 'cogs.' + cog

        try:
            self.bot.unload_extension(cog)
        except Exception as ex:
            await ctx.send(f"{self.emojis.cross} **Error unloading `{cog}`** `[ex {type(ex).__name__} - {ex}]`")
        else:
            await ctx.send(f"{self.emojis.tick} **Successfully unloaded `{cog}`**")
    
    @cogs.command(name = 'reload', aliases = ['refresh', 'restart'])
    async def cogs_reload(self, ctx, *, cog: str):
        """Command to reload cogs in real-time."""

        if cog.lower() == 'all':
            
            progress = []
            exceptions_caught = []
            cog_count = len(self.config.cogs)
            cog_counter = 0
            start = time.perf_counter()  # Start recording time.
            for cog in self.config.cogs:
                try:
                    self.bot.reload_extension(cog)
                except Exception as ex:
                    progress.append(f"{self.emojis.cross} | **`Couldn't Reload {cog}`**")
                    exceptions_caught.append({'cog': cog, 'exception': ex})
                else:
                    cog_counter += 1
                    progress.append(f"{self.emojis.tick} | **`Reloaded {cog}`**")
            end = time.perf_counter()  # Stop recording time.
            duration = (end - start) * 1000

            embed = discord.Embed(
                title = f"{self.emojis.tick if cog_count == cog_counter else self.emojis.neutral} Reloaded {cog_counter}/{cog_count} cogs.",
                description = '\n'.join(progress),
                color = self.colors.primary
            )
            if exceptions_caught:
                for ex in exceptions_caught:
                    embed.add_field(
                        name = f"Exception Caught | {ex['cog']}",
                        value = formatting.codeblock(ex['exception']),
                        inline = False
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

    @commands.command(aliases = ['kill', 'exit'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot"""

        print("[Disconnect] Bot Terminated")
        msg = await ctx.send('💀 **Terminating...**')
        await asyncio.sleep(1.5)
        await msg.edit(content = "☠️ **Terminated.**")
        await self.bot.logout()
    
    @commands.command(aliases = ['bsetname'], usage = '<username>')
    @commands.is_owner()
    async def bsetusername(self, ctx, *, name: str):
        """Set the bot's username."""

        await self.bot.user.edit(username = name)
        await ctx.send(f"{self.emojis.tick} **My username has successfully been set to \"{name}\".**")
    
    @commands.command(aliases = ['bsetnickname'], usage = '<nickname>')
    @commands.is_owner()
    @commands.guild_only()
    async def bsetnick(self, ctx, *, nickname=None):
        """Set the bot's nickname."""

        await ctx.guild.get_member(self.bot.user.id).edit(nick = nickname)
        await ctx.send(f"{self.emojis.tick} **My guild nickname has successfully been set to \"{nickname}\".**")
    
    @commands.command()
    async def uptime(self, ctx):
        """Check how long the bot has been up for."""

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        sentence = []

        if days > 0:
            sentence.append(f"{days} {'days' if days > 1 else 'day'}")
        if hours > 0:
            sentence.append(f"{hours} {'hours' if hours > 1 else 'hour'}")
        if minutes > 0:
            sentence.append(f"{minutes} {'minutes' if minutes > 1 else 'minute'}")
        if seconds > 0:
            sentence.append(f"{seconds} {'seconds' if seconds > 1 else 'second'}")

        sent = f"I have been online for the last {formatting.join_words(sentence)}."

        await ctx.send(sent)




def setup(bot):
    """Sets up the cog."""
    bot.add_cog(OwnerCog(bot))