import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class auto_voice(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.used = []

    @app_commands.command(name="канал-для-создания-приватки", description="Установить канал для создания приваток")
    async def auto_voice_set_channel(self, interaction:discord.Interaction, channel:discord.VoiceChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("У вас не хватает прав для выполнения команды!", ephemeral=True)
            return
        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        data["auto_voice_creation"] = True
        data["auto_voice_creation_channel"] = channel.id
        try:
            test = data["auto_voice_name"]
        except:
            data["auto_voice_name"] = "Канал {member}"

        with open(f"servers/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Изменения приняты!", ephemeral=True)

    @app_commands.command(name="включить-выключить-приватки", description="Вы можете включить или выключить приватные войс каналы")
    async def auto_voice_change_turn(self, interaction:discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("У вас не хватает прав для выполнения команды!", ephemeral=True)
            return
        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        data["auto_voice_creation"] = not data["auto_voice_creation"]

        with open(f"servers/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Изменения приняты!", ephemeral=True)

    @app_commands.command(name="добавить-войс-исключение", description="Чтобы защитить другие войсы от скрипта авто войс системы, добавьте их в белый список")
    async def auto_voice_add_exception(self, interaction:discord.Interaction, channel:discord.VoiceChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("У вас не хватает прав для выполнения команды!", ephemeral=True)
            return
        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
            data = json.load(f)

        try:
            data["auto_voice_exception"].append(channel.id)
        except:
            data["auto_voice_exception"] = [channel.id]

        with open(f"servers/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Изменения приняты!", ephemeral=True)


    @app_commands.command(name="изменить-названия-приваток", description="Измени названия приваток")
    async def auto_voice_change_name(self, interaction:discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("У вас не хватает прав для выполнения команды!", ephemeral=True)
            return
        class button(discord.ui.View):
            @discord.ui.button(label="Изменить", style=discord.ButtonStyle.blurple)
            async def change_button_callback(self, interaction:discord.Interaction, button):
                class modal(discord.ui.Modal, title="Настройка названия"):
                    name = discord.ui.TextInput(
                        label='Название',
                        style=discord.TextStyle.short,
                        placeholder='Введите название',
                        required=False,
                        max_length=500
                    )

                    async def on_submit(self, interaction: discord.Interaction):
                        with open(f"servers/{interaction.guild.id}.json", encoding="utf-8") as f:
                            data = json.load(f)

                        data["auto_voice_name"] = self.name.value

                        with open(f"servers/{interaction.guild.id}.json", "w") as f:
                            json.dump(data, f, indent=4)

                        await interaction.response.send_message("Изменения приняты", ephemeral=True)
                await interaction.response.send_modal(modal())
        emb = discord.Embed(title="Небольшая помощь", color=discord.Color.from_rgb(244, 169, 0))
        emb.add_field(name="{member}", value="Указывает имя участника создавшего приватку", inline=False)
        emb.add_field(name="{activity}", value="Указывает активность участника", inline=False)
        emb.set_footer(text=f"L.A Guru - {interaction.guild.name}", icon_url=interaction.guild.icon)

        await interaction.response.send_message(embed=emb, view=button(), ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after:discord.VoiceState):
        try:
            if after.channel is not None:
                with open(f"servers/{after.channel.guild.id}.json", encoding="utf-8") as f:
                    data = json.load(f)

                if after.channel.id == data["auto_voice_creation_channel"] and data["auto_voice_creation"] == True:
                    print("create")

                    if member.activity == None:
                        activity = "Без Активности"
                    else:
                        activity = member.activity.name

                    name = member.global_name.join(activity.join(data["auto_voice_name"].split("{activity}")).split("{member}"))
                    guild = self.bot.get_guild(after.channel.guild.id)
                    cat = guild.get_channel(after.channel.category.id)
                    channel = await guild.create_voice_channel(name=name, category=cat, position=after.channel.position)
                    await member.move_to(channel)

                    self.used.append(after.channel.id)

            elif before.channel is not None:
                if before.channel.id in self.used:
                    with open(f"servers/{before.channel.guild.id}.json", encoding="utf-8") as f:
                        data = json.load(f)

                    if len(before.channel.members) == 0 and before.channel.id in self.used:
                        print("delete")
                        self.used.remove(before.channel.id)
                        await before.channel.delete()
                    else:
                        pass

            elif before.channel and after.channel:
                if before.channel.id in self.used:
                    with open(f"servers/{before.channel.guild.id}.json", encoding="utf-8") as f:
                        data = json.load(f)

                    if len(before.channel.members) == 0 and before.channel.id != data["auto_voice_creation_channel"] and before.channel.id in self.used:
                        self.used.remove(before.channel.id)
                        await before.channel.delete()
                    else:
                        pass
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(auto_voice(bot), guilds=bot.guilds)
