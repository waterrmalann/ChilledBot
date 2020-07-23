# Discord
import discord
# Command Handler
from discord.ext import commands
# JSON Parser
from utils import default


class HelpCog(commands.Cog, name = "Help"):
    """Bot Help."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.bot_prefix = '.'
        self.hidden = True
    
    @commands.command(name = 'help', aliases = ['cmds', 'commands', 'helpme'])
    async def _help(self, ctx, param: str = 'help'):
        """Gives a list of bot commands"""

        request = param.strip().lower()

        if request == 'help' or not request:
            
            embed = discord.Embed(
                title = f'Bot Help [Prefix: {self.bot_prefix}]',
                color = self.colors.primary
            )

            # Management 🛠️ 
            #Developer ⌨️

            embed.add_field(
                name = '» Utility 🔧',
                value = f"`{self.bot_prefix}help utility`",
                inline = True
            )
            embed.add_field(
                name = '» Moderation 🛡️',
                value = f"`{self.bot_prefix}help mod`",
                inline = True
            )
            embed.add_field(
                name = '» Information 📖', 
                value = f"`{self.bot_prefix}help info`",
                inline = True
            )
            embed.add_field(
                name = '» Fun/Misc 🎲',
                value = f"`{self.bot_prefix}help fun`",
                inline = True
            )
            embed.add_field(
                name = '» Music 🎵',
                value = f"`{self.bot_prefix}help music`",
                inline = True
            )
            embed.add_field(
                name = '» Config ⚙️',
                value = f"`{self.bot_prefix}help config`", 
                inline = True
            )

            embed.add_field(
                name = '» Support Server :link:',
                value = f'**[{self.config.guild_support_invite}](https://www.youtube.com/watch?v=dQw4w9WgXcQ)**'
            )

            embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

            await ctx.send(embed = embed)
        
        elif request in self.bot.all_commands:

            command = self.bot.all_commands.get(request)

            command_info = []
            command_info.append(f"**Usage:** `.{command.name} {command.usage}`" if command.usage else f"**Usage:** `.{command.name}`")
            command_info.append(f"**Description:** {command.help}")
            if command.aliases: command_info.append(f"**Aliases:** `{', '.join(command.aliases)}`")

            embed = discord.Embed(
                title = f"Command: `.{command.name}`",
                description = '\n'.join(command_info),
                color = self.colors.primary
            )

            if command.usage:
                embed.set_footer(text = '<> Required | [] Optional')
            else: 
                embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

            await ctx.send(embed = embed)

        else:
            for cogg in self.bot.cogs:
                cog = self.bot.get_cog(cogg)
                if not cog.hidden:
                    if request in cog.aliases:
                        name = cog.name
                        commands = cog.get_commands()
                        cats = cog.categories
                        
                        cmds = {cat: [] for cat in cats}

                        for command in commands:
                            cmds[command.brief].append(command)
                        
                        embed = discord.Embed(title = f"{name} | Command List", color = self.colors.primary)
                        for key, value in cmds.items():
                            embed.add_field(
                                name = key.title(),
                                value = '\n'.join(f"`{cmd.name}` {cmd.help}" for cmd in value if not cmd.hidden),
                                inline = False
                            )
                        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed = embed)
            else:
                embed = discord.Embed(description = f'**Usage:** {self.bot_prefix}help <module/command>', color = self.colors.primary)
                embed.set_footer(text = 'Shows the command list.')
                return await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))