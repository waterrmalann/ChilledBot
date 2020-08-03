# Discord.
import discord
# Command Handler.
from discord.ext import commands
# Permissions / JSON Parser
from utils import permissions, default, converters
import typing


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
    async def ban(self, ctx, user: converters.MemberID, time_limit: typing.Optional[int] = 7, *, reason: str = None):
        """Bans an user from the server."""

        m = ctx.guild.get_member(user)

        if m is not None and await permissions.verify_user_modcmd(ctx, m): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.ban(discord.Object(id = user), reason = reason, delete_message_days = time_limit)
        except Exception as e:
            await ctx.send(f"{self.emojis.cross} **I couldn't ban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{m} [{user}]` **has been banned from the server. ({reason})**")

        #if dm:
        #    await user.send(f"You have been banned from **{ctx.guild.name}**. ({reason})")

    @commands.command(brief = 'user tools', aliases = ['hackbanhammer'], usage = '<user id> [reason]')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def hackban(self, ctx, user_id: int, *, reason: str = None):
        """Bans an user that's not in the server."""

        if await permissions.verify_id_modcmd(ctx, user_id): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.ban(discord.Object(id = user_id), reason = reason)
        except discord.NotFound:
            return await ctx.send(f"{self.emojis.cross} **I couldn't find an user with this ID.** `[ex NotFound]`")
        except Exception as e:
            return await ctx.send(f"{self.emojis.cross} **I couldn't ban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `User w/ ID: {user_id}` **has been banned from the server. ({reason})**")
    
    @commands.command(brief = 'user tools', aliases = ['softbanhammer'], usage = '<@user/id> (days to delete messages) [reason]')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def softban(self, ctx, user: discord.User, time_limit: typing.Optional[int] = 7, *, reason: str = None):
        """Bans an user and immediately unbans them, clearing all their messages."""

        m = ctx.guild.get_member(user.id)
        if m is not None and await permissions.verify_user_modcmd(ctx, m): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.ban(user, reason = reason, delete_message_days = time_limit)
            await ctx.guild.unban(user, reason = reason)
        except Exception as e:
            await ctx.send(f"{self.emojis.cross} **I couldn't softban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{m} [{user}]` **has been softbanned from the server. ({reason})**")

    @commands.command(brief='user tools', aliases = ['pardon'], usage = '<user/id>')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, user: str, *, reason: str = None):
        """Unbans a banned user in the server."""

        reason = reason or "No Reason Provided"

        for ban in await ctx.guild.bans():
            if user in {str(ban.user), str(ban.user.name)} or user == str(ban.user.id):
                user = ban.user
                break
        else:
            return await ctx.send(f"{self.emojis.cross} **I couldn't find the user in the ban list of this server.**")

        try:
            await ctx.guild.unban(user, reason = reason)
        except Exception as e:
            return await ctx.send(f"{self.emojis.cross} **I couldn't unban this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{user} [{user.id}]` **has been unbanned. ({reason})**")
    
    @commands.command(brief = 'user tools', aliases = ['boot'], usage = '<@user/id>')
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a member from this server."""

        if await permissions.verify_user_modcmd(ctx, member): return
        reason = reason or "No Reason Provided"

        try:
            await ctx.guild.kick(discord.Object(id = member.id), reason = reason)
        except Exception as e:
            await ctx.send(f"{self.emojis.cross} **I couldn't kick this user.** `[ex {type(e).__name__}]`")
        else:
            await ctx.send(f"{self.emojis.tick} `{member} [{member.id}]` **has been kicked from the server. ({reason})**")
    
    @commands.command(brief = 'user tools', usage = '<@user/id> [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)  # Also check if bot has manage_channels / manage_roles
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        """Mute someone, prevents them from talking in the server."""

        if await permissions.verify_user_modcmd(ctx, member): return

        mute_role = discord.utils.get(ctx.guild.roles, name = "Muted")

        if not mute_role:
            return await ctx.send(f"{self.emojis.cross} **A 'Muted' role doesn't already exist. Use `.role create chilledBotMutedRole` to create one.**")

        reason = reason or "No Reason Provided"
        await member.add_roles(mute_role)

        await ctx.send(f"{self.emojis.tick} `{member} [{member.id}]` **has been muted. ({reason})**")
    
    @commands.command(brief = 'user tools', usage = '<@user/id> [reason]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """Unmute someone, allows them to talk in the server."""

        if await permissions.verify_user_modcmd(ctx, member): return  # Not sure if this is really necessary.

        mute_role = discord.utils.get(ctx.guild.roles, name = "Muted")

        if not mute_role:
            return await ctx.send(f"{self.emojis.cross} **A 'Muted' role doesn't already exist. Use `.role create chilledBotMutedRole` to create one.**")

        if not mute_role in member.roles:
            return await ctx.send(f"{self.emojis.cross} **This user is not muted.**")
        
        reason = reason or "No Reason Provided"
        await member.remove_roles(mute_role)

        await ctx.send(f"{self.emojis.tick} `{member} [{member.id}]` **has been unmuted. ({reason})**")
    
    @commands.command(brief = 'server tools', aliases = ['echo', 'repeat'], usage = '<message>')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def say(self, ctx, *, to_say: str):
        """Make the bot say something."""

        await ctx.message.delete()
        await ctx.send(to_say)
    
    @commands.command(brief = 'server tools', aliases = ['announce', 'saye'], usage = '<message>')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def embed(self, ctx, *, to_say: str):
        """Make the bot embed something."""

        embed = discord.Embed(
            description = to_say,
            color = self.colors.primary
        )

        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'server tools', aliases = ['advanced_embed'], usage = '"title" "description" "footer"')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def aembed(self, ctx, title: str, description: str = None, footer: str = None):
        """Advanced version of the embed command."""

        embed = discord.Embed(title = title, color = self.colors.primary)
        if description: embed.description = description
        if footer: embed.set_footer(text = footer)

        await ctx.message.delete()
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'server tools', aliases = ['bulkdelete', 'prune'], usage = '<limit (upto 2000)>')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def purge(self, ctx, count: int):
        """Bulk delete messages from the channel."""

        if count > 2000 or count < 1:
            return await ctx.send(f"{self.emojis.cross} **I can only delete upto 2000 messages.** `[ex PurgeLimitHit]`")
        
        await ctx.message.delete()
        await ctx.channel.purge(limit = count)

    @commands.group(brief = 'server tools', name = 'role', usage = '<create/clone/remove> [params]')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def role(self, ctx):
        """Manage server roles."""

        if not ctx.invoked_subcommand:
            raise commands.BadArgument('missing subcommand')

    # role add interactive
    # asks questions, do you want this? do you want that?
    @role.command(name = 'add', aliases = ['create', 'make'], usage = '"<name>" [hoisted (yes/no)] [allow mention (yes/no)] (hex color code) [permissions integer]')
    async def role_add(self, ctx, name: str, hoisted: bool = False, allow_mentions: bool = False, color: discord.Color = None, permissions: int = 0):
        """Create a new role."""

        color = color or discord.Color.default()

        if name == 'chilledBotMutedRole':
            return await ctx.send('not yet amigo')

        new_role = await ctx.guild.create_role(name = name, color = color, hoist = hoisted, mentionable = allow_mentions)

        await ctx.send(f"{self.emojis.tick} **Successfully created role {new_role.mention}.")
    
    @role.command(name = 'clone', aliases = ['duplicate'], usage = '<role> [new name]')
    async def role_clone(self, ctx, target_role: discord.Role, name: str = None):
        """Clones a role."""

        # to-do: check if you can clone the role beforehand.

        name = name or target_role.name
        permissions = target_role.permissions
        color = target_role.color
        hoist = target_role.hoist
        mentionable = target_role.mentionable

        new_role = await ctx.guild.create_role(name = name, color = color, hoist = hoist, mentionable = mentionable, permissions = permissions)

        await ctx.send(f"{self.emojis.tick} **Successfully duplicated {target_role.mention} with {new_role.mention}")   
    
    @role.command(name = 'delete', aliases = ['remove'], usage = '<role> [reason]')
    async def role_delete(self, ctx, target_role: discord.Role, *, reason: str = None):
        """Deletes a role from the server."""

        # to-do: check if you can delete the role beforehand
        reason = reason or "No Reason Provided"
        await target_role.delete(reason = reason)
        await ctx.send(f"{self.emojis.tick} `@{target_role.name} [{target_role.id}]` **has been deleted. ({reason})**")
        
def setup(bot):
    bot.add_cog(ModerationCog(bot))