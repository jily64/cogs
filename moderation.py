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
        emb.add_field(name="Приветствия и прощания")

        if interaction.user.guild_permissions.administrator:
            class select_option(discord.ui.View):


                opt = [
                    discord.SelectOption(label="Установить Прощание и приветствие")
                ]

                @discord.ui.select(placeholder="Выбери настройку", options=opt)
                async def select_callback(self, interaction:discord.Interaction, select:discord.ui.Select):
                    with open(f"servers/{interaction.guild.id}.json") as f:
                        data = json.load(f, encoding="utf-8")
                    if select.values[0] == "Установить Прощание и приветствие":
                        class change_hm_modal(discord.ui.Modal, title="Время что то менять!", description="Используй маркер {member} для выделения участника"):
                            bb = discord.ui.TextInput(
                                label='Приветствие',
                                style=discord.TextStyle.short,
                                placeholder='Введите приветствие',
                                required=False,
                                max_length=500,
                                default=select.values[0]
                            )

                            qq = discord.ui.TextInput(
                                label='Прощание',
                                style=discord.TextStyle.short,
                                placeholder='Введите прощание',
                                required=False,
                                max_length=500,
                                default=select.values[0]
                            )
                            async def on_submit(self, interaction:interaction.response):
                                try:
                                    data["mod"]["bb"] = self.bb.value
                                    data["mod"]["qq"] = self.bb.value
                                except:
                                    data["mod"] = {
                                        "bb": self.bb.value,
                                        "qq": self.qq.value
                                    }

                                await interaction.response.send_message(f"{self.qq.value}\n\n{self.bb.value}")
                        await interaction.response.send_modal(modal=change_hm_modal())
            await interaction.response.send_message(embed=emb, view=select_option())


async def setup(bot: commands.Bot):
    await bot.add_cog(mod(bot), guilds=bot.guilds)
