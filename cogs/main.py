from core import Cog, FdcApp


class Main(Cog):
    def __init__(self, bot: FdcApp):
        self.bot = bot

    async def cog_load(self) -> None:
        async with self.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS Prefix(GuildId BIGINT, Prefix TEXT);")
    
    @Cog.command()
    async def prefix(self, ctx, prefix: str = "fd:"):
        async with self.acquire() as conn:
            async with conn.cursor() as cur:
                await self.execute(
                    "SELECT * FROM Prefix WHERE Guild = %s;", (ctx.guild.id,),
                    cursor=cur
                )
                if await self.fetchone(cursor=cur) is None:
                    await self.execute("INSERT INTO Prefix VALUES(%s, %s);", (ctx.guild.id, prefix))
                else:
                    await self.execute(
                        "UPDATE Prefix SET Prefix = %s WHERE GuildId = %s;", (prefix, ctx.guild.id),
                        cursor=cur
                    )
        await ctx.reply("設定したよ❤")

async def setup(bot: FdcApp) -> None:
    await bot.add_cog(Main(bot))
