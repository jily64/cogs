import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class verif(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.used = []

    @app_commands.command(name="verify", description="Настрой верификацию пользователей")
    async def verif(self, interaction:discord.Interaction):
        emb = discord.Embed(title="Верификация Пользователя", color=discord.Color.from_rgb(244, 169, 0))
        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)
            return
        class buttons(discord.ui.View):
            @discord.ui.button(label="Мальчик")
            async def male_callback(self, interaction:discord.Interaction, button):
                class user_id_modal(discord.ui.Modal, title="ID Пользователя"):
                    user = discord.ui.TextInput(
                        label='ID',
                        style=discord.TextStyle.short,
                        placeholder='Введите ID',
                        required=True,
                        max_length=500
                    )

                    async def on_submit(self, interaction: discord.Interaction):
                        try:
                            with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                                data = json.load(f)

                            role = interaction.guild.get_role(data["verify_male"])
                            user = interaction.guild.get_member(int(self.user.value))
                            await user.add_roles(role)
                            await interaction.response.send_message("Участник подтвержден!", ephemeral=True)
                        except:
                            await interaction.response.send_message("Ошибка! Либо у вас не настроены роли, либо просто ошибка.", ephemeral=True)
                await interaction.send_modal(user_id_modal())

            @discord.ui.button(label="Девочка")
            async def female_callback(self, interaction:discord.Interaction, button):
                class user_id_modal(discord.ui.Modal, title="ID Пользователя"):
                    user = discord.ui.TextInput(
                        label='ID',
                        style=discord.TextStyle.short,
                        placeholder='Введите ID',
                        required=True,
                        max_length=500
                    )

                    async def on_submit(self, interaction: discord.Interaction):
                        try:
                            with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                                data = json.load(f)

                            role = interaction.guild.get_role(data["verify_female"])
                            user = interaction.guild.get_member(int(self.user.value))
                            await user.add_roles(role)
                            await interaction.response.send_message("Участник подтвержден!", ephemeral=True)
                        except:
                            await interaction.response.send_message(
                                "Ошибка! Либо у вас не настроены роли, либо просто ошибка.", ephemeral=True)

                await interaction.response.send_modal(user_id_modal())

        await interaction.response.send_message(embed=emb, view=buttons(), ephemeral=True)


    @app_commands.command(name="verify-roles", description="Установка ролей для верификации")
    async def verify_set_roles(self, interaction:discord.Interaction, female:discord.Role, male:discord.Role):
        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message("Недостаточно прав", ephemeral=True)
            return
        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        data["verify_male"] = male.id
        data["verify_female"] = female.id

        with open(f"servers/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Изменения приняты!", ephemeral=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(verif(bot), guilds=bot.guilds)
