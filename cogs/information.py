# To-Do:
# >> Message Info
# >> Role Info
# >> Channel Info

# Discord.
import discord
# Command Handler.
from discord.ext import commands
# JSON Parser & Text Formatter.
from utils import default, formatting
# DateTime Parser.
from datetime import datetime

class InformationCog(commands.Cog):
    """Information-Related Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.emojis = default.get("emojis.json")
        self.bot_prefix = '.'
    
    @commands.command(aliases = ['pfp', 'pic'], usage = "[@user/id]")
    async def avatar(self, ctx, user: discord.Member = None):
        """Return the avatar of an user (if specified) or the author."""

        user = user or ctx.author
        
        embed = discord.Embed(
            title = user.name,
            color = self.colors.primary
        )
        embed.set_image(url = user.avatar_url)

        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Detailed information about the current guild the bot is in."""

        verification = str(ctx.guild.verification_level)
        if verification == 'none': verification = "[0] None"
        elif verification == 'low': verification = "[1] Low"
        elif verification == 'medium': verification = "[2] Medium"
        elif verification == 'high': verification = "[3] (╯°□°）╯︵ ┻━┻ (High)"
        else: verification = "[4] ┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻ (Extreme)"

        notification = ctx.guild.default_notifications
        if notification == 'all_messages': notification = "All Messages"
        else: notification = "Only Mentions"

        contentfilter = ctx.guild.explicit_content_filter
        if contentfilter == 'disabled': contentfilter = "Disabled"
        elif contentfilter == 'no_role': contentfilter = "Enabled for members with no role"
        else: contentfilter = "Enabled for all members"

        region = str(ctx.guild.region)
        if region in ('us-central', 'us-east', 'us-south', 'us-west'):region =  f"US {region[3:].capitalize()} :flag_us:"
        elif region == 'europe': region = "Europe :flag_eu:"
        elif region == 'india': region = "India :flag_in:"
        elif region == 'russia': region = "Russia :flag_ru:"
        elif region == 'sydney': region = "Sydney :flag_au:"
        elif region == 'hongkong': region = "Hong Kong :flag_hk:"
        elif region == 'japan': region = "Japan :flag_jp:"
        elif region == 'singapore': region = "Singapore :flag_sg:"
        elif region == 'southafrica': region = "South Africa :flag_za:"
        elif region == 'brazil': region = "Brazil :flag_br:"
        else: region = region.capitalize()

        categories = len(ctx.guild.categories)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        total_channels = text_channels + voice_channels

        humans_online = sum(member.status != discord.Status.offline and not member.bot for member in ctx.guild.members)
        humans_offline = sum(member.status == discord.Status.offline and not member.bot for member in ctx.guild.members)

        bots_online = sum(member.status != discord.Status.offline and member.bot for member in ctx.guild.members)
        bots_offline = sum(member.status == discord.Status.offline and member.bot for member in ctx.guild.members)

        total_members = len(ctx.guild.members)

        total_bots = sum(member.bot for member in ctx.guild.members)
        total_humans = sum(not member.bot for member in ctx.guild.members)

        total_online = bots_online + humans_online
        total_offline = bots_offline + humans_offline

        embed = discord.Embed(
            title = f"{ctx.guild.name} (`{ctx.guild.id}`)",
            color = self.colors.primary
        )

        embed.add_field(
            name = "**❯ Server**",
            value = f"**Owner:** {ctx.guild.owner.mention} (`{ctx.guild.owner.id}`)\n" \
                f"**Creation:** {ctx.guild.created_at.strftime('%A, %B %d %Y @ %H:%M:%S %p')}\n" \
                f"**Region:** {region}\n\n" \
                f"**Verification Level:** {verification}\n" \
                f"**Notification Level:** {notification}\n" \
                f"**Content Filter:** {contentfilter}",
            inline = False
        )

        embed.add_field(
            name = "**❯ Members**",
            value = f"{ctx.guild.member_count} total. ({total_humans} humans, {total_bots} bots)\n" \
                f"{total_online} online. ({humans_online} humans, {bots_online} bots)\n" \
                f"{(total_online / total_members * 100):.2f}% of members online. ({(humans_online / total_members * 100):.2f}% humans, {(bots_online / total_members * 100):.2f}% bots)\n" \
                f"*`{self.bot_prefix}userinfo [@user]` for more info.*",
            inline = False
        )

        embed.add_field(
            name = "**❯ Channels**",
            value = f"{categories} categories.\n" \
                f"{total_channels} channels. ({text_channels} text channels, {voice_channels} voice channels)\n" \
                f"*`{self.bot_prefix}channelinfo [#channel]` for more info.*",
            inline = False
        )


        embed.add_field(
            name = "**❯ Roles**",
            value = f"{len(ctx.guild.roles) - 1} roles.\n" \
                f"{ctx.guild.roles[-1].mention} (Top Role)\n" \
                f"*`{self.bot_prefix}roleinfo [role]` for more info.*",
            inline = False
        )

        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.command(aliases = ['whois'], usage = "[@user/id]")
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Returns information about an user (if specified) or the author."""

        user = user or ctx.author

        # Platforms the user is currently using.
        platforms = []
        if user.desktop_status != discord.Status.offline: platforms.append("Desktop")
        if user.mobile_status != discord.Status.offline: platforms.append("Mobile")
        if user.web_status != discord.Status.offline: platforms.append("Web Client")
        discord_client = f"({' | '.join(platforms)})" if platforms else ''

        statuses = {
            'online': ("Online", self.colors.online, self.emojis.online),
            'offline': ("Invisible" if user == ctx.author else "Offline", self.colors.offline, self.emojis.offline),
            'dnd': ("Do Not Disturb", self.colors.dnd, self.emojis.dnd),
            'idle': ("Idle", self.colors.idle, self.emojis.idle)
        }
        status = statuses.get(str(user.status), statuses['offline'])

        # (We loop through the user roles in reverse order so that it's displayed as in the hierarchy.)
        roles = ', '.join(i.mention for i in reversed(user.roles) if i != ctx.guild.default_role)

        user_values = []
        user_values.append(f"**Mention:** {user.mention}")
        user_values.append(f"**Status:** {status[2]} {status[0]} {discord_client}")
        if user.activity: user_values.append(f"**Activity:** {user.activity.type.name.capitalize()} {user.activity.name}")
        user_values.append(f"**Registered at:** {user.created_at.strftime('%A, %B %d %Y @ %H:%M:%S %p')}")

        server_values = []
        server_values.append(f"**Nickname:** {user.display_name}")
        server_values.append(f"**Joined At:** {user.joined_at.strftime('%A, %B %d %Y @ %H:%M:%S %p')}")
        if user.top_role != ctx.guild.default_role: server_values.append(f"**Top Role:** {user.top_role.mention}")

        embed = discord.Embed(title = f"{user} (`{user.id}`)", color = status[1])

        user_name = "**❯ User**" if not user.bot else "**❯ Bot**"

        # Tags
        if user == ctx.guild.owner: user_name += (" **(👑 Server Owner)**")
        if user.id in self.config.bot_owners: user_name += (" **[Bot Owner]**")
        if user.id in self.config.bot_vips: user_name += (" **[Bot Premium]**")

        embed.add_field(
            name = user_name,
            value = '\n'.join(user_values),
            inline = False
        )

        embed.add_field(
            name = "**❯ Server**",
            value = '\n'.join(server_values),
            inline = False
        )

        # If the user has roles, we show that else we show all the permissions they have in the guild.
        if roles: 
            embed.add_field(name = f"**❯ Roles ({len(user.roles) - 1})**", value = roles, inline = False)
        else:
            permissions = list(user.guild_permissions)
            embed.add_field(name = f"**❯ Permissions ({len(permissions)})**", value = ', '.join(formatting.casify(i[0]) for i in permissions), inline = False)

        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(InformationCog(bot))