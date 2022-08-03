from aiomysql import Cursor

from typing import Any

from inspect import getmembers


class BaseColumn:
    name: str | None = None
    type: Any = None
        
class TextColumn(BaseColumn):
    name = "TEXT"
    type = int()

class Table:
    def __init_subclass_(cls, tablename: str | None = None
                        ):
        self.tablename = cls.__name__ if self.tablename is None else self.tablename
        self.columns = {}
        for name, value in getmembers(cls):
            self.columns[name] = value
        super().__init_subclass__()

    async def insert
