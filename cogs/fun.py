# Discord.
import discord
# Command Handler.
from discord.ext import commands
# JSON Parser.
from utils import default
# Parsing HTML Special Characters (for Trivia)
import html
# Randomly picked integers and choices.
import random
# Asynchronous Requests.
import aiohttp
import asyncio
# Optional Command Parameters.
import typing


class FunCog(commands.Cog):
    """Entertainment & Miscellaneous Commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.config = default.get("config.json")
        self.colors = default.get("colors.json")
        self.emojis = default.get("emojis.json")
        self.bot_prefix = '.'

    #Usage: .{command.name} {command.usage}
    #embed.set_footer(text = command.help)


    @commands.command(aliases = ['hug'], usage = "[@user/id]")
    async def notice(self, ctx, user: discord.Member = None):
        """Notice me senpai!"""

        # Return the author if an user is not specified.
        user = user or ctx.author

        hugs = [
            "`＼(^o^)／`", "`d=(´▽｀)=b`", "`⊂((・▽・))⊃`"
            "`⊂( ◜◒◝ )⊃`", "`⊂（♡⌂♡）⊃`", r"`\(･◡･)/`",
            "`(づ｡◕‿‿◕｡)づ`", "`༼ つ ◕‿◕ ༽つ`", "`(づ￣ ³￣)づ`",
            "`(⊃｡•́‿•̀｡)⊃`",  "`ʕっ•ᴥ•ʔっ`", "`(o´･_･)っ`",
            "`(⊃ • ʖ̫ • )⊃`", "`(つ≧▽≦)つ`", "`(つ✧ω✧)つ`",
            "`(っ.❛ ᴗ ❛.)っ`", "`～(つˆДˆ)つ｡☆`", "`⊂(•‿•⊂ )*.✧`",
            "`⊂(´･◡･⊂ )∘˚˳°`", "`⊂(･ω･*⊂)`", "`⊂(・﹏・⊂)`",
            "`⊂(・▽・⊂)`", "`⊂(◉‿◉)つ`", "`o((*^▽^*))o`",
            "`╰(*´︶`*)╯`", "`╰(＾3＾)╯`", "`╰(⸝⸝⸝´꒳`⸝⸝⸝)╯`"
        ]

        await ctx.send(f"{user.mention}, `{random.choice(hugs)}`")
    
    @commands.command(aliases = ["feline", "tom", "mouser", "pussy", "meow"])
    async def cat(self, ctx, num: typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random cat picture from the internet."""

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

    @commands.command(aliases=["pupper", "woof", "doggo", "bork", "canine"])
    async def dog(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random dog picture from the internet."""

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
    
    @commands.command(name = "bird", aliases = ["birb", "ave", "birdie"])
    async def bird(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random birb picture from the internet."""

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
    
    @commands.command(name = "fox", aliases = ["foxie", "arf"])
    async def fox(self, ctx, num : typing.Optional[int] = 0, fact : bool = False):
        """Fetches a random fox picture from the internet."""

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
    
    @commands.command(name = "panda", aliases = ["achoo"])
    async def panda(self, ctx, fact : bool = False):
        """Fetches a random panda picture from the internet."""

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
    
    @commands.command(name = "koala")
    async def koala(self, ctx, fact : bool = False):
        """Fetches a random koala picture from the internet."""

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
    
    @commands.command(name = "anime")
    async def uwu(self, ctx):
        """Fetches a random anime picture from the internet."""

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
    
    @commands.command(name = "quote")
    async def quote(self, ctx):
        """Fetches a random quote from the internet."""

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
    
    @commands.command(name = 'meme', aliases = ['dankmeme', 'memes'], usage = '[memes/dankmemes/me_irl]')
    async def meme(self, ctx, subreddit: str = 'any'):
        """Fetches a meme for you."""

        meme_subreddits = ('r/memes', 'r/dankmemes', 'r/me_irl')

        if not subreddit.startswith('r/'): subreddit = f"r/{subreddit}"

        if subreddit not in meme_subreddits: subreddit = random.choice(meme_subreddits)

        subreddit = random.choice(meme_subreddits)
        url = f"https://www.reddit.com/{subreddit}/new.json?sort=hot"

        async with self.session.get(url) as r:
            res = await r.json()
            rand = random.randint(0, len(res['data']['children']))
            title = res["data"]["children"][rand]["data"]["title"]
            image = res["data"]["children"][rand]["data"]["url"]
            upvotes = res["data"]["children"][rand]["data"]["score"]
            comments = res["data"]["children"][rand]["data"]["num_comments"]
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = f"{subreddit} • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['wholesomememes', 'wholesome_meme', 'wholesomememe', 'wmeme'])
    async def wholesome(self, ctx):
        """Fetches a wholesome meme for you."""

        url = f"https://www.reddit.com/r/wholesomememes/new.json?sort=hot"

        async with self.session.get(url) as r:
            res = await r.json()
            rand = random.randint(0, len(res['data']['children']))
            title = res["data"]["children"][rand]["data"]["title"]
            image = res["data"]["children"][rand]["data"]["url"]
            upvotes = res["data"]["children"][rand]["data"]["score"]
            comments = res["data"]["children"][rand]["data"]["num_comments"]
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/wholesomememes • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(name = 'discordmeme', aliases = ['discordmemes', 'discordirl', 'discord_irl'])
    async def discordmeme(self, ctx):
        """Fetches a discord meme for you."""

        url = f"https://www.reddit.com/r/discord_irl/new.json?sort=hot"

        async with self.session.get(url) as r:
            res = await r.json()
            rand = random.randint(0, len(res['data']['children']))
            title = res["data"]["children"][rand]["data"]["title"]
            image = res["data"]["children"][rand]["data"]["url"]
            upvotes = res["data"]["children"][rand]["data"]["score"]
            comments = res["data"]["children"][rand]["data"]["num_comments"]
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/discord_irl • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(name = 'surrealmeme', aliases = ['surreal', 'surrealmemes'])
    async def surrealmeme(self, ctx):
        """Fetches a surreal meme for you."""

        url = f"https://www.reddit.com/r/surrealmemes/new.json?sort=hot"

        async with self.session.get(url) as r:
            res = await r.json()
            rand = random.randint(0, len(res['data']['children']))
            title = res["data"]["children"][rand]["data"]["title"]
            image = res["data"]["children"][rand]["data"]["url"]
            upvotes = res["data"]["children"][rand]["data"]["score"]
            comments = res["data"]["children"][rand]["data"]["num_comments"]
        
        embed = discord.Embed(title = title, url = image, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = f"r/surrealmemes • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['todayilearned'])
    async def til(self, ctx):
        """You learn something new everyday!"""

        url = "https://www.reddit.com/r/todayilearned/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']))
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
        embed.set_footer(text = f"r/todayilearned • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['jokes'])
    async def joke(self, ctx):
        """Gives you an joke."""

        url = "https://www.reddit.com/r/Jokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']))
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
        embed.set_footer(text = f"r/Jokes • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['antijokes'])
    async def antijoke(self, ctx):
        """Gives you an anti-joke."""

        url = "https://www.reddit.com/r/AntiJokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']))
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
        embed.set_footer(text = f"r/AntiJokes • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['antiantijokes'])
    async def antiantijoke(self, ctx):
        """Gives you an anti-anti-joke."""

        url = "https://www.reddit.com/r/AntiAntiJokes/new.json?sort=hot"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']))
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
        embed.set_footer(text = f"r/AntiAntiJokes • 👍 {upvotes} • 💬 {comments}")
        await ctx.send(embed = embed)
    
    @commands.command(name = 'reddit', usage = '[r/subreddit]')
    async def reddit(self, ctx, subreddit: str = 'r/all', sort_by: str = 'hot'):
        """Fetches content from a specified subreddit."""

        subreddit = subreddit.strip()
        if not subreddit.startswith('r/'):
            subreddit = 'r/' + subreddit
        
        url = f"https://www.reddit.com/{subreddit}/new.json?sort={sort_by}"

        async with self.session.get(url) as r:
            post = await r.json()
            rand = random.randint(0, len(post['data']['children']))
            post = post["data"]["children"][rand]["data"]
            title = post["title"]
            image = post["url"]
            content = post["selftext"]
            link = "https://www.reddit.com" + post["permalink"]
            nsfw = post["over_18"]
        
        if nsfw and not ctx.channel.nsfw:
            await ctx.send("⚠️ This post contains NSFW content! It cannot be previewed here.")
            return

        embed = discord.Embed(title = title, url = link, description = content, color = self.colors.primary)
        embed.set_image(url = image)
        embed.set_footer(text = subreddit)
        await ctx.send(embed = embed)
        
    @commands.command(name = "trivia", usage = "[category] [difficulty] [type]")
    async def trivia(self, ctx, triviacategory : typing.Union[str, int] = 'any', triviadifficulty : str = 'any', triviatype : str = 'any'):
        """Gives you a trivia question to answer. `trivia help`"""

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

        def check(m): return m.author == ctx.author and m.channel == ctx.channel

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

def setup(bot):
    bot.add_cog(FunCog(bot))