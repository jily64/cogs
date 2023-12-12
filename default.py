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
            @discord.ui.select(placeholder="Ожидайте Следующих обновлений!", options=opt)
            async def select_callback(self, interaction:discord.Interaction, select):
                print("ddd")

        await interaction.response.send_message(embed=emb, view=select())

    @app_commands.command(name="say", description="sss")
    async def say(self, interaction:discord.Interaction, arg:str):
        print(arg)


    @commands.command()
    async def ads(self, ctx):
        la = self.bot.get_guild(1005146118054756352)
        emb = discord.Embed(title="Опача! Рекламка значит...", color = discord.Color.from_rgb(244, 169, 0))
        emb.add_field(name="Приятные люди", value="На нашем сервере есть прекрасные люди, с которыми можно спокойно общаться на различные темы!")
        emb.add_field(name="Хорошая администрация", value="У нас прекрасная администрация, которая поможет вам в любой ситуации!")
        emb.add_field(name="Не с кем поиграть?", value="У нас ты найдешь людей, с которыми ты сможешь поиграть в разные игры. От бравл страса и до Porta или других серий!")
        emb.set_footer(text="Владелец проекта - U4rce GDev", icon_url=la.icon)

        guild = self.bot.get_guild(779695182324301855)
        chann = guild.get_channel(779695182324301858)

        await chann.send(embed=emb)






async def setup(bot: commands.Bot):
    await bot.add_cog(cog(bot), guilds=bot.guilds)
