from discord.ext import commands
import discord

import tweepy

import asyncio

from core import Cog
from data import CONFIG


class Twitter(Cog):
    TWITTER_API_KEY = CONFIG["twitter"]["api_key"]
    TWITTER_API_SECRET = CONFIG["twitter"]["api_secret"]
    def __init__(self, bot):
        self.bot = bot
        self.oauth1_user_handler = tweepy.OAuth1UserHandler(
            self.TWITTER_API_KEY, self.TWITTER_API_SECRET,
            callback="oob"
        )

    @commands.group()
    async def twitter(self, ctx):
        pass

    @twitter.command(name="login", description="twitterにログインします。")
    async def login(self, ctx):
        channel = await ctx.author.create_dm()
        await channel.send(embed=discord.Embed(
            title="twitterログイン",
            description=(
                "3分以内に下のurlにアクセスし、出てきたコードを入力してください。"
                f"\n{self.oauth1_user_handler.get_authorization_url()}"
            )
        ))
        try:
            message = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == channel,
                timeout=180
            )
        except asyncio.TimeoutError:
            await channel.send(embed=discord.Embed(
                title="twitterログイン",
                description="時間切れ"
            ))