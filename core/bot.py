from discord.ext import commands
import discord

from motor import motor_asyncio as motor

class FdcBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        pass

    def _command_prefix(self, message: discord.Message) -> str:
        pass

    async def setup_hook(self) -> None:
        self.db = motor.AsyncIOMotorClient("")["FdcBot"]

    def get_collection(self, name: str):
        return self.db[name]
