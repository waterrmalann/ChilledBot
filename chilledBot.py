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
from utils import default
# File Line Counter.
from line_counter import count_lines

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
prefix = '.'

# We load the extensions here from the initial_extensions list.

#for file in os.listdir("cogs"):
#    if file.endswith('.py'):
#        name = file[:-3]
#        bot.load_extension(f"cogs.{name}")

os.system('clear')
print("ChilledBot by Zeesmic#8023...", '\n')
for extension in config.cogs:
    try:
        bot.load_extension(extension)
        print(f"[Cogs] Successfully loaded {extension}.")
    except Exception as ex:
        print(f"[Cogs] Failed to load {extension} due to exception {ex}")
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

    bot.channel_logs = bot.get_channel(config.channel_logs)
    bot.channel_cmdexceptions = bot.get_channel(config.channel_cmdexceptions)
    bot.channel_exceptions = bot.get_channel(config.channel_exceptions)
    bot.channel_guilds = bot.get_channel(config.channel_guilds)

    await bot.channel_logs.send(
        "**[Ready]** __ChilledBot__ has started.\n" \
        f"**[Login]** Logged in as **{bot.user.name}** (`{bot.user.id}`).\n" \
        f"**[On]** {default.datefr(datetime.now())}"
    )

@bot.event
async def on_disconnect():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_disconnect"""

    print("[Disconnected] Lost connection with Discord.")

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'): return
    
    ignored = (commands.CommandNotFound)
    input_errors = (commands.MissingRequiredArgument, commands.BadArgument)
    error = getattr(error, 'original', error)
    
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f"{emojis.neutral} **This command is on cooldown. Try again in {error.retry_after:.2f}s.** `[ex Cooldown]`")
    
    elif isinstance(error, input_errors):
        embed = discord.Embed(description = f"**Syntax:** {ctx.command.qualified_name} {ctx.command.usage}", color = colors.primary)
        if error: embed.add_field(name = "Error", value = error)
        embed.set_footer(text = ctx.command.help)
        return await ctx.send(embed = embed)

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f"{emojis.cross} **This command is disabled.** `[ex CmdDisabled]`")

    elif isinstance(error, commands.NoPrivateMessage):
        try: return await ctx.author.send(f"{emojis.cross} **This command can't be used in DMs.** `[ex GuildOnly]`")
        except: pass
    
    elif isinstance(error, commands.NotOwner):
        return await ctx.send(f"{emojis.cross} **You are not authorized to use this command.** `[ex AuthError]`")
    
    else:

        desc_values = []
        desc_values.append("This command has raised an unexpected error. My developers have been notified of this issue!")
        desc_values.append(f"```\n{error}\n```")
        desc_values.append(f"[Visit the support server to learn more.]({config.guild_support_invite})")

        embed = discord.Embed(
            title = "⚠️ **Unhandled Exception**",
            description = '\n'.join(desc_values),
            color = colors.error
        )
        embed.set_footer(text = f"Exception caused by {ctx.command.qualified_name}")
        await ctx.send(embed = embed)

        exception_embed = discord.Embed(
            title = "⚠️ **Unhandled Command Exception**",
            color = colors.error
        )
        exception_embed.add_field(
            name = "Command",
            value = f"`{ctx.command.qualified_name}` from `{ctx.command.cog_name}`",
            inline = False
        )
        exception_embed.add_field(
            name = "Error",
            value = f"**Type:** {type(error)}\n" \
                f"```{error}```\n" \
                f"```{error.__traceback__}```",
            inline = False
        )
        exception_embed.add_field(
            name = "Context",
            value = f"**Command Invoked by:** {ctx.author} ({ctx.author.id})\n" \
                f"**Command Invoked in:** {ctx.guild} ({ctx.guild.id} #{ctx.channel})\n" \
                f"**Command Message:** {ctx.message.content}",
            inline = False
        )
        exception_embed.timestamp = datetime.utcnow()
        await bot.channel_cmdexceptions.send(embed = exception_embed)

    print('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)

# Start the bot.
bot.run(os.environ.get("BOT_TOKEN"), bot = True, reconnect = True)