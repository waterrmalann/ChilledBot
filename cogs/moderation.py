# Discord.
import discord
# Command Handler.
from discord.ext import commands
# Permissions / JSON Parser
from utils import permissions, default
import typing

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base = 10)
            except ValueError:
                raise commands.BadArgument(f"Invalid member id.") from None
        else:
            return m.id


class ModerationCog(commands.Cog, name = "Moderation"):
    """Server Administration and Management Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.emojis = default.get("emojis.json")
        self.colors = default.get("colors.json")
        self.bot_prefix = '.'

        # Cog Info
        self.hidden = True
        self.name = "Moderation & Management"
        self.aliases = {'mod', 'moderator', 'moderation', 'manage', 'admin'}
        self.categories = ('user tools', 'server tools')

    @commands.command(brief = 'user tools', aliases = ['banhammer'], usage = '<@user/id> (days to delete msgs) [reason]')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, user: MemberID, time_limit: typing.Optional[int] = 7, *, reason: str = None):
        """Bans an user from the server."""

        m = ctx.guild.get_member(user)

        if m is not None and await permissions.check_modcmd_perms(ctx, m): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.ban(discord.Object(id = user), reason = reason, delete_message_days = time_limit)
        except Exception as e:
            await ctx.send(f"{self.emojis.cross} **I couldn't ban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{m} [{user}]` **has been banned from the server. ({reason})**")

        #if dm:
        #    await user.send(f"You have been banned from **{ctx.guild.name}**. ({reason})")

    @commands.command(brief='user tools', aliases = ['pardon'], usage = '<user/id>')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, user: str, *, reason: str = None):
        """Unbans a banned user in the server."""

        reason = reason or "No Reason Provided"

        for ban in await ctx.guild.bans():
            if user in str(ban.user) or user == str(ban.user.id):
                user = ban.user
                break
        else:
            return await ctx.send(f"{self.emojis.cross} **I couldn't find the user in the ban list of this server.**")

        try:
            await ctx.guild.unban(discord.Object(id = user), reason = reason)
        except Exception as e:
            return await ctx.send(f"{self.emojis.cross} **I couldn't unban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{user} [{user.id}]` **has been unbanned. ({reason})**")
    
    @commands.command(brief = 'user tools', aliases =['boot'], usage = '<@user/id>')
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a member from this server."""

        if await permissions.check_modcmd_perms(ctx, member): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.kick(discord.Object(id = member.id), reason = reason)
        except Exception as e:
            await ctx.send(f"{self.emojis.cross} **I couldn't kick this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{member} [{member.id}]` **has been kicked from the server. ({reason})**")
        
def setup(bot):
    bot.add_cog(ModerationCog(bot))