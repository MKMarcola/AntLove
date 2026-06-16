import discord
from discord import app_commands
import random
import datetime

import os
TOKEN = os.getenv("MTUxNTk5MzkwMTY4MzU3MjgwNw.Ghp762.Z3EgSJ78f1mAQBG33r7qGhF5JXoCl9J-KHFVgg")

intents = discord.Intents.all()

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        # banco fake (em memória)
        self.db = {}
        self.auto_role_id = None  # coloque ID do cargo aqui se quiser

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"✅ Bot online como {self.user}")

    # 🧠 XP + DINHEIRO
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)

        if user_id not in self.db:
            self.db[user_id] = {
                "xp": 0,
                "nivel": 1,
                "dinheiro": 0,
                "daily": None
            }

        user = self.db[user_id]

        # XP
        ganho = random.randint(5, 15)
        user["xp"] += ganho

        if user["xp"] >= user["nivel"] * 100:
            user["nivel"] += 1
            await message.channel.send(
                f"🚀 {message.author.mention} subiu para nível {user['nivel']}!"
            )

        # dinheiro
        user["dinheiro"] += random.randint(1, 10)

        # 🛡️ anti-link
        if "http" in message.content:
            await message.delete()
            await message.channel.send(
                f"🚫 {message.author.mention} links não são permitidos!"
            )

    # 👤 auto cargo
    async def on_member_join(self, member):
        if self.auto_role_id:
            role = member.guild.get_role(self.auto_role_id)
            if role:
                await member.add_roles(role)

bot = Bot()

# 💰 SALDO
@bot.tree.command(name="saldo", description="Ver seu dinheiro")
async def saldo(interaction: discord.Interaction):
    user = bot.db.get(str(interaction.user.id), {"dinheiro": 0})
    await interaction.response.send_message(
        f"💰 Você tem {user['dinheiro']} moedas"
    )

# 🎁 DAILY
@bot.tree.command(name="daily", description="Recompensa diária")
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    if user_id not in bot.db:
        bot.db[user_id] = {"xp": 0, "nivel": 1, "dinheiro": 0, "daily": None}

    user = bot.db[user_id]
    now = datetime.datetime.utcnow()

    if user["daily"] and (now - user["daily"]).total_seconds() < 86400:
        await interaction.response.send_message(
            "⏳ Você já pegou seu daily hoje!"
        )
        return

    user["daily"] = now
    user["dinheiro"] += 500

    await interaction.response.send_message(
        "🎁 Você ganhou 500 moedas!"
    )

# 🏆 RANK
@bot.tree.command(name="rank", description="Ver nível")
async def rank(interaction: discord.Interaction):
    user = bot.db.get(str(interaction.user.id), {"xp": 0, "nivel": 1})
    await interaction.response.send_message(
        f"🏆 Nível {user['nivel']} | XP {user['xp']}"
    )

# 🛡️ BAN
@bot.tree.command(name="ban", description="Banir usuário")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member):
    await user.ban()
    await interaction.response.send_message(f"🔨 {user} foi banido")

# 👢 KICK
@bot.tree.command(name="kick", description="Expulsar usuário")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, user: discord.Member):
    await user.kick()
    await interaction.response.send_message(f"👢 {user} foi expulso")

# 🎟️ TICKET
@bot.tree.command(name="ticket", description="Abrir suporte")
async def ticket(interaction: discord.Interaction):
    channel = await interaction.guild.create_text_channel(
        name=f"ticket-{interaction.user.name}"
    )
    await interaction.response.send_message(
        f"🎟️ Ticket criado: {channel.mention}"
    )

# 🧹 LIMPAR
@bot.tree.command(name="limpar", description="Apagar mensagens")
@app_commands.default_permissions(manage_messages=True)
async def limpar(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)
    await interaction.response.send_message(
        f"🧹 {quantidade} mensagens apagadas",
        ephemeral=True
    )

# 🏓 PING
@bot.tree.command(name="ping", description="Verificar bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

bot.run ("MTUxNTk5MzkwMTY4MzU3MjgwNw.Ghp762.Z3EgSJ78f1mAQBG33r7qGhF5JXoCl9J-KHFVgg")