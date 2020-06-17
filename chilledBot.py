import discord
from discord.ext import commands
from utils import default

import sys, traceback, os

"""
    A simple discord bot made using Python, utilizing the cogs functionality.

    The bot is meant to be a utility first, moderation, and music bot.
    It is specifically tailored for study, chill, and LoFi servers.
"""

def get_prefix(bot, message):
    """A callable prefix for the bot."""

    # We support multiple prefixes.
    prefixes = ['.', 'c.']

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
    description = "A simple, fun, and utility bot that can also do moderation."
)
bot.remove_command('help')

# We load the extensions here from the initial_extensions list.

#for file in os.listdir("cogs"):
#    if file.endswith('.py'):
#        name = file[:-3]
#        bot.load_extension(f"cogs.{name}")

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f"[Cogs] Successfully loaded {extension}.")
    except Exception as ex:
        print(f"[Cogs] Failed to load {extension} due to exception {ex}")

@bot.event
async def on_connect():
    """"http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_connect"""

    os.system('clear')
    print("ChilledBot by Zeesmic#8023...", '\n')

    print("[Connection] Connecting to Discord...")
    print("[Connected] Established connection with Discord.")

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print("[Ready] ChilledBot has started.")
    print(f"[Login] Logged in as {bot.user.name} ({bot.user.id})")

    # Changing the bot presence to "Listening to LoFi"
    await bot.change_presence(
        activity = discord.Activity (
            name = "LoFi",
            type = discord.ActivityType.listening
        ),
        status = discord.Status.idle,
        afk = True
    )

@bot.event
async def on_disconnect():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_disconnect"""

    print("[Disconnected] Lost connection with Discord.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send("<:red_mark:694527415904370799> **This command can't be used in DMs.** `[ex GuildOnly]`")
        return
    if isinstance(error, commands.DisabledCommand):
        await ctx.send("<:red_mark:694527415904370799> **This command is disabled.** `[ex CmdDisabled]`")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"<:red_mark:694527415904370799> **This command is on cooldown. Try again in {error.retry_after:.2f}s.** `[ex Cooldown]`")
        return

# Start the bot.
bot.run(TOKEN, bot = True, reconnect = True)