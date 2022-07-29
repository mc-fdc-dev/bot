from discord.ext import commands
import discord

from aiomysql import create_pool

class FdcBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.mysql = kwargs.pop("mysql")
        kwargs["command_prefix"] = self._command_prefix
        self.prefixes = {}
        super().__init__(*args, **kwargs)

    def _command_prefix(self, message: discord.Message) -> str:
        if message.guild.id in self.prefixes:
            return self.prefixes[message.guild.id]
        else:
            return "fb."

    async def setup_hook(self) -> None:
        self.pool = create_pool(**self.mysql)
