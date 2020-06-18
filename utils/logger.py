import discord
from discord.ext import commands
from utils import default

config = default.get("config.json")

async def log(ctx, message):
    channel = ctx.bot.get_channel(config.channel_logs)
    await channel.send(f"[LOG] {message.strip()}")

async def error(ctx, message):
    channel = ctx.bot.get_channel(config.channel_errors)
    await channel.send(f"[ERROR LOG] {message.strip()}")