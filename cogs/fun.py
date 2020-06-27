# Discord.
import discord
# Command Handler.
from discord.ext import commands
# Asynchronous Package & Requests.
import asyncio
import aiohttp
# Optional Command Parameters.
import typing
# Randomization.
import random
# Parsing HTML Special Characters (for Trivia)
import html
# DateTime Parser.
from datetime import datetime
# JSON Parser.
from utils import default


class FunCog(commands.Cog):
    """Entertainment & Miscellaneous Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.emojis = default.get("emojis.json")
        self.bot_prefix = '.'
        self.categories = ['random', 'animals', 'reddit', 'text', 'misc']

    #Usage: .{command.name} {command.usage}
    #embed.set_footer(text = command.help)


    @commands.command(name = '8ball', brief = 'random', aliases = ['eightball', 'eight-ball', '8-ball'], usage = '<question>')
    async def eightball(self, ctx, *, question: str):
        """Ask the magic 8-ball your doubts."""

        fortunes = (
            # Positive Responses
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            # Neutral Responses
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            # Negative Responses
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        )

        embed = discord.Embed(color = self.colors.primary, timestamp = datetime.utcnow())
        embed.set_author(name='The Magic 8-Ball', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/8-Ball_Pool.svg/240px-8-Ball_Pool.svg.png')
        embed.set_footer(text = f"Asked by {ctx.author}", icon_url = ctx.author.avatar_url)
        embed.add_field(name = question, value = f"**Answer:** {random.choice(fortunes)}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'random', aliases = ['flipcoin', 'tosscoin', 'coinflip'])
    async def coin(self, ctx):
        """Toss a coin."""

        choices = ('heads', 'tails')

        embed = discord.Embed(
            description = f"You flipped a coin and it's **{random.choice(choices)}**",
            color = self.colors.primary
        )
        embed.set_footer(text=f"Tossed by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(brief = 'random', aliases = ['dice'], usage = '[number]')
    async def roll(self, ctx, number: typing.Optional[int] = 6):
        """Roll a dice or a number."""

        if number < 2: number = 6

        if number == 6:
            embed = discord.Embed(
                description = f"🎲 You rolled a dice and got **{random.randint(1, 6)}**",
                color = self.colors.primary
            )
            embed.set_footer(text = f"Rolled by {ctx.author}", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                description = f"🎲 You rolled a number and got **{random.randint(1, number)}**",
                color = self.colors.primary
            )
            embed.set_footer(text = f"Rolled by {ctx.author}", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
    
    @commands.command(brief = 'random', aliases = ['sps', 'stonepaperscissors', 'rockpaperscissors'], usage = '<rock/paper/scissors>')
    async def rps(self, ctx, choice: str):
        """Play rock, paper, scissors."""

        choices = ('rock', 'paper', 'scissors')

        choice = choice.lower()
        if choice == 'stone': choice = choice.replace('stone', 'rock')
        if choice not in choices: raise commands.BadArgument("Please pick a valid choice.")

        choose = random.choice(choices)

        if choose == choice: await ctx.send(f"I chose {choose}, It's a tie")
        elif choose == "rock" and choice == "scissors": await ctx.send(f"I chose {choose}, You lose!")
        elif choose == "paper" and choice == "rock": await ctx.send(f"I chose {choose}, You lose!")
        elif choose == "scissors" and choice == "paper": await ctx.send(f"I chose {choose}, You lose!")
        else: await ctx.send(f"I chose {choose}, You win!")


    @commands.command(brief = 'random', aliases = ['choice', 'choose'], usage = '<item> <item> [items...]')
    async def choices(self, ctx, *options):
        """Randomly pick an item from a list of items."""

        if not options: return await ctx.send(f"**Syntax:** {ctx.command.name} {ctx.command.usage}")
        await ctx.send(f"I pick {random.choice(options)}")

    @commands.command(brief = 'text', usage = '<text>')
    async def clap(self, ctx, *, text: str):
        """Clappify text."""

        await ctx.send(text.replace(' ', '👏'))

    @commands.command(brief = 'text', usage = '<text>')
    async def reverse(self, ctx, *, text: str):
        """Reverse given text."""

        await ctx.send(text[::-1])
    
    # Why did I make this?
    @commands.command(brief = 'text', usage = "<text>")
    async def emojify(self, ctx, *, text: str):
        """Convert text to block letters."""

        numbers = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}

        emojified = []
        for i in text:
            if i.lower() in 'abcdefghijklmnopqrstuvwxyz':
                emojified.append(f":regional_indicator_{i.lower()}:")
            elif i.isdigit():
                emojified.append(f":{numbers.get(int(i), ':zero:')}:")
            else:
                emojified.append(' ')

        await ctx.send(''.join(emojified))

    @commands.command(brief = 'text', usage = '<word>')
    async def scramble(self, ctx, *, word: str):
        """Scramble given word."""

        letters = list(word)
        random.shuffle(letters)
        await ctx.send(''.join(letters))

    @commands.command(brief = 'misc', aliases = ['hug'], usage = "[@user/id]")
    async def notice(self, ctx, user: discord.Member = None):
        """Notice me senpai!"""

        # Return the author if an user is not specified.
        user = user or ctx.author

        hugs = (
            "`＼(^o^)／`", "`d=(´▽｀)=b`", "`⊂((・▽・))⊃`"
            "`⊂( ◜◒◝ )⊃`", "`⊂（♡⌂♡）⊃`", r"`\(･◡･)/`",
            "`(づ｡◕‿‿◕｡)づ`", "`༼ つ ◕‿◕ ༽つ`", "`(づ￣ ³￣)づ`",
            "`(⊃｡•́‿•̀｡)⊃`",  "`ʕっ•ᴥ•ʔっ`", "`(o´･_･)っ`",
            "`(⊃ • ʖ̫ • )⊃`", "`(つ≧▽≦)つ`", "`(つ✧ω✧)つ`",
            "`(っ.❛ ᴗ ❛.)っ`", "`～(つˆДˆ)つ｡☆`", "`⊂(•‿•⊂ )*.✧`",
            "`⊂(´･◡･⊂ )∘˚˳°`", "`⊂(･ω･*⊂)`", "`⊂(・﹏・⊂)`",
            "`⊂(・▽・⊂)`", "`⊂(◉‿◉)つ`", "`o((*^▽^*))o`",
            "`╰(*´︶`*)╯`", "`╰(＾3＾)╯`", "`╰(⸝⸝⸝´꒳`⸝⸝⸝)╯`"
        )

        await ctx.send(f"{user.mention}, `{random.choice(hugs)}`")
    
    @commands.command(brief = 'animals', aliases = ["feline", "tom", "mouser", "pussy", "meow"])
    async def cat(self, ctx, num: typing.Optional[int] = 0, fact : bool = False):
        """Gives you a cat pic."""

        choices = ("Meow... 🐱", "Meow 😻", "Here's a feline for you. 🐈")
        choice = random.choice(choices)

        if num > 2 or num < 1: num = random.randint(1, 2)  # 50%/50%

        if num == 1:
            url = "http://shibe.online/api/cats"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data[0]
        else:
            url = "https://some-random-api.ml/img/cat"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)

        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:  # We'll do 30% chance to get a cat fact.
            url = "https://catfact.ninja/fact"
            async with self.session.get(url) as r:
                data = await r.json()
                cat_fact = data['fact']
            await ctx.send(f"**Did you know?** {cat_fact}")

    @commands.command(brief = 'animals', aliases = ["pupper", "woof", "doggo", "bork", "canine"])
    async def dog(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Gives you a dog pic."""

        choices = ("Woof 🐶", "Bork Bork :service_dog:", "Here's a canine for you. 🐕", "Arf! 🐶")
        choice = random.choice(choices)

        if num > 3 or num < 1: num = random.randint(1, 3)  # 33%/33%/33% Chance

        if num == 1:
            url = "https://dog.ceo/api/breeds/image/random"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["message"]
        elif num == 2:
            url = "https://some-random-api.ml/img/dog"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["link"]
        else:
            url = "https://random.dog/woof.json"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["url"]
        
        if image.endswith(('.webm', '.mp4')):
            # Sending videos as a raw message because apparently discord embeds don't support videos.
            await ctx.send(image)
        else:
            embed = discord.Embed(title = choice, color = self.colors.primary)
            embed.set_image(url = image)
            embed.set_footer(text = url)
            await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/dog"
            async with self.session.get(url) as r:
                data = await r.json()
                fact = data['fact']
            await ctx.send(f"**Did you know?** {fact}")
            #https://dog-api.kinduff.com/api/facts  data["facts"][0]
    
    @commands.command(brief = 'animals', aliases = ["birb", "ave", "birdie"])
    async def bird(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Gives you a bird pic."""

        choices = ("🐦 Here's your birb.", "Here's a birdie for you. 🐦", "🐦 Here's a birdie.")
        choice = random.choice(choices)

        if num > 2 or num < 1: num = random.randint(1, 2)  # 50%/50% Chance

        if num == 1:
            url = "http://shibe.online/api/birds"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data[0]
        else:
            url = "https://some-random-api.ml/img/birb"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/bird"
            async with self.session.get(url) as r:
                data = await r.json()
                fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(brief = 'animals', aliases = ["foxie", "arf"])
    async def fox(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Gives you a fox pic."""

        choices = ("🦊 Here's a fox.", "Here's a fox for you. 🦊", "🦊 Here's your fox.")
        choice = random.choice(choices)


        if num > 2 or num < 1: num = random.randint(1, 2)  # 50%/50% Chance

        if num == 1:
            url = "https://randomfox.ca/floof/"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["image"]
        else:
            url = "https://some-random-api.ml/img/fox"
            async with self.session.get(url) as r:
                data = await r.json()
                image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/fox"
            async with self.session.get(url) as r:
                data = await r.json()
                fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
            # Random Fox Fact: Did You Know? 
    
    @commands.command(brief = 'animals', aliases = ["achoo"])
    async def panda(self, ctx, fact : bool = False):
        """Gives you a panda pic."""

        choices = ("🐼 Here's a panda.", "Here's a panda for you. 🐼", "🐼 Here's your panda!", "Here's your panda... 🐼")
        choice = random.choice(choices)

        url = "https://some-random-api.ml/img/panda"
        async with self.session.get(url) as r:
            data = await r.json()
            image = data["link"]
        
        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/panda"
            async with self.session.get(url) as r:
                data = await r.json()
                fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(brief = 'animals')
    async def koala(self, ctx, fact : bool = False):
        """Gives you a koala pic."""

        choices = ("🐨 Here's a koala.", "Here's a cute koala for you. 🐨", "🐨 Here's your koala!", "Here's your koala... 🐨")
        choice = random.choice(choices)

        url = "https://some-random-api.ml/img/koala"
        async with self.session.get(url) as r:
            data = await r.json()
            image = data["link"]

        embed = discord.Embed(title = choice, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = url)
        await ctx.send(embed = embed)

        if fact or random.randint(1, 10) < 4:
            url = "https://some-random-api.ml/facts/koala"
            async with self.session.get(url) as r:
                data = await r.json()
                fact = data["fact"]
            await ctx.send(f"**Did you know?** {fact}")
    
    @commands.command(name = "anime", brief = 'misc')
    async def uwu(self, ctx):
        """Gives you an anime girl pic."""

        url = "http://api.cutegirls.moe/json"
        async with self.session.get(url) as r:
            data = await r.json()
            image = data["data"]["image"]
            title = data["data"]["title"]
            link = data["data"]["link"]
            #author = data["data"]["author"]
            sub = data["data"]["sub"]
        url = "http://api.cutegirls.moe"

        embed = discord.Embed(title = title, color = self.colors.primary, url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"{url} • r/{sub}")
        await ctx.send(embed = embed)
    
    @commands.command(name = "quote", brief = 'misc')
    async def quote(self, ctx):
        """Gives you a quote."""

        url = "http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=en"
        async with self.session.get(url) as r:
            data = await r.json()
            quote_text = data['quoteText']
            quote_author = data['quoteAuthor'] or "Anonymous"
            quote_link = data['quoteLink']
        url = "http://api.forismatic.com/"

        embed = discord.Embed(
            color = self.colors.primary,
            description = f'*"{quote_text}"*\n**~ {quote_author}**'
        )
        embed.set_author(
            name = "Here's a quote...",
            url = quote_link,
            icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Cquote2_black.svg/1200px-Cquote2_black.svg.png"
        )
        embed.set_footer(text = url)
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'reddit', aliases = ['memes'], usage = '[memes/dankmemes/me_irl]')
    async def meme(self, ctx, subreddit: str = 'any', sorting: str = 'any'):
        """Gives you a meme."""

        meme_subreddits = ('r/memes', 'r/dankmemes', 'r/me_irl')
        sorts = ('new', 'hot')

        subreddit = subreddit.lower().strip()
        sorting = sorting.lower().strip()
        if not subreddit.startswith('r/'): subreddit = f"r/{subreddit}"
        if subreddit not in meme_subreddits: subreddit = random.choice(meme_subreddits)
        if sorting not in sorts: sorting = random.choice(sorts)

        url = f"https://www.reddit.com/{subreddit}/{sorting}.json?sort=hot"

        allowed_formats = ('.jpg', '.png', '.jpeg') #, '.gif', '.gifv'
        async with self.session.get(url) as r:
            post = await r.json()
            posts = [post for post in post["data"]["children"] if post["data"]["url"].endswith(allowed_formats)]
            post = posts[random.randint(0, len(posts) - 1)]["data"]

            title = post["title"]
            image = post["url"]
            content = html.unescape(post["selftext"])
            nsfw = post["over_18"]
            upvotes = post["score"]
            comments = post["num_comments"]
            author = post["author"]
            link = f"https://www.reddit.com{post['permalink']}"
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        if content: embed.description = content
        embed.set_author(name = f"u/{author}", url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"{subreddit}/{sorting} • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'reddit', aliases = ['wholesomememes', 'wholesome_meme', 'wholesomememe', 'wmeme'])
    async def wholesome(self, ctx, sorting: str = 'any'):
        """Gives you a wholesome meme."""

        sorts = ('new', 'hot')
        sorting = sorting.lower().strip()
        if sorting not in sorts: sorting = random.choice(sorts)

        url = f"https://www.reddit.com/r/wholesomememes/{sorting}.json?sort=hot"
        
        allowed_formats = ('.jpg', '.png', '.jpeg') #, '.gif', '.gifv'
        async with self.session.get(url) as r:
            post = await r.json()
            posts = [post for post in post["data"]["children"] if post["data"]["url"].endswith(allowed_formats)]
            post = posts[random.randint(0, len(posts) - 1)]["data"]

            title = post["title"]
            image = post["url"]
            content = html.unescape(post["selftext"])
            nsfw = post["over_18"]
            upvotes = post["score"]
            comments = post["num_comments"]
            author = post["author"]
            link = f"https://www.reddit.com{post['permalink']}"
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        if content: embed.description = content
        embed.set_author(name = f"u/{author}", url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/wholesomememes/{sorting} • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'reddit', aliases = ['discordmemes', 'discordirl', 'discord_irl'])
    async def discordmeme(self, ctx, sorting: str = 'any'):
        """Gives you a discord meme."""

        sorts = ('new', 'hot')
        sorting = sorting.lower().strip()
        if sorting not in sorts: sorting = random.choice(sorts)

        url = f"https://www.reddit.com/r/discord_irl/{sorting}.json?sort=hot"

        allowed_formats = ('.jpg', '.png', '.jpeg') #, '.gif', '.gifv'
        async with self.session.get(url) as r:
            post = await r.json()
            posts = [post for post in post["data"]["children"] if post["data"]["url"].endswith(allowed_formats)]
            post = posts[random.randint(0, len(posts) - 1)]["data"]

            title = post["title"]
            image = post["url"]
            content = html.unescape(post["selftext"])
            nsfw = post["over_18"]
            upvotes = post["score"]
            comments = post["num_comments"]
            author = post["author"]
            link = f"https://www.reddit.com{post['permalink']}"
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        if content: embed.description = content
        embed.set_author(name = f"u/{author}", url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/discord_irl • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'reddit', aliases = ['surreal', 'surrealmemes'])
    async def surrealmeme(self, ctx, sorting: str = 'any'):
        """Gives you a surreal meme."""

        sorts = ('new', 'hot')
        sorting = sorting.lower().strip()
        if sorting not in sorts: sorting = random.choice(sorts)

        url = f"https://www.reddit.com/r/surrealmemes/{sorting}.json?sort=hot"

        allowed_formats = ('.jpg', '.png', '.jpeg') #, '.gif', '.gifv'
        async with self.session.get(url) as r:
            post = await r.json()
            posts = [post for post in post["data"]["children"] if post["data"]["url"].endswith(allowed_formats)]
            post = posts[random.randint(0, len(posts) - 1)]["data"]

            title = post["title"]
            image = post["url"]
            content = html.unescape(post["selftext"])
            nsfw = post["over_18"]
            upvotes = post["score"]
            comments = post["num_comments"]
            author = post["author"]
            link = f"https://www.reddit.com{post['permalink']}"
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        if content: embed.description = content
        embed.set_author(name = f"u/{author}", url = link)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/surrealmemes/{sorting} • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'reddit', aliases = ['todayilearned'])
    async def til(self, ctx, sorting: str = 'any'):
        """You learn something new everyday!"""

        sorts = ('new', 'hot')
        sorting = sorting.lower().strip()
        if sorting not in sorts: sorting = random.choice(sorts)

        url = f"https://www.reddit.com/r/todayilearned/{sorting}.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']) - 1)
            post = post["data"]["children"][rand]["data"]
            
            title = post["title"]
            url = post["url"]
            content = post["selftext"]
            upvotes = post["score"]
            comments = post["num_comments"]
            author = post["author"]
            link = f'https://www.reddit.com{post["permalink"]}'

        embed = discord.Embed(color = self.colors.primary)
        if len(title) < 256:
            embed.title = title
            embed.url = link
            embed.description = f"[Source]({url})"
        else:
            embed.description = f"**[{title}]({link})**\n\n[Source]({url})"

        embed.set_author(name = f"u/{author}")
        embed.set_footer(text = f"r/todayilearned/{sorting} • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(brief = 'reddit', aliases = ['jokes'])
    async def joke(self, ctx):
        """Gives you a joke."""

        url = "https://www.reddit.com/r/Jokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']) - 1)
            post = post["data"]["children"][rand]["data"]
            title = post["title"]
            content = html.unescape(post["selftext"])
            upvotes = post["score"]
            comments = post["num_comments"]
            link = f'https://www.reddit.com{post["permalink"]}'

        embed = discord.Embed(
            title = title,
            url = link,
            description = content,
            color = self.colors.primary
        )
        embed.set_footer(text = f"r/Jokes • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'reddit', aliases = ['antijokes'])
    async def antijoke(self, ctx):
        """Gives you an anti-joke."""

        url = "https://www.reddit.com/r/AntiJokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']) - 1)
            post = post["data"]["children"][rand]["data"]
            title = post["title"]
            content = html.unescape(post["selftext"])
            upvotes = post["score"]
            comments = post["num_comments"]
            link = f'https://www.reddit.com{post["permalink"]}'

        embed = discord.Embed(
            title = title,
            url = link,
            description = content,
            color = self.colors.primary
        )
        embed.set_footer(text = f"r/AntiJokes • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'reddit', aliases = ['antiantijokes'])
    async def antiantijoke(self, ctx):
        """Gives you an anti-anti-joke."""

        url = "https://www.reddit.com/r/AntiAntiJokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']) - 1)
            post = post["data"]["children"][rand]["data"]
            title = post["title"]
            content = html.unescape(post["selftext"])
            upvotes = post["score"]
            comments = post["num_comments"]
            link = f'https://www.reddit.com{post["permalink"]}'

        embed = discord.Embed(
            title = title,
            url = link,
            description = content,
            color = self.colors.primary
        )
        embed.set_footer(text = f"r/AntiAntiJokes • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'reddit', usage = '[r/subreddit]')
    async def reddit(self, ctx, subreddit: str = 'r/all', sort_by: str = 'hot'):
        """Fetches content from a specified subreddit."""

        subreddit = subreddit.strip()
        if not subreddit.startswith('r/'):
            subreddit = 'r/' + subreddit
        
        url = f"https://www.reddit.com/{subreddit}/new.json?sort={sort_by}"

        #async with self.session.get(url) as r:
        #    post = await r.json()
        #    rand = random.randint(0, len(post['data']['children']))
        #    post = post["data"]["children"][rand]["data"]
        #    title = post["title"]
        #    image = post["url"]
        #    content = post["selftext"]
        #    link = "https://www.reddit.com" + post["permalink"]
        #    nsfw = post["over_18"]

        # Replace with "allowed_formats = ('.jpg', '.png', '.jpeg', '.gif') and more you could find."
        videos = ('https://v.redd', 'https://youtu', 'https://www.youtu', 'https://www.twitch', 'https://twitch')


        async with self.session.get(url) as r:
            post = await r.json()
            print(len(post["data"]["children"]))
            posts = [post for post in post["data"]["children"] if not post["data"]["url"].startswith(videos)]
            post = posts[random.randint(0, len(posts) - 1)]["data"]
            print(len(posts))

            title = post["title"]
            image = post["url"]
            content = post["selftext"]
            nsfw = post["over_18"]
            upvotes = post["score"]
            comments = post["num_comments"]
            link = f"https://www.reddit.com{post['permalink']}"

        print()
        print(f"Title: {title}")
        print(f"Image: {image}")
        print(f"Content: {content}")
        print(f"NSFW: {nsfw}")
        
        if nsfw and not ctx.channel.nsfw:
            return await ctx.send("⚠️ This post contains NSFW content! It cannot be previewed here.")
            
        embed = discord.Embed(title = title, url = link, description = content, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = f"{subreddit} • ⬆️ {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
        
    @commands.command(brief = 'misc', usage = "[category] [difficulty] [type]")
    async def trivia(self, ctx, triviacategory : typing.Union[str, int] = 'any', triviadifficulty : str = 'any', triviatype : str = 'any'):
        """Gives you a trivia question."""

        url = "https://opentdb.com/api.php?amount=1"

        if isinstance(triviacategory, str): triviacategory = triviacategory.strip().lower()
        triviadifficulty = triviadifficulty.strip().lower()
        triviatype = triviatype.strip().lower()

        if triviacategory == 'categories':

            trivia_categories = {
                9: "GK", 10: "Entertainment: Books",
                11: "Entertainment: Film", 12: "Entertainment: Music",
                13: "Entertainment: Musicals & Theatres", 14: "Entertainment: Television",
                15: "Entertainment: Video-Games", 16: "Entertainment: Board Games",
                17: "Science & Nature", 18: "Science: Computers",
                19: "Science: Mathematics", 20: "Mythology",
                21: "Sports", 22: "Geography",
                23: "History", 24: "Politics",
                25: "Art", 26: "Celebrities",
                27: "Animals", 28: "Vehicles",
                29: "Entertainment: Comics", 30: "Science: Gadgets",
                31: "Entertainment: Japanese Anime & Manga", 32: "Entertainment: Cartoon & Animations"
            }

            embed = discord.Embed(
                title = "Trivia Categories",
                description = '\n'.join(f"{k}. {v}" for k, v in trivia_categories.items()),
                color = self.colors.primary
            )
            await ctx.send(embed = embed)
            return
        if triviacategory == 'difficulties':

            embed = discord.Embed(
                title = "Trivia Difficulties",
                description = "Easy\nMedium\nHard",
                color = self.colors.primary
            )
            await ctx.send(embed = embed)
            return
        if triviacategory == 'types':

            embed = discord.Embed(
                title = "Trivia Types",
                description = "Multiple\nBoolean",
                color = self.colors.primary
            )
            await ctx.send(embed = embed)
            return
        if triviacategory == 'help':

            embed = discord.Embed(
                title = "Trivia Help",
                description = "The trivia command supports extra parameters if you do wish to control what questions you get.\n\n" \
                    "**Command Parameters:** `.trivia [category id] [difficulty] [type]`\n" \
                    "**Command Example:** `.trivia 9 easy multiple` (9 = GK, Easy = Difficulty, Multiple = Multiple Choice Question)\n\n" \
                    "**Trivia Categories and IDs:** `.trivia categories`\n" \
                    "**Trivia Difficulties:** `.trivia difficulties`\n" \
                    "**Trivia Types:** `.trivia types`\n\n" \
                    "*By default, these parameters are set to 'any'. You can also set it manually, " \
                    "for example if you want to only control the difficulty and not the category, " \
                    "`.trivia any easy` will work, it gives an easy question from 'any' randomly picked category.*",
                color = self.colors.primary
            )
            await ctx.send(embed = embed)
            return

        # Manual Category Modifiers
        if triviacategory.isdigit():
            if int(triviacategory) > 8 and int(triviacategory) < 33:
                url += f'&category={triviacategory}'
        # Manual Difficulty Modifiers
        if triviadifficulty == 'easy': url += '&difficulty=easy'
        if triviadifficulty == 'medium': url += '&difficulty=medium'
        if triviadifficulty == 'hard': url += '&difficulty=hard'
        # Manual Type Modifiers
        if triviatype in {'multiple', 'mcq', 'choices'}: url += '&type=multiple'
        if triviatype in {'boolean', 'bool', 'true or false'}: url += '&type=boolean'

        async with self.session.get(url) as r:
            data = await r.json()
            question_type = data["results"][0]["type"]
            category = data["results"][0]["category"]
            question = data["results"][0]["question"]
            answer = data["results"][0]["correct_answer"]
            choices = data["results"][0]["incorrect_answers"]
            choices.append(answer)
            random.shuffle(choices)
            difficulty = data["results"][0]["difficulty"].capitalize()
        url = "https://opentdb.com"

        answer_number = 0
        options, number = [], 1
        for choice in choices:
            options.append(f"{number}] {html.unescape(choice)}")
            if choice == answer: answer_number = number
            number += 1
        
        question, answer = html.unescape(question), html.unescape(answer)

        timer = random.randint(6, 8) if question_type == 'boolean' else random.randint(9, 13)

        embed = discord.Embed(title = f"You have {timer} seconds to answer.", color = self.colors.primary)
        embed.set_author(
            name = f"Trivia Question for {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        embed.add_field(name = "Category", value = category, inline = True)
        embed.add_field(name = "Difficulty", value = difficulty, inline = True)
        
        embed.add_field(name = "Question", value = question, inline = False)
        embed.add_field(name = "Options", value = '\n'.join(options), inline = False)

        embed.set_footer(text = f"Use the number of the correct answer. • {url}")

        await ctx.send(embed = embed)

        check = lambda m: m.author == ctx.author and m.channel == ctx.channel

        try:
            user_answer = await self.bot.wait_for('message', check = check, timeout = timer)
        except asyncio.TimeoutError:
            await ctx.send(f"{self.emojis.cross} You didn't answer the question within {timer} seconds, {ctx.author.mention}. It was {answer}.")
        else:
            user_answer = user_answer.content
            if (user_answer.strip().lower() == answer.lower()) or (user_answer.strip() == str(answer_number)):
                await ctx.send(f"{self.emojis.tick} Your answer was correct! It's {answer}.")
            else:
                await ctx.send(f"{self.emojis.cross} Your answer was incorrect. The correct answer was {answer}.")

    @commands.command(brief = 'misc')
    async def bored(self, ctx):
        """Bored? Try this command."""

        async with self.session.get('http://www.boredapi.com/api/activity/') as r:
            res = await r.json()

        embed = discord.Embed(
            title = "Bored?",
            description = res['activity'],
            color = self.colors.primary,
            timestamp = datetime.utcnow()
        )
        embed.set_footer(text = f"{ctx.author} is bored.", icon_url = ctx.author.avatar_url)
        
        await ctx.send(embed = embed)
    
    @commands.command(brief = 'misc')
    async def smile(self, ctx):
        """Smile! :)"""

        smiles = (
            '😄', '😸', '😃', '😺',
            '😅', '🙂', '😁', '😀'
        )
        
        await ctx.send(random.choice(smiles))

def setup(bot):
    bot.add_cog(FunCog(bot))