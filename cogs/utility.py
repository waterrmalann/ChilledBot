#0x15F153 Changelog Color
# Discord.
import discord
# Commnd Handler.
from discord.ext import commands
# Time Value Manipulation.
import time
# Asynchronous Requests.
import aiohttp
# Asynchronous Wikipedia.
#import aiowiki
# Randomization.
import random
# Wikiepdia Library.
import wikipedia
# Mathematics Parser.
from py_expression_eval import Parser
# Color Conversion
import colorsys
# JSON Parser.
from utils import default, formatting
# DateTime Parser.
from humanize import naturaldelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
# Base64
import base64


class UtilityCog(commands.Cog, name = "Utility"):
    """Utility Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.exp_parser = Parser()  # Mathematic Expression Parser.
        self.config = default.get("config.json")
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
        #self.wiki = aiowiki.Wiki.wikipedia("en")
        self.bot_prefix = '.'

        # Cog Info
        self.hidden = False
        self.name = "Utility"
        self.aliases = {'utility', 'utils', 'tools'}
        self.categories = ('bot', 'design', 'useful', 'other')

    @commands.command(brief = 'bot', name = 'ping')
    async def ping(self, ctx):
        """Check the bot's latency."""

        # Calculates ping between sending a message and editing it, giving a nice round-trip latency.
        # The second ping is an average latency between the bot and the websocket server (one-way, not round-trip)
        start = time.perf_counter()
        msg = await ctx.send('Ping?')
        end = time.perf_counter()
        duration = (end - start) * 1000
        await msg.edit(content = f'🏓 Pong! Latency is {duration:.2f}ms. API Latency is {(self.bot.latency * 1000):.2f}ms.')

    @commands.command(brief = 'bot', aliases = ['updates', 'changes', 'whats_new', 'whatsnew'])
    async def changelog(self, ctx):
        """Changelog of the current version of the bot."""
        
        embed = discord.Embed(title = f"{self.config.bot_name} {self.config.bot_version} Changelog.")
        embed.add_field(
            name = "Uptime Command",
            value = "Displays for how long the bot has been online for. `uptime`",
            inline = False
        )
        embed.set_footer(text = "Last updated July 19th, 2020")
        await ctx.send(embed = embed)

    @commands.command(brief = 'bot')
    async def invite(self, ctx):
        """Gives you a link to invite me!"""

        invite_url = f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2147483095&scope=bot"
        embed = discord.Embed(
            title = "Invite me to your server!",
            description = f"🔗  You can invite me using __**[this link!]({invite_url})**__",
            color = self.colors.secondary
        )

        await ctx.send(embed = embed)

    @commands.command(brief = 'design', aliases = ["color"], usage = '[color (hex/int)]')
    async def colour(self, ctx, *, col: str = None):
        """Returns information on a specific (or random) color."""

        if col:
            if len(col) == 8 and col.startswith('0x'):
                col = int(col, 16)
            elif len(col) == 6 or col.startswith('#'):
                if col.startswith('#'):
                    col = int(col[1:], 16)
                else:
                    col = int(col, 16)
            elif col.isdigit():
                col = int(col)
            else:
                raise commands.BadArgument('Invalid color!')
        else:
            col = random.randint(0, 16777215)
        hexcode = hex(col)[2:].upper()
        
        embed = discord.Embed(
            title = f"#{hexcode}",  # Replace this with the color's name.
            url = f"https://www.colorhexa.com/{hexcode}",
            color = col,
        )
        embed.set_thumbnail(url = f"http://www.colourlovers.com/img/{hexcode}/200/200/image.png")
    
        # Thanks to Spinfish. I got inspired by his code for this part.
        # https://github.com/spinfish/michael-bot/blob/master/cogs/utilities.py
        r, g, b = discord.Color(col).to_rgb()
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        y, i, q = colorsys.rgb_to_yiq(r, g, b)

        embed.add_field(name = "Hex Code", value = f"`#{hexcode}`", inline = True)
        embed.add_field(name = "Integer", value = f"`{col}`", inline = True)
        embed.add_field(name = "RGB Value", value = f"`{r, g, b}`", inline = False)
        embed.add_field(name = "HLS Value", value = f"`{(round(h, 2), round(l, 2), round(s, 2))}`", inline = True)
        embed.add_field(name = "HSV Value", value = f"`{(round(h, 3), round(s, 3), round(v, 3))}`", inline = True)
        embed.add_field(name = "YIQ Value", value = f"`{(round(y, 5), round(i, 5), round(q, 5))}`", inline = True)

        embed.set_thumbnail(url = f"http://www.colourlovers.com/img/{hexcode}/200/200/image.png")
        embed.set_footer(text = "https://colourlovers.com | https://colorhexa.com")
        
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'design', aliases = ['screenshot'], usage = '<Website URL>')
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
            await ctx.send(embed = embed)
    
    @commands.command(brief = 'design', name = 'lorem', usage = '[characters (upto 2000)]')
    async def lorem(self, ctx, character_count: int = 502):
        """Generates dummy text. (lorem ipsum)"""

        if character_count > 2000:
            raise commands.BadArgument('character count exceeds 2000 limit.')

        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. " \
            "Aenean commodo ligula eget dolor. Aenean massa. " \
            "Cum sociis natoque penatibus et magnis dis parturient montes, " \
            "nascetur ridiculus mus. Donec quam felis, ultricies nec, " \
            "pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. " \
            "Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. " \
            "In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. " \
            "Nullam dictum felis eu pede mollis pretium. Integer tincidunt. " \
            "Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. " \
            "Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. " \
            "Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. " \
            "Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. " \
            "Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. " \
            "Nam eget dui. " \
            "Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, " \
            "sem quam semper libero, sit amet adipiscing sem neque sed ipsum. " \
            "Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. " \
            "Maecenas nec odio et ante tincidunt tempus. " \
            "Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. " \
            "Etiam sit amet orci eget eros faucibus tincidunt. " \
            "Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. " \
            "Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. " \
            "Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. " \
            "Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. " \
            "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; " \
            "In ac dui quis mi consectetuer lacinia. " \
            "Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. " \
            "Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. " \
            "Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestib"
        
        print(len(lorem_ipsum))
        dummy_text = lorem_ipsum[:character_count]

        await ctx.send(dummy_text)


    @commands.command(brief = 'useful', aliases = ['math', 'calculate'], usage = '<expression>')
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
            return await ctx.send(f"{self.emojis.cross} **Cannot compute. Make sure expression is valid.** `[ex {type(e).__name__}]`")

        embed = discord.Embed(
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )
        embed.add_field(name = equation, value = str(final))
        embed.set_footer(text = f"Evaluated by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    @commands.command(brief = 'useful', aliases = ['tz'], usage = "<timezone> [timezones...]")
    async def time(self, ctx, *timezones):
        """Show time(s) for specified timezone(s)"""

        if not timezones:
            raise commands.BadArgument('no timezones provided.')
            
        if len(timezones) > 24:
            raise commands.BadArgument('too many timezones to handle.')
        
        tzones = []
        for timezone in timezones:
            if not timezone in pytz.all_timezones_set:
                raise commands.BadArgument(f"'{timezone}' is an invalid timezone.")
            
            name = formatting.casify(timezone.replace('/', ' / '))
            timez = pytz.timezone(timezone)

            tzones.append((name, timez))
        
        main_timezone = tzones[0]
        utcnow = pytz.timezone('utc').localize(datetime.utcnow())
        main_astimezone = utcnow.astimezone(main_timezone[1]).replace(tzinfo = None)

        embed = discord.Embed(
            title = "Timzones",
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )
        for timezone in tzones:
            astimezone = utcnow.astimezone(timezone[1]).replace(tzinfo = None)
            # Calculate the difference between the two timezones.
            offset = relativedelta(main_astimezone, astimezone)

            diff = []
            if offset.days: diff.append(f"{abs(offset.days)} days")
            if offset.hours: diff.append(f"{abs(offset.hours)} hours")
            if offset.minutes: diff.append(f"{abs(offset.minutes)} minutes")
            
            diff = f"*`({', '.join(diff)})`*" if diff else ''

            strftime = datetime.now(tz = timezone[1]).strftime('%a, %b %d %I:%M %p')

            embed.add_field(
                name = f"{timezone[0]} Time",
                value = f"{strftime} {diff}",
                inline = False
            )

        await ctx.send(embed = embed)

    @commands.command(brief = 'useful', usage = "<url>")
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

    # Actually make these subcommands.
    @commands.command(brief = 'useful', usage = '<search/summary/random> [query]', aliases = ["wikipedia"])
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
    
    @commands.command(brief = 'useful', usage = '<"question"> ["option 1"] ["option 2"]')
    #@commands.has_permissions(manage_messages = True)
    @commands.guild_only()
    async def poll(self, ctx, question: str, yes: str = "yes", no: str = "no"):
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
        
    
    @commands.command(brief = 'useful', usage = '[code block]')
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

    @commands.command(brief = 'other', usage = '<@user/id> [confident (yes/no)]')
    async def guesstoken(self, ctx, member: discord.Member = None, confident: bool = False):
        """Guesses the user's token to some level of acccuracy."""

        member = member or ctx.author
        token_parts = [
            '####################',  # -> ID of the user.
            '######',  # -> Timestamp of token creation.
            '###########################'  # -> HMAC, Can't guess :/
        ]

        # User ID -> Base64 Encoding
        user_id = bytes(str(member.id), encoding = 'utf8')
        b64 = base64.b64encode(user_id)
        b64 = b64.decode()
        token_parts[0] = b64

        if confident:
            #return datetime.utcfromtimestamp(int.from_bytes(base64.b64decode(token_part + "=="), "big"))

            epoch = int(member.created_at.timestamp())
            discord_epoch = epoch - 1293840000

        await ctx.send(f"__**Non MFA Token:**__ **`{b64}.######.###########################`**")

    @commands.group(name = 'base64', brief = 'other', usage = '<encode/decode> [text]')
    async def bbase64(self, ctx):
        """Base64 Encode/Decode."""

        if not ctx.invoked_subcommand:
            raise commands.BadArgument('Missing <encode/decode> parameter.')
    
    @bbase64.command(name = 'encode')
    async def bbase64_encode(self, ctx, *, text: str):
        """Base64 Encode Text."""

        text = base64.urlsafe_b64encode(bytes(text, 'utf8')).decode()
        await ctx.send(f"**URL Safe Base64 Encoding:**\n```{text}```")
    
    @bbase64.command(name = 'decode')
    async def bbase64_decode(self, ctx, *, text: str):
        """Base64 Decode Text."""

        if text.startswith('`') and text.endswith('`'): text = text.strip('`')

        try:
            text = base64.urlsafe_b64decode(bytes(text, 'utf8')).decode()
        except Exception as ex:
            return await ctx.send(f"{self.emojis.cross} **Couldn't decode. Make sure text is a valid Base64 string.** `[ex {type(ex).__name__}]`")

        await ctx.send(f"```{text}```")
    
    @commands.group(name = 'base16', brief = 'other', usage = '<encode/decode> [text]')
    async def base16(self, ctx):
        """Base16 Encode/Decode."""
        
        if not ctx.invoked_subcommand:
            raise commands.BadArgument('Missing <encode/decode> parameter.')
            
    @base16.command(name = 'encode')
    async def base16_encode(self, ctx, *, text: str):
        """Base16 encode text."""

        text = base64.b16encode(bytes(text, 'utf8')).decode()
        await ctx.send(f"**Base16 Encoding:**\n```{text}```")
    
    @base16.command(name = 'decode')
    async def base16_decode(self, ctx, *, text: str):
        """Base16 decode text."""

        if text.startswith('`') and text.endswith('`'): text = text.strip('`')

        try:
            text = base64.b16decode(bytes(text, 'utf8')).decode()
        except Exception as ex:
            return await ctx.send(f"{self.emojis.cross} **Couldn't decode. Make sure text is a valid Base16 string.** `[ex {type(ex).__name__}]`")
        
        await ctx.send(f"```{text}```")
    
    @commands.group(name = 'base32', brief = 'other', usage = '<encode/decode> [text]')
    async def base32(self, ctx):
        """Base32 Encode/Decode."""
        
        if not ctx.invoked_subcommand:
            raise commands.BadArgument('Missing <encode/decode> parameter.')
            
    @base32.command(name = 'encode')
    async def base32_encode(self, ctx, *, text: str):
        """Base32 encode text."""

        text = base64.b32encode(bytes(text, 'utf8')).decode()
        await ctx.send(f"**Base32 Encoding:**\n```{text}```")
    
    @base32.command(name = 'decode')
    async def base32_decode(self, ctx, *, text: str):
        """Base32 decode text."""

        if text.startswith('`') and text.endswith('`'): text = text.strip('`')

        try:
            text = base64.b32decode(bytes(text, 'utf8')).decode()
        except Exception as ex:
            return await ctx.send(f"{self.emojis.cross} **Couldn't decode. Make sure text is a valid Base32 string.** `[ex {type(ex).__name__}]`")
        
        await ctx.send(f"```{text}```")
    
    @commands.group(name = 'base85', brief = 'other', usage = '<encode/decode> [text]')
    async def base85(self, ctx):
        """Base85 Encode/Decode."""
        
        if not ctx.invoked_subcommand:
            raise commands.BadArgument('Missing <encode/decode> parameter.')
            
    @base85.command(name = 'encode')
    async def base85_encode(self, ctx, *, text: str):
        """Base85 encode text."""

        text = base64.b85encode(bytes(text, 'utf8')).decode()
        await ctx.send(f"**Base85 Encoding:**\n```{text}```")
    
    @base85.command(name = 'decode')
    async def base85_decode(self, ctx, *, text: str):
        """Base85 decode text."""

        if text.startswith('`') and text.endswith('`'): text = text.strip('`')

        try:
            text = base64.b85decode(bytes(text, 'utf8')).decode()
        except Exception as ex:
            return await ctx.send(f"{self.emojis.cross} **Couldn't decode. Make sure text is a valid Base85 string.** `[ex {type(ex).__name__}]`")
        
        await ctx.send(f"```{text}```")

def setup(bot):
    bot.add_cog(UtilityCog(bot))