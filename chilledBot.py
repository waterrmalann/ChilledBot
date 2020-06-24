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

        # Management 🛠️ 
        #Developer ⌨️

        embed.add_field(
            name = '» Utility 🔧',
            value = f"`{prefix}help utility`",
            inline = True
        )
        embed.add_field(
            name = '» Moderation 🛡️',
            value = f"`{prefix}help mod`",
            inline = True
        )
        embed.add_field(
            name = '» Information 📖', 
            value = f"`{prefix}help info`",
            inline = True
        )
        embed.add_field(
            name = '» Fun/Misc 🎲',
            value = f"`{prefix}help fun`",
            inline = True
        )
        embed.add_field(
            name = '» Music 🎵',
            value = f"`{prefix}help music`",
            inline = True
        )
        embed.add_field(
            name = '» Config ⚙️',
            value = f"`{prefix}help config`", 
            inline = True
        )

        embed.add_field(
            name = '» Support Server :link:',
            value = '**[https://discord.gg/nG86J2U](https://www.youtube.com/watch?v=dQw4w9WgXcQ)**'
        )

        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    elif request == 'utility':
        
        cmds = bot.get_cog("UtilityCog").get_commands()
        # {"help": "Gives help", ["helpme", "commands"]}
        #commands = {cmd.name: (cmd.help, cmd.aliases) for cmd in cmds if not cmd.hidden}

        commands = '\n'.join(f"**{cmd.name}**: {cmd.help}" for cmd in cmds if not cmd.hidden)
        
        embed = discord.Embed(title = f"Utility Commands List.", color = colors.primary)
        embed.add_field(
            name = "Commands | The prefix is '.'",
            value = commands
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    elif request == 'mod':

        cmds = bot.get_cog("ModerationCog").get_commands()
        # {"help": "Gives help", ["helpme", "commands"]}
        #commands = {cmd.name: (cmd.help, cmd.aliases) for cmd in cmds if not cmd.hidden}

        commands = '\n'.join(f"**{cmd.name}**: {cmd.help}" for cmd in cmds if not cmd.hidden)
        
        embed = discord.Embed(title = f"Moderation Commands List.", color = colors.primary)
        embed.add_field(
            name = "Commands | The prefix is '.'",
            value = commands
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        
    elif request == 'music':
        embed = discord.Embed(title = f"Music Commands List.", color = colors.primary)

        embed.add_field(name="👩🏻‍🏭 Work-In-Progress", value="This module is a work in progress.")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    elif request == 'fun':
        cmds = bot.get_cog("FunCog").get_commands()
        # {"help": "Gives help", ["helpme", "commands"]}
        #commands = {cmd.name: (cmd.help, cmd.aliases) for cmd in cmds if not cmd.hidden}

        commands = '\n'.join(f"**{cmd.name}**: {cmd.help}" for cmd in cmds if not cmd.hidden)
        
        embed = discord.Embed(title = f"Fun Commands List.", color = colors.primary)
        embed.add_field(
            name = "Commands | The prefix is '.'",
            value = commands
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    elif request == 'info':
        cmds = bot.get_cog("InformationCog").get_commands()
        # {"help": "Gives help", ["helpme", "commands"]}
        #commands = {cmd.name: (cmd.help, cmd.aliases) for cmd in cmds if not cmd.hidden}

        commands = '\n'.join(f"**{cmd.name}**: {cmd.help}" for cmd in cmds if not cmd.hidden)
        
        embed = discord.Embed(title = f"Information Commands List.", color = colors.primary)
        embed.add_field(
            name = "Commands | The prefix is '.'",
            value = commands
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    elif request == 'config':
        cmds = bot.get_cog("ConfigCog").get_commands()
        # {"help": "Gives help", ["helpme", "commands"]}
        #commands = {cmd.name: (cmd.help, cmd.aliases) for cmd in cmds if not cmd.hidden}

        commands = '\n'.join(f"**{cmd.name}**: {cmd.help}" for cmd in cmds if not cmd.hidden)
        
        embed = discord.Embed(title = f"Config Commands List.", color = colors.primary)
        embed.add_field(
            name = "Commands | The prefix is '.'",
            value = commands
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    # Commands
    elif request in bot.all_commands:

        command = bot.all_commands.get(request)

        text = f"**Usage:** `.{command.name} {command.usage}`" if command.usage else f"**Usage:** `.{command.name}`"
        if command.aliases: text += f"\n**Aliases:** `{', '.join(command.aliases)}`"

        embed = discord.Embed(
            title = f"Command: `.{command.name}`",
            description = text,
            color = colors.primary
        )
        embed.set_footer(text = command.help)

        await ctx.send(embed = embed)


    else:
        embed = discord.Embed(description = f'**Usage:** {prefix}help <module/command>',color = colors.primary)
        embed.set_footer(text='Shows the command list.')

        await ctx.send(embed=embed)


@bot.command()
async def botstats(ctx):
    """Detailed statistics of the bot"""

    mem = psutil.virtual_memory()

    embed = discord.Embed(
        title = f"[Statistics] {bot.user.name} (`{str(bot.user.id)}``)",
        color = colors.secondary
    )
    
    embed.add_field(
        name = 'Discord.py',
        value = f'[{discord.__version__}](https://discordpy.readthedocs.io/en/latest/)',
        inline = True
    )
    embed.add_field(
        name = 'Python',
        value = f'[{platform.python_version()}](https://www.python.org/)',
        inline=True
    )
    embed.add_field(
        name = 'OS',
        value = f'{platform.system()}, {platform.machine()}',
        inline = True
    )
    embed.add_field(
        name = 'Memory Usage',
        value = f'{round(mem.used / 1024 / 1024 / 1024, 2)}MB',
        inline = True
    )
    embed.add_field(
        name = 'Guilds',
        value = len(bot.guilds),
        inline = True
    )
    embed.add_field(
        name = 'Users',
        value = len(bot.users),
        inline = True
    )

    embed.add_field(
        name='Uptime',
        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())),
        inline=True
    )
    embed.add_field(
        name = 'Loaded Cogs',
        value = len(bot.cogs),
        inline = True
    )
    embed.add_field(
        name = "Loaded Commands",
        value = len(bot.commands),
        inline = True
    )
    embed.add_field(
        name = 'Created on',
        value = f'{bot.user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")}',
        inline = False
    )
    embed.add_field(
        name = 'File size',
        value = '44.0 KB (45,056 bytes)\n7.0 KB (7,221 bytes)',
        inline = False
    )
    embed.add_field(
        name = 'Silent Mode',
        value = False,
        inline = False
    )

    embed.set_footer(text = f"Made with ❤ in Python {platform.python_version()} by Zeesmic#8023", icon_url = 'http://i.imgur.com/5BFecvA.png')
    await ctx.send(embed = embed)

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