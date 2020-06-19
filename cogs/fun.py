import discord
from discord.ext import commands
from utils import default
import random
import aiohttp
import asyncio


class FunCog(commands.Cog):
    """Entertainment / Fun Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.bot_prefix = '.'
    
    @commands.command(aliases=["feline", "tom", "mouser", "pussy", "meow"])
    async def cat(self, ctx, num : int = 0, fact : bool = False):
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
    async def dog(self, ctx, num : int = 0, fact : bool = False):
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
    
    @commands.command(name = "bird", aliases = ["birb", "ave", "birdie"])
    async def bird(self, ctx, num : int = 0, fact : bool = False):
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
    async def fox(self, ctx, num : int = 0, fact : bool = False):
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




    

def setup(bot):
    bot.add_cog(FunCog(bot))