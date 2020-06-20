# Discord.
import discord
# Command / Event Handler.
from discord.ext import commands
# JSON Parser / Logging Functions.
from utils import default, logger
# DateTime Parser.
from datetime import datetime
# Operating System Functions.
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

config = default.get("config.json")
emojis = default.get("emojis.json")
colors = default.get("colors.json")

bot = commands.AutoShardedBot(
    command_prefix = get_prefix,
    description = "A simple, fun, and utility bot that can also do moderation.",
    owner_ids = set(config.bot_owners)
)

bot.remove_command('help')
prefix = '.'

# We load the extensions here from the initial_extensions list.

#for file in os.listdir("cogs"):
#    if file.endswith('.py'):
#        name = file[:-3]
#        bot.load_extension(f"cogs.{name}")

os.system('clear')
print("ChilledBot by Zeesmic#8023...", '\n')
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f"[Cogs] Successfully loaded {extension}.")
    except Exception as ex:
        print(f"[Cogs] Failed to load {extension} due to exception {ex}")
print()

"""@bot.command()
async def help(ctx):
    commands = []
    for cog in bot.cogs:
        for cmd in bot.get_cog(cog).get_commands():
            commands.append(cmd.name)
    await ctx.send(', '.join(commands))"""

@bot.command(aliases = ['cmds', 'commands', 'helpme'])
async def help(ctx, param = 'help'):
    """Gives a list of bot commands"""

    request = param.strip().lower()

    if request == 'help':
        
        embed = discord.Embed(
            title = f'Bot Help [Prefix: {prefix}]',
            color = colors.primary
        )

        embed.add_field(
            name = '» Utility :wrench:',
            value = f"`{prefix}help utility`",
            inline = True
        )
        embed.add_field(
            name = '» Moderation :hammer:',
            value = f"`{prefix}help mod`",
            inline = True
        )
        embed.add_field(
            name = '» Information :book:', 
            value = f"`{prefix}help info`",
            inline = True
        )
        embed.add_field(
            name = '» Fun :game_die:',
            value = f"`{prefix}help fun`",
            inline = True
        )
        embed.add_field(
            name = '» Music :musical_note:',
            value = f"`{prefix}help music`",
            inline = True
        )
        embed.add_field(
            name = '» Config :gear:',
            value = f"`{prefix}help config`", 
            inline = True
        )

        embed.add_field(
            name = '» Support Server :link:',
            value = '**[https://discord.gg/nG86J2U](https://www.youtube.com/watch?v=dQw4w9WgXcQ)**'
        )

        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

    elif request == 'utility':
        embed = discord.Embed(title = f"{config.bot_name} Utility Commands.", color = colors.primary)

        embed.add_field(name="Math :triangular_ruler:", value="math, add, subtract, multiply, divide")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

    elif request == 'mod':
        embed = discord.Embed(title = f"{config.bot_name} Moderation Commands.", color = colors.primary)

        embed.add_field(name="String", value="x, y, z")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    elif request == 'music':
        embed = discord.Embed(title = f"{config.bot_name} Music Commands.", color = colors.primary)

        embed.add_field(name="String", value="x, y, z")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    elif request == 'fun':
        embed = discord.Embed(title = f"{config.bot_name} Fun Commands.", color = colors.primary)

        embed.add_field(name="String", value="roastme")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    elif request == 'info':
        embed = discord.Embed(title = f"{config.bot_name} Information Commands.", color = colors.primary)

        embed.add_field(name="String", value="x, y, z")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    elif request == 'config':
        embed = discord.Embed(title = f"{config.bot_name} Configuration Commands.", color = colors.primary)

        embed.add_field(
        name = "Bot Account Configuration",
        value = f"""
        **{prefix}setprefix** : Set the bot's prefix.
        **{prefix}
        """
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    else:
        embed = discord.Embed(description = f'**Usage:** {prefix}help <help/utility/music/fun/info/config/mod>',color = colors.primary)
        embed.set_footer(text='Shows the command list.')

        await ctx.send(embed=embed)


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

    #await logger.log(bot, "**[Ready] ChilledBot has started.**")
    #await logger.log(bot, f"**[Login] Logged in as {bot.user.name} ({bot.user.id}).**")
    #await logger.log(bot, f"**[On] {datetime.now().strftime('%A, %B %d %Y @ %H:%M:%S %p')}**")

@bot.event
async def on_disconnect():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_disconnect"""

    print("[Disconnected] Lost connection with Discord.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send(f"{emojis.cross} **This command can't be used in DMs.** `[ex GuildOnly]`")
        return
    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f"{emojis.cross} **This command is disabled.** `[ex CmdDisabled]`")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{emojis.neutral} **This command is on cooldown. Try again in {error.retry_after:.2f}s.** `[ex Cooldown]`")
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send(f"{emojis.cross} **You are not authorized to use this command.** `[ex AuthError]`")
        return

# Start the bot.
bot.run(os.environ.get("BOT_TOKEN"), bot = True, reconnect = True)