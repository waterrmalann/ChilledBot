# Discord.
import discord
# Command Handler.
from discord.ext import commands
# JSON Parser.
from utils import default
# Randomly picked integers and choices.
import random
# Asynchronous Requests.
import aiohttp
# Optional Command Parameters.
import typing


class FunCog(commands.Cog):
    """Entertainment / Fun Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.bot_prefix = '.'

    @commands.command()
    async def notice(self, ctx, user : discord.Member = None):
        """Notice me senpai."""

        user = user or ctx.author

        hugs = [
            "`＼(^o^)／`",
            "`d=(´▽｀)=b`",
            "`⊂((・▽・))⊃`",
            "`⊂( ◜◒◝ )⊃`",
            "`⊂（♡⌂♡）⊃`",
        ]

        await ctx.send(f"{user.mention}, `{random.choice(hugs)}`")
    
    @commands.command(aliases=["feline", "tom", "mouser", "pussy", "meow"])
    async def cat(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random cat picture from the internet."""

        choices = ("Meow... :cat:", "Meow :heart_eyes_cat:", "Here's a feline for you. :cat2:")
        choice = random.choice(choices)

        if num > 3 or num < 1: num = random.randint(1, 3)  # 33%/33%/33% Chance

        if num == 1:
            url = "http://thecatapi.com/api/images/get?format=src&type=png"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    image = r.url
            url = "http://thecatapi.com"
        elif num == 2:
            url = "http://shibe.online/api/cats"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data[0]
        else:
            url = "https://some-random-api.ml/img/cat"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)

        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:  # We'll do 30% chance to get a cat fact.
            url = "https://catfact.ninja/fact"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    cat_fact = data['fact']
            await ctx.send(f"**Did you know?** {cat_fact}")

    @commands.command(aliases=["pupper", "woof", "doggo", "bork", "canine"])
    async def dog(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random dog picture from the internet."""

        choices = ("Woof :dog:", "Bork Bork :service_dog:", "Here's a canine for you. :dog2:", "Arf! :dog:")
        choice = random.choice(choices)

        if num > 3 or num < 1: num = random.randint(1, 3)  # 33%/33%/33% Chance

        if num == 1:
            url = "https://dog.ceo/api/breeds/image/random"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["message"]
        elif num == 2:
            url = "https://some-random-api.ml/img/dog"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["link"]
        else:
            url = "https://random.dog/woof.json"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["url"]
        
        if image.endswith(('.webm', '.mp4')):
            # Sending videos as a raw message because apparently discord embeds don't support videos.
            await ctx.send(image)
        else:
            embed = discord.Embed(title = choice, color = self.colors.primary)
            embed.set_image(url = image)
            embed.set_footer(text = url)
            await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/dog"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    fact = data['fact']
            await ctx.send(f"**Did you know?** {fact}")
            #https://dog-api.kinduff.com/api/facts  data["facts"][0]
    
    @commands.command(name = "bird", aliases = ["birb", "ave", "birdie"])
    async def bird(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random birb picture from the internet."""

        choices = ("🐦 Here's your birb.", "Here's a birdie for you. 🐦", "🐦 Here's a birdie.")
        choice = random.choice(choices)

        if num > 2 or num < 1: num = random.randint(1, 2)  # 50%/50% Chance

        if num == 1:
            url = "http://shibe.online/api/birds"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data[0]
        else:
            url = "https://some-random-api.ml/img/birb"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/bird"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(name = "fox", aliases = ["foxie", "arf"])
    async def fox(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random fox picture from the internet."""

        choices = ("🦊 Here's a fox.", "Here's a fox for you. 🦊", "🦊 Here's your fox.")
        choice = random.choice(choices)


        if num > 2 or num < 1: num = random.randint(1, 2)  # 50%/50% Chance

        if num == 1:
            url = "https://randomfox.ca/floof/"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["image"]
        else:
            url = "https://some-random-api.ml/img/fox"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/fox"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
            # Random Fox Fact: Did You Know? 
    
    @commands.command(name = "panda", aliases = ["achoo"])
    async def panda(self, ctx, fact : bool = False):
        """Fetches a random panda picture from the internet."""

        choices = ("🐼 Here's a panda.", "Here's a panda for you. 🐼", "🐼 Here's your panda!", "Here's your panda... 🐼")
        choice = random.choice(choices)

        url = "https://some-random-api.ml/img/panda"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                data = await r.json()
                image = data["link"]
        
        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/panda"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(name = "koala")
    async def koala(self, ctx, fact : bool = False):
        """Fetches a random koala picture from the internet."""

        choices = ("🐨 Here's a koala.", "Here's a cute koala for you. 🐨", "🐨 Here's your koala!", "Here's your koala... 🐨")
        choice = random.choice(choices)

        url = "https://some-random-api.ml/img/koala"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                data = await r.json()
                image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/koala"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    data = await r.json()
                    fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(name = "anime")
    async def uwu(self, ctx):
        """Fetches a random anime picture from the internet."""

        url = "http://api.cutegirls.moe/json"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                data = await r.json()
                image = data["data"]["image"]
                title = data["data"]["title"]
                link = data["data"]["link"]
                author = data["data"]["author"]
                sub = data["data"]["sub"]
        url = "http://api.cutegirls.moe"

        embed = discord.Embed(title = title, color = self.colors.primary, url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"{url} • r/{sub} • {author}")
        await ctx.send(embed = embed)
    
    @commands.command(name = "quote")
    async def quote(self, ctx):
        """Fetches a random quote from the internet."""

        url = "http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                data = await r.json()
                quote_text = data['quoteText']
                quote_author = data['quoteAuthor']
                quote_link = data['quoteLink']
        url = "http://api.forismatic.com/"

        embed = discord.Embed(
            color = self.colors.primary,
            description = f'*"{quote_text}"*\n**~ {quote_author}**'
        )
        embed.set_author(
            name = "Here's a quote...",
            url = quote_link,
            icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Cquote2_black.svg/1200px-Cquote2_black.svg.png"
        )
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(FunCog(bot))