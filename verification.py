import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class verif(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.used = []

    @app_commands.command(name="Верификация", description="Настрйо верификацию пользователей")
    async def verif(self, interaction:discord.Interaction):
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(verif(bot), guilds=bot.guilds)
