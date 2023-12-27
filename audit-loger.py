import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class audit(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="аудит", description="Настройки аудита")
    async def audit(self, interaction:discord.Interaction, channel:discord.TextChannel = None):
        emb = discord.Embed(title="Настройка аудита")
        emb.add_field(name="ВНИМАНИЕ!", value="Эта функция предусмотренна под настройку через сайт, но так как менеджер бота не добавлен на сайт, вы можете только включить или выключить данную функцию. Приносим извинения по данному поводу.")
        emb.add_field(name="Описание", value="Полный аудит всего, что происходит на сервере. Здесь вы можете настроить куда будут выводиться сообщения.", inline=False)
        emb.add_field(name="Использование", value="Просто прописав команду, вы вызовите просто сообщение с выключением или включением функции. Для настройки канала, используйте опцию channel в этой же команде")

        if channel == None:
            with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                data = json.load(f)
            try:
                if data["audit"] == True:
                    class turn_off_button(discord.ui.View):
                        @discord.ui.button(label="Отключить аудит", style=discord.ButtonStyle.red)
                        async def off_callback(self, interaction: discord.Interaction, button):
                            with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                                data = json.load(f)
                            data["audit"] = False

                            with open(f"servers/{interaction.guild.id}.json", "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=4)
                            emb = discord.Embed(title="Аудит отключен")
                            await interaction.response.send_message(embed=emb, ephemeral=True)
                            return

                    await interaction.response.send_message(embed=emb, ephemeral=True, view=turn_off_button())
                else:
                    await interaction.response.send_message(embed=emb, ephemeral=True)
            except:
                await interaction.response.send_message(embed=emb, ephemeral=True)

        else:
            with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                data = json.load(f)
            data["audit_channel"] = channel.id
            data["audit"] = True

            with open(f"servers/{interaction.guild.id}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            emb = discord.Embed(title="Успешно изменен канал.")
            await interaction.response.send_message(embed=emb, ephemeral=True)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        print(f'{before.author} изменил сообщение: "{before.content}" -> "{after.content}"')

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        print(f'Было создано новое приглашение: {invite.url} {invite.inviter.id}')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user} был забанен на сервере: {guild.name}')


    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        print(f'{user} был разбанен на сервере: {guild.name}')

    @commands.Cog.listener()
    async def on_member_timeout(self, member, timeout):
        print(f'{member} был отправлен в тайм-аут на сервере: {timeout}')


async def setup(bot: commands.Bot):
    await bot.add_cog(audit(bot), guilds=bot.guilds)
