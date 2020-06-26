#0x15F153 Changelog Color
# Discord.
import discord
# Commnd Handler.
from discord.ext import commands
# Time Value Manipulation.
import time
# Asynchronous Requests.
import aiohttp
# Randomization.
import random
# Wikiepdia Library.
import wikipedia
# JSON Parser.
from utils import default
# DateTime Parser.
from datetime import datetime


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
    
    @commands.command(usage = "<color (hex/int)>")
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
        
        hex_color_code = f"#{hex(col)[2:].upper()}"
        embed = discord.Embed(
            title = f"{hex_color_code} | {col}",
            color = col,
            description = f"A preview of the color **{hex_color_code}**."
        )

        await ctx.send(embed=embed)
    
    @commands.command(usage = "<url>")
    async def request(self, ctx, url = None, debug : bool = False):
        """Sends a request and returns data from an url."""

        url = url or "http://shibe.online/api/cats"
        start = time.perf_counter()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                if debug: await ctx.send(embed = discord.Embed(description=f"**Debug:**\n```py\n{r}```"))
                data = await r.json()
        end = time.perf_counter()
        duration = (end - start) * 1000
        
        embed = discord.Embed(
            title = url,
            color = self.colors.secondary,
            description = f"{self.emojis.tick} Evaluated in {duration:.2f}ms."
        )

        embed.add_field(name = "Retrieved Data", value = f"```py\n{data}```", inline = False)
        if isinstance(data, dict):
            embed.add_field(name = "Keys", value = f"```py\n{', '.join(data.keys())}```", inline = False)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed = embed)
    
    @commands.command(usage = '<search/summary/random> [query]', aliases = ["wikipedia"])
    async def wiki(self, ctx, param: str, *, stuff = None):
        """Searches for articles on Wikipedia."""

        param = param.lower().strip()

        if param == 'search':
            if stuff is None:
                raise commands.BadArgument(message = 'missing query')
            else:
                results = wikipedia.search(stuff)
                new_results = [f"{count}. {result}" for count, result in enumerate(results)]
                await ctx.send(f"I searched for {stuff} and got the following results.")
                return await ctx.send("\n".join(new_results))

        elif param == 'summary':

            if stuff is None:
                raise commands.BadArgument('missing query')
            else:
                msg = await ctx.send("🌐 **Searching...**")
                try:
                    summary = wikipedia.summary(stuff, sentences = 5, auto_suggest = False)

                    embed = discord.Embed(title = stuff.capitalize(), description = summary, color = self.colors.primary)
                    embed.set_footer(text = "Powered by wikipedia.org")
                    await ctx.send(embed = embed)
                except Exception as ex:
                    await ctx.send(f"{self.emojis.cross} **Unknown Exception.** `[ex {ex}]`")
                    await ctx.send("Please try again later or with a different search query.\nMy developer has been notified of the issue.")

                    # send dm to a random dev
                finally:

                    await msg.delete()

        elif param.lower() == 'random':
            msg = await ctx.send("🎲 **Randomizing...**")
            try:
                rand = wikipedia.random()
                print(rand)
                rand = random.choice(rand)
                summary = wikipedia.summary(rand, sentences = 5)

                embed = discord.Embed(title = rand, description = summary, color = self.colors.primary)
                embed.set_footer(text = "Powered by wikipedia.org")
                await ctx.send(embed = embed)
            except Exception as ex:
                await ctx.send(f"{self.emojis.cross} **Unknown Exception.** `[ex {ex}]`")
                await ctx.send("Please try again later.\nMy developer has been notified of the issue.")
                #owner = self.bot.get_user(random.choice(list(self.bot.owner_ids)))
            finally:
                await msg.delete()
        
        else:

            raise commands.BadArgument('missing parameter')
    
    @commands.command()
    async def invite(self, ctx):
        """Gives you a link to invite me!"""

        invite_url = f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147483095&scope=bot"
        embed = discord.Embed(color = self.colors.secondary, description = f"🔗  You can invite me using __**[this link!]({invite_url})**__")
        await ctx.send(embed = embed)
    
    #@commands.command()
    #async def reverse(self, ctx, *, text = None):
    #    if not text:
    #        help_message = get_help_message(reverse)

def setup(bot):
    bot.add_cog(UtilityCog(bot))