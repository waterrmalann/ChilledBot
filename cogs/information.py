# To-Do:
# >> Message Info
# >> Role Info
# >> Channel Info

# Discord.
import discord
# Command Handler.
from discord.ext import commands
# DateTime Parser.
from datetime import datetime
from humanize import naturaldelta
# JSON Parser & Text Formatter.
from utils import default, formatting
import typing


class InformationCog(commands.Cog, name = "Information"):
    """Information-Related Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.emojis = default.get("emojis.json")
        self.bot_prefix = '.'

        # Cog Info
        self.hidden = False
        self.name = "Information"
        self.aliases = {'info', 'information'}
        self.categories = ('user', 'server', 'discord')
        
    
    @commands.command(brief = 'user', aliases = ['pfp', 'pic'], usage = "[@user/id]")
    async def avatar(self, ctx, user: discord.Member = None):
        """Return the avatar of an user (if specified) or the author."""

        # Return the author if an user is not specified.
        user = user or ctx.author

        # Get the link to the user's avatar.
        avatar_urls = [str(user.avatar_url_as(size = sz)) for sz in (128, 256, 512, 1024, 2048)]
        sizes = f"**[[128]({avatar_urls[0]})] | [[256]({avatar_urls[1]})] | [512] | [[1024]({avatar_urls[3]})] | [[2048]({avatar_urls[4]})]**"

        embed = discord.Embed(title = str(user), description = sizes, url = avatar_urls[2], color = self.colors.primary)
        embed.set_image(url = avatar_urls[2])
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'discord', aliases = ['e', 'em'], usage = '<emoji>')
    async def emoji(self, ctx, emoji: discord.Emoji):
        """Returns a larger version of the specified emoji."""

        emoji_url = str(emoji.url)
        embed = discord.Embed(title = f":{emoji.name}:", url = emoji_url, color = self.colors.primary)
        embed.set_image(url = emoji_url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(brief = 'server')
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Detailed information about the current guild the bot is in."""

        # The user verification level of the server.
        verification = str(ctx.guild.verification_level)
        if verification == 'none': verification = "[0] None"
        elif verification == 'low': verification = "[1] Low"
        elif verification == 'medium': verification = "[2] Medium"
        elif verification == 'high': verification = "[3] (╯°□°）╯︵ ┻━┻ (High)"
        else: verification = "[4] ┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻ (Extreme)"

        # The guild's default notification level. We format the text properly.
        notification = ctx.guild.default_notifications
        if notification == 'all_messages': notification = "All Messages"
        else: notification = "Only Mentions"

        # The guild's content filter status.
        # (Content filtering algorithms employed by Discord to identify and delete explicit content.)
        contentfilter = ctx.guild.explicit_content_filter
        if contentfilter == 'disabled': contentfilter = "Disabled"
        elif contentfilter == 'no_role': contentfilter = "Enabled for members with no role"
        else: contentfilter = "Enabled for all members"

        # The server's (voice/host?) region with their respective country flags.
        region = str(ctx.guild.region)
        if region in {'us-central', 'us-east', 'us-south', 'us-west'}:region =  f"US {region[3:].capitalize()} :flag_us:"
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

        total_emojis = len(ctx.guild.emojis)
        animated_emojis = sum(1 for emoji in ctx.guild.emojis if emoji.animated)
        static_emojis = total_emojis - animated_emojis
        
        server_values = []  # ❯ Server
        server_values.append(f"**Owner:** {ctx.guild.owner.mention} (`{ctx.guild.owner.id}`)")
        server_values.append(f"**Creation:** {default.datefr(ctx.guild.created_at)}")
        server_values.append(f"**Region:** {region}\n")
        server_values.append(f"**Verification Level:** {verification}")
        server_values.append(f"**Notification Level:** {notification}")
        server_values.append(f"**Content Filter:** {contentfilter}")
        server_values.append(f"**2FA (for Staff):** {'Enabled' if ctx.guild.mfa_level else 'Disabled'}")
        if total_emojis: server_values.append(f"**Custom Emojis:** {len(ctx.guild.emojis)} ({static_emojis} static, {animated_emojis} animated)")
        if ctx.guild.premium_tier: server_values.append(f"**Premium Tier:** {ctx.guild.premium_tier} ({ctx.guild.premium_subscription_count} boosts)")

        member_values = []  # ❯ Members
        member_values.append(f"{ctx.guild.member_count} total ({total_humans} humans, {total_bots} bots)")
        member_values.append(f"{(total_online / total_members * 100):.1f}% of members online ({(humans_online / total_members * 100):.1f}% humans, {(bots_online / total_members * 100):.1f}% bots)")
        member_values.append(f"*`{self.bot_prefix}userinfo [@user]` for more info.*")

        channel_values = []  # ❯ Channels
        channel_values.append(f"{categories} categories")
        channel_values.append(f"{total_channels} channels ({text_channels} text, {voice_channels} voice)")
        channel_values.append(f"*`{self.bot_prefix}channelinfo [#channel]` for more info.*")

        role_values = []  # ❯ Roles
        role_values.append(f"{len(ctx.guild.roles) - 1} roles")
        role_values.append(f"{ctx.guild.roles[-1].mention} (Top Role)")
        role_values.append(f"*`{self.bot_prefix}roleinfo [role]` for more info.*")

        embed = discord.Embed(
            title = f"{ctx.guild.name} (`{ctx.guild.id}`)",
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )

        embed.add_field(
            name = "❯ Server",
            value = '\n'.join(server_values),
            inline = False
        )
        
        embed.add_field(
            name = "❯ Members",
            value = '\n'.join(member_values),
            inline = False
        )

        embed.add_field(
            name = "❯ Channels",
            value = '\n'.join(channel_values),
            inline = False
        )

        embed.add_field(
            name = "❯ Roles",
            value = '\n'.join(role_values),
            inline = False
        )

        if ctx.guild.features:
            features = ', '.join(formatting.casify(i) for i in ctx.guild.features)
            embed.add_field(
                name = "❯ Features",
                value = features,
                inline = False
            )

        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    @commands.command(brief = 'server')
    @commands.guild_only()
    async def channelinfo(self, ctx, *, channel: typing.Union[discord.TextChannel, discord.VoiceChannel] = None):
        """Returns information about the specified or the current channel."""

        channel = channel or ctx.channel
        voice_channel = type(channel) is discord.VoiceChannel
        if not voice_channel and ctx.author not in channel.members:
            return await ctx.send(f"{self.emojis.cross} **You aren't supposed to see this channel!**")

        # permissions_synced
        channel_values = []
        channel_values.append(f"**Mention:** {channel.mention}")
        if channel.category: channel_values.append(f"**Category:** {channel.category.name} (`{channel.category.id}`)")
        channel_values.append(f"**Created at:** {default.datefr(channel.created_at)}")
        if voice_channel and channel.user_limit:
            channel_values.append(f"**Members:** {len(channel.members)}/{channel.user_limit}")
        else:
            channel_values.append(f"**Members:** {len(channel.members)}")
        if voice_channel:
            channel_values.append(f"**Bitrate:** {round(channel.bitrate / 1000)}kbps")
        else:
            channel_values.append(f"**Slowmode:** {naturaldelta(channel.slowmode_delay) if channel.slowmode_delay > 0 else 'No Slowmode.'}")
        #channel_values.append(f"**Position:** {default.int_suffix(channel.position + 1)}")
        
        embed = discord.Embed(
            title = f"#{channel.name} (`{channel.id}`)" if not voice_channel else f"\🔊 {channel.name} (`{channel.id}`)",
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )

        embed.add_field(
            name = f"❯ Text Channel {'- ⚠️ NSFW' if channel.nsfw else ''}" if not voice_channel else "❯ Voice Channel",
            value = '\n'.join(channel_values),
            inline = False
        )

        if not voice_channel and channel.topic:
            embed.add_field(name = "❯ Topic", value = channel.topic, inline = False)
        
        if voice_channel: thumb = "https://cdn.discordapp.com/attachments/726353729842053171/736108059264548886/channel_speaker.png"
        else: thumb = "https://cdn.discordapp.com/attachments/726353729842053171/736108052750663761/channel_hashtag.png"
        embed.set_thumbnail(url = thumb)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)


    @commands.command(brief = 'user', aliases = ['whois'], usage = "[@user/id]", description = "this crazy mf can go 0-60 in 6 seconds!")
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Returns information about an user (if specified) or the author."""

        # Return the author if an user is not specified.
        user = user or ctx.author

        platforms = [] # Platforms the user is currently online on.
        if user.desktop_status != discord.Status.offline: platforms.append("Desktop")
        if user.mobile_status != discord.Status.offline: platforms.append("Mobile")
        if user.web_status != discord.Status.offline: platforms.append("Web Client")
        discord_client = f"({' | '.join(platforms)})" if platforms else ''

        statuses = {
            # Status: (Name, Color, Emoji)
            # The name is to show the name of the status.
            # The color is to color the embed line based on their status.
            # The emoji is to show alongside the name.
            'online': ("Online", self.colors.online, self.emojis.online),
            'offline': ("Invisible" if user == ctx.author or user.voice else "Offline", self.colors.offline, self.emojis.offline),
            'dnd': ("Do Not Disturb", self.colors.dnd, self.emojis.dnd),
            'idle': ("Idle", self.colors.idle, self.emojis.idle)
        }

        # Get the user's current status alongside it's color and emoji.
        # If not found (ehrm?!) then it will return the offline status.
        status = statuses.get(str(user.status), statuses['offline'])

        # (We loop through the user roles in reverse order so that it's displayed as in the hierarchy.)
        roles = ', '.join(i.mention for i in reversed(user.roles) if i != ctx.guild.default_role)

        user_values = []  # ❯ Bot / ❯ User / ❯ Discord Staff
        if user.id in self.config.bot_owners: user_values.append(f"**I created this bot.**")
        if user.id in self.config.bot_vips and user.id not in self.config.bot_owners: user_values.append(f"**I support this bot.**")
        user_values.append(f"**Mention:** {user.mention}")
        user_values.append(f"**Status:** {status[2]} {status[0]} {discord_client}")
        if user.activity: user_values.append(f"**Activity:** {user.activity.type.name.capitalize()} {user.activity.name}")
        user_values.append(f"**Registered at:** {default.datefr(user.created_at)}")

        server_values = []  # ❯ Server️
        if user == ctx.guild.owner: server_values.append(f"**\👑 Server Owner**")
        elif user.guild_permissions.administrator: server_values.append(f"**\🛠️ Server Administrator**")
        elif user.guild_permissions.ban_members: server_values.append("**️️\🛡️ Server Staff**")
        #else: server_values.append("**Member**")
        server_values.append(f"**Nickname:** {user.display_name}")
        server_values.append(f"**Joined At:** {default.datefr(user.joined_at)}")
        if user.top_role != ctx.guild.default_role: server_values.append(f"**Top Role:** {user.top_role.mention}")

        embed = discord.Embed(title = f"{user} (`{user.id}`)", color = status[1], timestamp = datetime.utcnow())

        embed.add_field(
            name = "❯ Bot" if user.bot else "❯ Discord Staff" if user.system else "❯ User",
            value = '\n'.join(user_values),
            inline = False
        )

        embed.add_field(
            name = "❯ Server",
            value = '\n'.join(server_values),
            inline = False
        )

        if roles:
            # If the user has roles, we show that.
            embed.add_field(name = f"❯ Roles ({len(user.roles) - 1})", value = roles, inline = False)
        else:
            # else we show all the permissions they have in the guild.
            permissions = list(user.guild_permissions)
            embed.add_field(name = f"❯ Permissions ({len(permissions)})", value = ', '.join(formatting.casify(i[0]) for i in permissions), inline = False)

        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command(brief = 'server', usage = "[max uses] [temporary: yes/no]") # [max age (seconds)]
    @commands.guild_only()
    @commands.bot_has_permissions(create_instant_invite = True)
    @commands.has_permissions(create_instant_invite = True)
    async def createinvite(self, ctx, max_uses: typing.Optional[int] = 0, temporary: bool = False):
        """Creates an invite link for the current server."""

        invite = await ctx.guild.text_channels[0].create_invite(
            max_uses = max_uses,
            max_age = 0,
            temporary = temporary
        )
        await ctx.send(f"**<{invite}>**")

    #role = discord.utils.get(ctx.guild.roles, name="Role") if role in ctx.author.roles:


def setup(bot):
    bot.add_cog(InformationCog(bot))