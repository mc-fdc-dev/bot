from discord.ext import commands
import discord

import tweepy

import asyncio

from core import Cog, sql
from data import CONFIG


class TwitterAccount2(sql.Table):
    Userid = sql.BigintColumn()
    Token = sql.TextColumn()

class Twitter(Cog):
    TWITTER_API_KEY = CONFIG["twitter"]["api_key"]
    TWITTER_API_SECRET = CONFIG["twitter"]["api_secret"]
    def __init__(self, bot):
        self.bot = bot
        self.oauth1_user_handler = tweepy.OAuth1UserHandler(
            self.TWITTER_API_KEY, self.TWITTER_API_SECRET,
            callback="oob"
        )
        self.table = TwitterAccount2()

    async def cog_load(self) -> None:
        await self.table.create(self.bot.pool)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""CREATE TABLE IF NOT EXISTS TwitterAccount(
                    User BIGINT,
                    ApiKey TEXT,
                    ApiSecret TEXT
                );""")

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
            access_token, access_token_secret = self.oauth1_user_handler.get_access_token(
                message.content
            )
            await self.execute(
                "INSERT INTO TwitterAccount VALUES(%s, %s, %s);",
                (ctx.author.id, access_token, access_token_secret)
            )
            await channel.send(f"access_token: {access_token}\naccess_token_secret: {access_token_secret}")
        except asyncio.TimeoutError:
            await channel.send(embed=discord.Embed(
                title="twitterログイン",
                description="時間切れ"
            ))


async def setup(bot):
    await bot.add_cog(Twitter(bot))