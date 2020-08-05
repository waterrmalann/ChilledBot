# Discord.
import discord
# Command / Event Handler.
from discord.ext import commands
# Operating System Functions.
import os, sys, platform, psutil
import traceback
# Time Value Manipulation.
import time
# DateTime Parser.
from datetime import datetime
# JSON Parser.
from utils import default, formatting
# File Line Counter.
from line_counter import count_lines
import random

"""
   A simple utility-first discord bot written in Python using the Discord.py library.

   ChilledBot was designed to assist productivity with it's focus on utility features.

   The bot is multi-purpose, so there's more useful features available such as server management and entertainment commands.

    Written by Alan Biju Varghese (alanthekiwi)
"""

config = default.get("config.json")
emojis = default.get("emojis.json")
colors = default.get("colors.json")

def get_prefix(bot, message):
    """A callable prefix for the bot."""

    # We support multiple prefixes.
    prefixes = config.bot_prefix

    # Only allow '?' as a prefix in DMs.
    if not message.guild: return '?'

    # We also allow mentions while in guilds.
    return commands.when_mentioned_or(*prefixes)(bot, message)

## Cogs ##
initial_extensions = [
    'cogs.owners',
    'cogs.utility',
    'cogs.information',
    'cogs.fun',
    'cogs.moderation',
    'cogs.config'
]



bot = commands.AutoShardedBot(
    command_prefix = get_prefix,
    description = "A simple, fun, and utility bot that can also do moderation.",
    owner_ids = set(config.bot_owners)
)
bot.launch_time = datetime.utcnow()
bot.remove_command('help')
bot.command_counter = 0
prefix = '.'


# Startup Stuff
os.system('clear')
print(r"   ________    _ ____         __   ____        __ ")
print(r"  / ____/ /_  (_) / /__  ____/ /  / __ )____  / /_")
print(r" / /   / __ \/ / / / _ \/ __  /  / __  / __ \/ __/")
print(r"/ /___/ / / / / / /  __/ /_/ /  / /_/ / /_/ / /_  ")
print(r"\____/_/ /_/_/_/_/\___/\__,_/  /_____/\____/\__/  ")
print("\n", "Version: 1.0.0 | Closed Beta | By Zeesmic#8023", "\n")

# Loading all the command/event extensions.
for extension in config.cogs:
    try:
        bot.load_extension(extension)
        print(f"[Cogs] Successfully loaded {extension}.")
    except Exception as error:
        print()
        print(f"[Cogs] Failed to load {extension}. due to exception {error}")
        print(f"Exception: {error}\nException (Type): {type(error)}\nException (Traceback): {error.__traceback__}")
        #traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
        print()
print()

@bot.event
async def on_connect():
    """"http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_connect"""

    print("[Connection] Connecting to Discord...")
    print("[Connected] Established connection with Discord.")

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print("[Ready] ChilledBot has started.")
    print(f"[Login] Logged in as {bot.user.name} ({bot.user.id})")

    # Changing the bot presence to "Listening to LoFi"
    await bot.change_presence(
        activity = discord.Activity(
            name = "LoFi",
            type = discord.ActivityType.listening
        ),
        status = discord.Status.idle,
        afk = True
    )

    # Loading bot channels into variables.
    bot.channel_logs = bot.get_channel(config.channel_logs)
    bot.channel_cmdexceptions = bot.get_channel(config.channel_cmdexceptions)
    bot.channel_exceptions = bot.get_channel(config.channel_exceptions)
    bot.channel_guilds = bot.get_channel(config.channel_guilds)

    embed = discord.Embed(
        title = "[Ready] ChilledBot has started.",
        description = f"Logged in as **{bot.user}** (`{bot.user.id}`)",
        color = colors.primary
    )
    embed.set_footer(text = default.datefr(datetime.now()))
    await bot.channel_logs.send(embed = embed)

