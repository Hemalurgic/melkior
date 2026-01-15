import asyncio
import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from services.database import init_db


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Melkior has awakened. Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} guild(s)")


async def main():
    await init_db()
    await bot.load_extension("cogs.chat")
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
