# cogs - role
from discord.ext import commands


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="role")
    async def role(self, ctx, title: str, *, role: str):
        pass
