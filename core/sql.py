from aiomysql import Pool

from typing import Any

from inspect import getmembers


class BaseColumn:
    name: str | None = None
    type: Any = None
        
class TextColumn(BaseColumn):
    name = "TEXT"
    type = str

class BigintColumn(BaseColumn):
    name = "BIGINT"
    type = int

class Table:
    name: str
    columns: dict
    pool: Pool
    def __init_subclass__(cls, *, name: str | None = None):
        cls.name = cls.__name__ if name is None else name
        cls.columns = {}
        for name in dir(cls):
            if isinstance(column := getattr(cls, name), BaseColumn):
                cls.columns[name] = getattr(cls, name)

    async def create(self, pool: Pool) -> None:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS {} ({});".format(
                    self.name, ", ".join(
                        f"{name} {column.name}" for name, column in self.columns.items()
                )))

    async def insert(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self.columns:
                raise KeyError(f"{name} is not a column in {self.name}")
            if not isinstance(value, self.columns[name].type):
                raise TypeError(f"{name} is not of type {self.columns[name].type}")
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(
                    self.name, ", ".join(kwargs.keys()), ", ".join("%s" for _ in kwargs.values())
                ), (*kwargs.values(),))