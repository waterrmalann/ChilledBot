import discord

from utils import default
from discord.ext import commands

emojis = default.get("emojis.json")

async def check_modcmd_perms(ctx, member):
    """Permission check for moderation commands such as ban, kick, mute, etc..."""
    
    if member == ctx.author:
        return await ctx.send(f"{emojis.cross} **You can't {ctx.command.name} yourself, goober.**")
    if member.id == ctx.bot.user.id:
        if ctx.command.name in {'kick', 'ban', 'softban', 'hackban'}:
            return await ctx.send(f"{emojis.cross} **You can't {ctx.command.name} me. Use `leave` instead.**")
        return await ctx.send(f"{emojis.cross} **You can't make me use this command on me.**")
    
    bot = ctx.guild.get_member(ctx.bot.user.id)
    if bot.top_role == member.top_role:
        return await ctx.send(f"{emojis.cross} **I can't {ctx.command.name} this user because they have the same permissions as me.**")
    if bot.top_role < member.top_role:
        return await ctx.send(f"{emojis.cross} **I can't {ctx.command.name} this user because they are above me in the role hierarchy.**")

    if ctx.author.id == ctx.guild.owner.id: return False

    if member.id == ctx.guild.owner.id:
        return await ctx.send(f"{emojis.cross} **You can't {ctx.command.name} the owner of this server.**")
    if ctx.author.top_role == member.top_role:
        return await ctx.send(f"{emojis.cross} **You can't {ctx.command.name} someone with the same permissions as you.**")
    if ctx.author.top_role < member.top_role:
        return await ctx.send(f"{emojis.cross} **You can't {ctx.command.name} someone above you in the role hierarchy.**")
