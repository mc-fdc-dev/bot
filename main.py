from core import FdcApp
import json

from data import CONFIG

bot = FdcApp()

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.load_extension("jishaku")

bot.run(CONFIG["token"])