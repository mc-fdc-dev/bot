from discord.ext import commands
import discord

from aiomysql import create_pool

import os

from data import CONFIG


class FdcApp(commands.Bot):
    def __init__(self, *args, **kwargs):
        kwargs["command_prefix"] = self._command_prefix
        kwargs["intents"] = discord.Intents.all()
        self.prefixes = {}
        super().__init__(*args, **kwargs)

    def _command_prefix(self, _, message: discord.Message) -> str:
        if message.guild.id in self.prefixes:
            return self.prefixes[message.guild.id]
        else:
            return "fb."

    async def on_message(self, message: discord.Message) -> None:
        if isinstance(message.channel, discord.DMChannel):
            return
        await self.process_commands(message)
            
    async def setup_hook(self) -> None:
        self.pool = await create_pool(**CONFIG["mysql"])
        print("Connect to database")
        for cog in os.listdir("cogs"):
            if cog.startswith("__"):
                continue
            await self.load_extension("cogs." + cog[:-3])
