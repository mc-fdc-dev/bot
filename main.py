from core import FdcBot
import json


with open("config.json", "r") as f:
    config = json.load(f)
bot = FdcBot(mysql=config["mysql"])

@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.load_extension("jishaku")

bot.run(config["token"])