import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class mod(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="modaretion-settings", description="Настройка модерации")
    async def mod_settings(self, interaction:discord.Interaction):
        emb = discord.Embed(title="Настройки модерации")
        emb.add_field(name="Приветствия и прощания", value="Давай настроим, как будем встречать и прощаться с участниками!")

        if interaction.user.guild_permissions.administrator:
            class select_option(discord.ui.View):


                opt = [
                    discord.SelectOption(label="Установить Прощание и приветствие")
                ]

                @discord.ui.select(placeholder="Выбери настройку", options=opt)
                async def select_callback(self, interaction:discord.Interaction, select:discord.ui.Select):
                    with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                        data = json.load(f)
                    if select.values[0] == "Установить Прощание и приветствие":
                        class change_hm_modal(discord.ui.Modal, title="Время что то менять!"):

                            qq = discord.ui.TextInput(
                                label='Приветствие',
                                style=discord.TextStyle.short,
                                placeholder='Введите приветствие',
                                required=False,
                                max_length=500,
                                default="Используй маркер {member} для выделения участника"
                            )


                            bb = discord.ui.TextInput(
                                label='Прощание',
                                style=discord.TextStyle.short,
                                placeholder='Введите прощание',
                                required=False,
                                max_length=500,
                                default="Используй маркер {member} для выделения участника"
                            )
                            async def on_submit(self, interaction:interaction.response):
                                try:
                                    data["mod"]["bb"] = self.bb.value
                                    data["mod"]["qq"] = self.bb.value
                                except:
                                    data["mod"] = {
                                        "hello_channel": None,
                                        "bb_channel": None,
                                        "bb": self.bb.value,
                                        "qq": self.qq.value
                                    }

                                with open(f"servers/{interaction.guild.id}.json", "w") as f:
                                    json.dump(data, f, indent=4)

                                await interaction.response.send_message(f"{self.qq.value}\n\n{self.bb.value}")
                        await interaction.response.send_modal(change_hm_modal())
            await interaction.response.send_message(embed=emb, view=select_option())

    @app_commands.command(name="set-hello-bey-channel", description="Установить канал для Приветствий и прощаний")
    async def set_channel_bbqq(self, interaction:discord.Interaction, hello:discord.TextChannel=None, bey:discord.TextChannel=None):
        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        try:
            data["mod"]["hello_channel"] = hello.id
            data["mod"]["bb_channel"] = bey.id
        except:
            data["mod"] = {
                "hello_channel": hello.id,
                "bb_channel": bey.id,
                "bb": "",
                "qq": ""
            }
        with open(f"servers/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Изменения приняты!", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open(f"servers/{member.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        try:
            hello_message = member.mention.join(data["mod"]["qq"].split("{member}"))
            channel = member.guild.get_channel(data["mod"]["hello_channel"])
            await channel.send(hello_message)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open(f"servers/{member.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        try:
            hello_message = member.mention.join(data["mod"]["bb"].split("{member}"))
            channel = member.guild.get_channel(data["mod"]["bb_channel"])
            await channel.send(hello_message)
        except:
            pass





async def setup(bot: commands.Bot):
    await bot.add_cog(mod(bot), guilds=bot.guilds)
