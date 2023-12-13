import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class cog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Узнай что я могу!")
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
                discord.SelectOption(label="Модерация"),
                discord.SelectOption(label="Разное"),
                discord.SelectOption(label="Разработчики")
            ]
            @discord.ui.select(placeholder="Ожидайте Следующих обновлений!", options=opt)
            async def select_callback(self, interaction:discord.Interaction, select):
                if select.values[0] == "Модерация":
                    emb2 = discord.Embed(title="Помощь по настройке модерации", color=discord.Color.from_rgb(255, 0, 230))
                    emb2.add_field(name="/moderation-setting", value="Основные настройки модерации")
                    emb2.add_field(name="/set-hello-bey-channel", value="Установить каналы для вывода приветствий и прощаний")
                    emb2.add_field(name="/server-info", value="Информация о сервере", inline=False)
                    emb2.set_footer(text=f"L.A Guru - {interaction.guild.name}", icon_url=interaction.guild.icon)

                elif select.values[0] == "Разное":
                    emb2 = discord.Embed(title="Другие фун-ции бота",
                                         color=discord.Color.from_rgb(255, 0, 230))
                    emb2.add_field(name="/выдача", value="Установить роль для рекции поставленной под определенным сообщением")
                    emb2.add_field(name="/очистить-сообщение", value="Убарть все реакции с назначеными ролями с сообщения")

                    emb2.add_field(name="/say", value="Сказать от имени бота (на некоторых серверах недоступно)", inline=False)

                    emb2.add_field(name="/канал-для-создания-приватки", value="Назначить канал для приваток")
                    emb2.add_field(name="/включить-выключить-приватки", value="Вы можете включить или выключить данную функцию (автоматически включается при назначении канала)")
                    emb2.add_field(name="/добавить-войс-исключение", value="Во время бета теста, бот может немного пошалить, обезопасьте себя этой командой", inline=False)
                    emb2.add_field(name="/изменить-названия-приваток", value="Измените название создаваемого канала")

                    emb2.set_footer(text=f"L.A Guru - {interaction.guild.name}", icon_url=interaction.guild.icon)

                elif select.values[0] == "Разработчики":
                    emb2 = discord.Embed(title="Разработчики",
                                         color=discord.Color.from_rgb(255, 0, 230))
                    emb2.add_field(name="U4rce GDev",
                                   value="Команда разработчиков игр и ботов для телеграмм и дискорд. Работает с 2020 года")

                    emb2.set_footer(text=f"L.A Guru - {interaction.guild.name}", icon_url=interaction.guild.icon)
                    emb2.set_image(url="https://i.imgur.com/HelSf8s.png")

                await interaction.response.send_message(embed=emb2, ephemeral=True)


        await interaction.response.send_message(embed=emb, view=select(), ephemeral=True)

    @app_commands.command(name="say", description="sss")
    async def say(self, interaction:discord.Interaction, arg:str):
        print(arg)

    @app_commands.command(name="server-info", description="Давай я покажу показатели этого сервера!")
    async def server_info(self, interaction:discord.Interaction):
        emb = discord.Embed(title=interaction.guild.name, color=discord.Color.from_rgb(244, 169, 0))

        online = 0
        offline = 0
        donot = 0
        sleep = 0

        for i in interaction.guild.members:
            if i.status == discord.Status.online:
                online+=1
            elif i.status == discord.Status.offline:
                offline+=1
            elif i.status == discord.Status.dnd:
                donot+=1
            elif i.status == discord.Status.idle:
                sleep+=1
        emb.add_field(name="Участники", value=f"Online: {online}\nOffline: {offline}\nIdle: {sleep}\nDND: {donot}")
        emb.add_field(name="Всего участников", value=str(len(interaction.guild.members)))
        emb.add_field(name="Создан", value=str(interaction.guild.created_at.strftime("%Y.%m.%d")), inline=False)
        emb.add_field(name="Владелец", value=interaction.guild.owner.name)
        emb.set_footer(icon_url=interaction.guild.icon, text=f"L.A Guru - {interaction.guild.name}")

        await interaction.response.send_message(embed=emb)
    @commands.command()
    async def ads(self, ctx):
        la = self.bot.get_guild(1005146118054756352)
        emb = discord.Embed(title="Опача! Рекламка значит...", color=discord.Color.from_rgb(244, 169, 0))
        emb.add_field(name="Приятные люди", value="На нашем сервере есть прекрасные люди, с которыми можно спокойно общаться на различные темы!")
        emb.add_field(name="Хорошая администрация", value="У нас прекрасная администрация, которая поможет вам в любой ситуации!")
        emb.add_field(name="Не с кем поиграть?", value="У нас ты найдешь людей, с которыми ты сможешь поиграть в разные игры. От бравл страса и до Porta или других серий!")
        emb.set_footer(text="Владелец проекта - U4rce GDev", icon_url=la.icon)

        guild = self.bot.get_guild(777455887715008582)
        chann = guild.get_channel(1179821694056157255)

        await chann.send(embed=emb, content="https://discord.gg/BpmZeK2fDg")



    @app_commands.command(name="send_update", description="send update info")
    async def send_update_info(self, interaction:discord.Interaction):
        print(len(self.bot.guilds))
        if interaction.user.id == 727210460356673607:
            for i in self.bot.guilds:
                for j in i.text_channels:
                    print(j.name)
                    try:
                        emb = discord.Embed(title="Вышло новое обновление! (1.0.4)", color=discord.Color.from_rgb(244, 169, 0))
                        emb.add_field(name="Теперь есть приватки!", value="Теперь ваши пользователи могу создавать личные каналы! Как их настроить, читайте в /help; Разное")
                        emb.set_footer(text=f"L.A Guru - {i.name}", icon_url=i.icon)
                        await j.send(embed=emb)
                        break
                    except Exception as e:
                        print(e)

                print(i.name)

async def setup(bot: commands.Bot):
    await bot.add_cog(cog(bot), guilds=bot.guilds)
