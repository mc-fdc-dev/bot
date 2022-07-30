from core import Cog


class Main(Cog):
    
    @Cog.command()
    async def prefix(self, ctx):
        async with self.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO Prefix VALUES(%s, %s);", (
