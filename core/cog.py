from discord.ext import commands

from aiomysql import Cursor

from typing import Any, List


class Cog(commands.Cog):
    
    @property
    def acquire(self) -> Any:
        return self.bot.acquire
    
    async def execute(self, *args, cursor: Cursor | None = None, **kwargs) -> None:
        if cursor is None:
            async with self.bot.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(*args, **kwargs)
        await cursor.execute(*args, **kwargs)
 
    async def fetchone(self, *, cursor: Cursor | None = None) -> Any:
        if cursor is None:
            async with self.bot.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.fetchone(*args, **kwargs)
        await cursor.fetchone(*args, **kwargs)

    async def fetchall(self, *, cursor: Cursor | None = None) -> List[Any]:
        if cursor is None:
            async with self.bot.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.fetchall(*args, **kwargs)
        await cursor.fetchall(*args, **kwargs)
