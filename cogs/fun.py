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

        self.cat_facts = [
            "The oldest known pet cat existed 9,500 years ago.",
            "Cats spend 70% of their lives sleeping.",
            "A cat was the Mayor of an Alaskan town for 20 years.",
            "The record for the longest cat ever is 48.5 inches.",
            "The richest cat in the world had £7 million.",
            "Cats walk like camels and giraffes.",
            "Isaac Newton invented the cat door.",
            "In 1963 a cat went to space.",
            "Ancient Egyptians would shave off their eyebrows when their cats died",
            "House cats share 95.6% of their genetic makeup with tigers",
            "A house cat can reach speeds of up to 30mph",
            "The oldest cat in the world was 38 years old!",
            "The record for the loudest purr is 67.8db(A) (nearly the same as that of a shower)."
        ]
    
    @commands.command(aliases=["feline", "tom", "mouser", "pussy", "meow"])
    async def cat(self, ctx):
        """Fetches a random cat picture from the internet."""
        choices = ("Meow... :cat:", "Meow :heart_eyes_cat:", "Here's a feline for you. :cat2:")
        choice = random.choice(choices)

        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://thecatapi.com/api/images/get?format=src&type=png") as r:
                image = r.url

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = "http://thecatapi.com")

        await ctx.send(embed = embed)

        if random.randint(1, 10) < 4:  # We'll do 30% chance to get a cat fact.
            await ctx.send(f"**Did you know?** {random.choice(self.cat_facts)}")

def setup(bot):
    bot.add_cog(FunCog(bot))