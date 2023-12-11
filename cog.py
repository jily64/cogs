import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
print("loh")
class cog1(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="loh", description="Узнай что я могу!")
    async def help(self, interaction:discord.Interaction):
        await interaction.response.send_message("loh")



async def setup(bot: commands.Bot):
    await bot.add_cog(cog1(bot), guilds=bot.guilds)
