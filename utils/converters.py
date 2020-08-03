import discord
from discord.ext import commands
import re
import base64

class Color(commands.Converter):
    """Returns the color integer from hex codes accepting nuances."""

    async def convert(self, ctx, col):
        if len(col) == 8 and col.startswith('0x'):  # 0xFF0000
            col = int(col, 16)
        elif len(col) == 6 or col.startswith('#'):
            if col.startswith('#'):
                col = int(col[1:], 16)  # #FF0000
            else:
                col = int(col, 16)  # FF0000
        elif col.isdigit():
            col = int(col)  # 16711680
        else:
            raise commands.BadArgument('invalid color')
        return col

class MemberID(commands.Converter):
    """Returns the id of an user."""

    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base = 10)
            except ValueError:
                raise commands.BadArgument("invalid member id") from None
        else:
            return m.id

# bad idea
class AdvancedMemberOrUser(commands.Converter):
    """An advanced converter that attempts to convert to member, user through normal means and finally fetching."""

    async def convert(self, ctx, argument):
        # Attempt to convert the argument to a discord member object.
        try:
            member = await commands.MemberConverter().convert(ctx, argument)
            return member
        except commands.BadArgument:
            # If it fails, then attempt to convert it to a discord user object. (from global cache)
            try:
                user = await commands.UserConverter().convert(ctx, argument)
                return user
            except commands.BadArgument:
                # If that fails, attempt to convert it to a discord user object. (with an actual request to discord)

                # See if the argument is a digit, then it could be the user id.
                user_id = int(argument) if argument.isdigit() else 0

                # Check if it's an user token.
                if re.match('[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}', argument):
                    data = argument.split('.')[0].encode('utf8')
                    data = base64.b64decode(data)
                    if not data.isdigit(): raise commands.BadArgument("invalid user token")  # we've been tricked
                    user_id = int(data)
                
                # If we finally have an integer (possibly an user id) after all that.
                if user_id:
                    # Attempt getting the user from the global cache and request for them if it fails.
                    try:
                        user = ctx.bot.get_user(user_id) or await ctx.bot.fetch_user(user_id)
                        return user
                    except discord.NotFound:
                        raise commands.BadArgument('invalid user id')
                else:
                    raise commands.BadArgument('invalid user')