@bot.event
async def on_disconnect():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_disconnect"""

    print("[Disconnected] Lost connection with Discord.")

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title = f"[Guild Joined] {guild.name} (`{guild.id}`)",
        description = f"**Owned by:** {guild.owner} (`{guild.owner.id}`)\n" \
            f"**Members:** {guild.member_count}\n" \
            f"**Region:** {guild.region}",
        color = colors.primary,
    )
    embed.set_footer(text = default.datefr(datetime.now()))
    embed.set_thumbnail(url = guild.icon_url)
    await bot.channel_guilds.send(embed = embed)

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
        title = f"[Guild Removed] {guild.name} (`{guild.id}`)",
        description = f"**Owned by:** {guild.owner} (`{guild.owner.id}`)",
        color = colors.primary
    )
    embed.set_footer(text = default.datefr(datetime.now()))
    await bot.channel_guilds.send(embed = embed)

@bot.event
async def on_command(ctx):
    """https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.on_command"""
    
    print(f"\n[CMD] {ctx.command.qualified_name} by {ctx.author} in {ctx.guild.name}")

@bot.event
async def on_command_completion(ctx):
    """https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.on_command_completion"""

    print(f"[CMD] {ctx.command.qualified_name} Successful.")
    bot.command_counter += 1

@bot.event
async def on_command_error(ctx, error):
    """https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.on_command_error"""
    if hasattr(ctx.command, 'on_error'): return
    
    ignored = (commands.CommandNotFound, commands.MissingPermissions)
    input_errors = (commands.MissingRequiredArgument, commands.BadArgument)
    error = getattr(error, 'original', error)
    
    if isinstance(error, ignored):
        return

    # On Cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f"{emojis.neutral} **This command is on cooldown. Try again in {error.retry_after:.2f}s.** `[ex Cooldown]`", delete_after = 5)
    
    # Missing / Invalid / Bad Arguments
    elif isinstance(error, input_errors):

        description_values = []
        description_values.append(f"**Usage:** `{ctx.command.qualified_name} {ctx.command.usage}`")
        description_values.append(f"**Description:** {ctx.command.help}")
        if error: description_values.append(f"\n**`{error}`**")

        embed = discord.Embed(
            title = f"Help: {ctx.command.qualified_name}",
            description = '\n'.join(description_values),
            color = colors.primary
        )

        if ctx.command.parent:
            embed.set_footer(text = f"{ctx.command.cog.name}/{ctx.command.parent.brief.title()}/{ctx.command.parent.name}")
        else:
            embed.set_footer(text = f"{ctx.command.cog.name}/{ctx.command.brief.title()}")

        return await ctx.send(embed = embed)

    # Disabled
    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f"{emojis.cross} **This command is disabled.** `[ex CmdDisabled]`")

    # Guild Only
    elif isinstance(error, commands.NoPrivateMessage):
        try: return await ctx.author.send(f"{emojis.cross} **This command can't be used in DMs.** `[ex GuildOnly]`")
        except: pass
    
    # Not Authorized
    elif isinstance(error, commands.NotOwner):
        return await ctx.send(f"{emojis.cross} **You are not authorized to use this command.** `[ex AuthError]`")
    
    elif isinstance(error, commands.BotMissingPermissions):
        permissions = [f"`{formatting.casify(i)}`" for i in error.missing_perms]
        return await ctx.send(f"{emojis.cross} **I miss the following {'permissions' if len(error.missing_perms) > 1 else 'permission'} required to run this command:** {formatting.join_words(permissions)}")
    
    # NSFW Channel Required
    elif isinstance(error, commands.NSFWChannelRequired):
        return await ctx.send(f"🔞 **This command only works in NSFW channels.** `[ex NSFWRequired]`")
    
    # Unhandled
    else:

        desc_values = []
        desc_values.append("This command has raised an unexpected error. My developers have been notified of this issue!")
        desc_values.append(f"```\n{error}\n```")
        desc_values.append(f"[Visit the support server to learn more.]({config.guild_support_invite})")

        embed = discord.Embed(
            title = "⚠️ **Unhandled Exception**",
            description = '\n'.join(desc_values),
            color = colors.error,
            timestamp = datetime.utcnow()
        )
        embed.set_footer(text = f"Exception caused by {ctx.command.qualified_name}")
        await ctx.send(embed = embed)

        exception_embed = discord.Embed(
            title = "⚠️ Unhandled Command Exception",
            color = colors.error,
            timestamp = datetime.utcnow()
        )
        exception_embed.add_field(
            name = "Command",
            value = f"{ctx.command.qualified_name} ({ctx.command.cog_name})",
            inline = False
        )
        exception_embed.add_field(
            name = "Error",
            value = f"**{type(error)}**\n" \
                f"```k\n{error}```" \
                f"```k\n{error.__traceback__}```",
            inline = False
        )
        exception_embed.add_field(
            name = "Invoked by",
            value = f"{ctx.author} (`{ctx.author.id}`)",
            inline = False
        )
        exception_embed.add_field(
            name = "Invoked in",
            value = f"{ctx.guild} (`{ctx.guild.id}`)\n" \
                f"#{ctx.channel} (`{ctx.channel.id}`)",
            inline = False
        )
        exception_embed.add_field(
            name = "Message Content",
            value = ctx.message.content,
            inline = False
        )
        await bot.channel_cmdexceptions.send(embed = exception_embed)

    print('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)

# Start the bot.
bot.run(os.environ.get("BOT_TOKEN"), bot = True, reconnect = True)