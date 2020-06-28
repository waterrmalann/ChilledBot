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
# Mathematics Parser.
from py_expression_eval import Parser
# JSON Parser.
from utils import default
# DateTime Parser.
from datetime import datetime


class UtilityCog(commands.Cog):
    """Utility Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.exp_parser = Parser()  # Mathematic Expression Parser.
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
        
        embed = discord.Embed(title = f"{self.config.bot_name} {self.config.bot_version} Changelog.")
        embed.add_field(
            name = "Uptime Command",
            value = "Displays for how long the bot has been online for. `uptime`",
            inline = False
        )
        embed.set_footer(text = "Last updated June 27th, 2020")
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['colour'], usage = "<color (hex/int)>")
    async def color(self, ctx, col: str):
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

    @commands.command(aliases = ['math', 'calculate'], usage = '<expression>')
    async def calc(self, ctx, *, equation):
        """Calculate a math equation. See `calc help`"""


        if equation == 'help':

            embed = discord.Embed(title = "Calculator Help", color = self.colors.primary)
            embed.description = "```m\n" \
                "2 + 3 -> 5\n" \
                "2 - 3 -> -1\n" \
                "2 * 3 -> 6\n" \
                "2 / 3 -> 0.6666666666666666\n" \
                "2 % 3 -> 2\n" \
                "-3 * 4 -> -12\n" \
                "abs(-2) -> 2\n\n" \
                "ceil(1.4) -> 2.0\n" \
                "floor(1.4) -> 1.0\n" \
                "round(1.4) -> 1.0\n\n" \
                "2^3 -> 8.0\n" \
                "sqrt(16) -> 4.0\n\n" \
                "sin(3.14) -> 0.0015926529164868282\n" \
                "cos(3.14) -> -0.9999987317275395\n" \
                "tan(3.14) -> -0.0015926549364072232\n\n" \
                "asin(1) -> 1.5707963267948966\n" \
                "acos(1) -> 0.0\n" \
                "atan(1) -> 0.7853981633974483\n\n" \
                "log(2.7) -> 0.9932517730102834\n" \
                "log(16, 2) -> 4.0\n" \
                "exp(1) -> 2.718281828459045\n\n" \
                "log(E) -> 1.0\n" \
                "cos(PI) -> -1.0```"
            embed.set_footer(text = "Example: math 2 * 3")
            return await ctx.send(embed = embed)
    
        try:
            final = self.exp_parser.parse(equation).evaluate({})
        except ZeroDivisionError:
            return await ctx.send(f"{self.emojis.cross} **You cannot divide by zero!** `[ex ZeroDivisionError]`")
        except OverflowError:
            return await ctx.send(f"{self.emojis.cross} **Result too large to be represented. Are you trying to break me?** `[ex OverflowError]`")
        except Exception as e:
            return await ctx.send(f"{self.emojis.cross} **Cannot compute. Make sure expression is valid.** `[ex Exception]`")

        embed = discord.Embed(
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )
        embed.add_field(name = equation, value = str(final))
        embed.set_footer(text = f"Evaluated by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
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
            description = f"{self.emojis.tick} Evaluated in {duration:.2f}ms.",
            timestamp = datetime.utcnow()
        )

        embed.add_field(name = "Retrieved Data", value = f"```py\n{data}```", inline = False)
        if isinstance(data, dict):
            embed.add_field(name = "Keys", value = f"```py\n{', '.join(data.keys())}```", inline = False)
        await ctx.send(embed = embed)
    
    @commands.command(usage = '<search/summary/random> [query]', aliases = ["wikipedia"])
    async def wiki(self, ctx, param: str, *, stuff = None):
        """Searches for articles on Wikipedia."""

        param = param.lower().strip()

        if param == 'search':
            if stuff is None:
                raise commands.BadArgument(message = 'Missing query parameter.')
            else:
                results = wikipedia.search(stuff)
                new_results = [f"{count}. {result}" for count, result in enumerate(results)]
                await ctx.send(f"I searched for {stuff} and got the following results.")
                return await ctx.send("\n".join(new_results))

        elif param == 'summary':

            if stuff is None:
                raise commands.BadArgument('Missing query parameter.')
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

            raise commands.BadArgument('Missing parameter.')
    
    @commands.command(aliases = ['ud', 'urbandict', 'udict'])
    #@commands.is_nsfw()
    async def urban(self, ctx, *, query):
        """Search the urban dictionary for word meanings."""

        async with self.session.get('http://api.urbandictionary.com/v0/define', params={'term': query}) as resp:
            result = await resp.json()

        if not result['list']:
            return await ctx.send("No word was found.")

        definition = result['list'][0]['definition']
        word = result['list'][0]['word']
        link = result['list'][0]['permalink']
        example = result['list'][0]['example']
        author = result['list'][0]['author'].title()
        thumbs_up = result['list'][0]['thumbs_up']

        embed = discord.Embed(
            title = word,
            url = link,
            color = self.colors.ud_yellow,
            timestamp = datetime.utcnow()
        )
        embed.set_author(name = f"By {author} on Urban Dictionary.")
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/726353729842053171/726353766881689651/urban_dict.png")
        embed.add_field(name = "Meaning", value = definition, inline = False)
        embed.add_field(name = "Example", value = example, inline = False)
        embed.set_footer(text = f"urbandictionary.com • 👍 {thumbs_up}", icon_url = ctx.author.avatar_url)
        
        await ctx.send(embed = embed)
    
    @commands.command()
    async def invite(self, ctx):
        """Gives you a link to invite me!"""

        invite_url = f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147483095&scope=bot"
        embed = discord.Embed(color = self.colors.secondary, description = f"🔗  You can invite me using __**[this link!]({invite_url})**__")
        await ctx.send(embed = embed)
    
    @commands.command(usage = '<"question"> ["option 1"] ["option 2"]')
    #@commands.has_permissions(manage_messages = True)
    @commands.guild_only()
    async def poll(self, ctx, question: str, yes: str = "yes", no: str = "no", ):
        """Creates a simple voting poll."""

        embed = discord.Embed(
            title = question.capitalize(),
            description = f"{self.emojis.tick} {yes.capitalize()}\n{self.emojis.cross} {no.capitalize()}",
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )
        try:
            await ctx.message.delete() 
        except:
            await ctx.send("Could not execute command! Please try again later.")
        else:
            sent_embed = await ctx.send(embed = embed)
            await sent_embed.add_reaction(self.emojis.tick)
            await sent_embed.add_reaction(self.emojis.cross)
        
    
    @commands.command(usage = '[code block]')
    async def hastebin(self, ctx, *, codeblock):
        """Paste code to hastebin."""

        if codeblock.startswith('`') and codeblock.endswith('`'):
            code = codeblock.strip('`')
        else:
            raise commands.BadArgument('Code must be in a codeblock!')

        async with self.session.post("https://hastebin.com/documents", data = code) as resp:
            data = await resp.json()
            pin = data['key']

        embed = discord.Embed(
            title = 'Your code has been successfully posted to hastebin!',
            description = f"https://hastebin.com/{pin}",
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        ) 
        embed.set_footer(text = f"Posted by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['screenshot'], usage = '<Website URL>')
    @commands.is_nsfw()
    async def ss(self, ctx, *, url: str):
        """Takes a screenshot of the website linked."""
        
        async with ctx.typing():

            async with self.session.post("http://magmafuck.herokuapp.com/api/v1", headers = {'website': url}) as r:
                data = await r.json()

            image = data['snapshot']
            embed = discord.Embed(title = f'Screenshot of {url}', color = self.colors.primary)
            embed.set_image(url = image)
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
            await ctx.send(embed=embed)

    #@commands.command()
    #async def reverse(self, ctx, *, text = None):
    #    if not text:
    #        help_message = get_help_message(reverse)

def setup(bot):
    bot.add_cog(UtilityCog(bot))