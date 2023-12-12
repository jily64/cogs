import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio

class rk(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="выдача", description="Установить сообщению роль на реакции")
    async def react(self, interaction: discord.Interaction, message_id: str, role_id: discord.Role, emoji_name: str):
        message_id = int(message_id)
        role_id = role_id.id
        if interaction.user.guild_permissions.administrator:
            with open(f"servers/{interaction.guild.id}.json", "r", encoding="utf-8") as f:
                datas = json.load(f)
                f.close()
            try:
                if 'rgr' not in datas:
                    datas["rgr"] = {}
            except:
                datas["rgr"] = {}

            data = datas["rgr"]

            try:
                message = data[str(message_id)]
                data[str(message_id)][emoji_name] = {
                    "role": int(role_id)
                }

            except:
                message = {
                    emoji_name: {
                        "role": int(role_id)
                    }
                }
                data[str(message_id)] = message
            datas["rgr"] = data
            print(emoji_name)
            with open(f"servers/{interaction.guild.id}.json", "w") as f:
                json.dump(datas, f, indent=4)
            channel = self.bot.get_channel(interaction.channel.id)
            message = await channel.fetch_message(int(message_id))
            await message.add_reaction(emoji_name)
            await interaction.response.send_message("Успешно добавлены роли на сообщение", ephemeral=True)

    @app_commands.command(name="очистить_сообщение", description="убрать все привязанные роли к сообщению")
    async def clear(self, interaction: discord.Interaction, message_id: str):
        if interaction.user.guild_permissions.administrator:
            message_id = int(message_id)
            with open(f"servers/{interaction.guild.id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                f.close()
            if str(message_id) in data["rgr"]:
                data["rgr"].pop(str(message_id))
                message = await interaction.channel.fetch_message(message_id)
                await message.clear_reactions()
                await interaction.response.send_message("Теперь сообщение чистенькое! :З", ephemeral=True)
            else:
                await interaction.response.send_message("Я не нашел такого сообщения(", ephemeral=True)

            with open(f"servers/{interaction.guild.id}.json", "w") as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        with open(f"servers/{payload.guild_id}.json", "r") as f:
            data = json.load(f)
            f.close()
        print(payload.emoji)
        if str(payload.message_id) in data["rgr"]:
            if str(payload.emoji) in data["rgr"][str(payload.message_id)]:
                role = self.bot.get_guild(payload.guild_id).get_role(data["rgr"][str(payload.message_id)][str(payload.emoji)]["role"])
                user = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        with open(f"servers/{payload.guild_id}.json", "r") as f:
            data = json.load(f)
            f.close()
        if str(payload.message_id) in data["rgr"]:
            if str(payload.emoji) in data["rgr"][str(payload.message_id)]:
                role = self.bot.get_guild(payload.guild_id).get_role(
                    data["rgr"][str(payload.message_id)][str(payload.emoji)]["role"])
                user = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await user.remove_roles(role)







async def setup(bot: commands.Bot):
    await bot.add_cog(rk(bot), guilds=bot.guilds)