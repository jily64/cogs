import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class cog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help2", description="Узнай что я могу!")
    async def help(self, interaction:discord.Interaction):
        emb = discord.Embed(title="Опаньки! Что это тут?", description="Нука давай посмотрим, что ты можешь потыкать :3", color=discord.Color.from_rgb(255, 0, 230))
        emb.add_field(name="Партнерская программа", value="Если у тебя есть наша партнерская программа, то ты можешь узнать, что ты можешь использовать!")
        emb.add_field(name="Модерация", value="Я помогу тебе следить за сервером!")
        emb.add_field(name="Экономика", value="Деньги на бочку!")
        emb.add_field(name="Империя", value="Приветствую вождь! Вступай в нашу импперию Land.ADM!")
        emb.add_field(name="Другое", value="Авто-войс каналы, роли по реакциям")
        emb.add_field(name="Разработчики", value="Интересно узнать кто и как меня создавал?")

        emb.set_footer(text=f"L.A Guru - {interaction.guild.name}", icon_url=interaction.guild.icon)

        class select(discord.ui.View):
            opt = [
                discord.SelectOption(label="Зиза Лох")
            ]
            @discord.ui.select(placeholder="Зацени ебейшие описания", options=opt)
            async def select_callback(self, interaction:discord.Interaction, select):
                print("ddd")

        await interaction.response.send_message(embed=emb, view=select())



async def setup(bot: commands.Bot):
    await bot.add_cog(cog(bot), guilds=bot.guilds)
