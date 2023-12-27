import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class sec(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="безопасность", description="Настройка систем безопасности сервера.")
    async def security(self, interaction:discord.Interaction):
        emb = discord.Embed(title="Настройка безопасности сервера")
        emb.add_field(name="Подробности о каждой функции", value="У нас на сайте, вы сможете найти нужную вам информацию по настройке бота")
        emb.set_footer(text=f"U4rce GDEV - {interaction.guild.name}", icon_url=interaction.guild.icon)




async def setup(bot: commands.Bot):
    await bot.add_cog(sec(bot), guilds=bot.guilds)
