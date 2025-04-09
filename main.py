# 🌷 Replit 웹 서버로 24시간 유지시키기 위한 코드
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "공주님의 봇이 마법처럼 작동 중이에요! 🏰✨"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------------------------------------------

# 💖 디스코드 봇 코드 시작!
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

PASSWORD = "0330"
WAIT_ROLE = "𖹭"
PASS_ROLE = "☘︎"
TARGET_CHANNEL_ID = 1359204289683390736  # ← 여기에 #𝑃𝐴𝑆𝑆𝑊𝑂𝑅𝐷 채널 ID 넣기!

# 🧁 버튼 누르면 비밀번호 입력 모달 뜨는 뷰
class PasswordView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            Button(
                label="비밀번호 ☘︎",
                style=discord.ButtonStyle.success,
                custom_id="password_button"
            )
        )

# 🍡 모달 입력창
class PasswordModal(Modal, title="🌸입장 비밀번호"):
    password = TextInput(label="비밀번호를 입력해주세요", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        if self.password.value == PASSWORD:
            guild = interaction.guild
            member = interaction.user
            wait_role = discord.utils.get(guild.roles, name=WAIT_ROLE)
            pass_role = discord.utils.get(guild.roles, name=PASS_ROLE)

            if pass_role:
                await member.add_roles(pass_role)
                if wait_role in member.roles:
                    await member.remove_roles(wait_role)
                await interaction.response.send_message("✨인증되었습니다", ephemeral=True)
            else:
                await interaction.response.send_message("❌ '입장 완료' 역할이 없어요!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 비밀번호가 틀렸어요! 다시 시도해주세요.", ephemeral=True)

# 💫 버튼 클릭 시 모달 띄우기
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "password_button":
            await interaction.response.send_modal(PasswordModal())

# 🌟 봇 실행 시 인증 메시지 자동 전송
@bot.event
async def on_ready():
    print(f"공주님의 봇 {bot.user} 가 마법처럼 작동 중이에요! 🏰✨")

    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        view = PasswordView()
        await channel.send(
            "\u200b\n"
            "\n\n ⁺. ⊹˚₊ ₊·(੭ ˙ྌ˙ )੭‧*  𝗛𝗲𝗹𝗹𝗼, 𝘄𝗼𝗿𝗹𝗱!  \n\n\n"
            "\u200b\n",
            view=view
        )

# 👑 서버 입장 시 대기 역할 부여
@bot.event
async def on_member_join(member):
    guild = member.guild
    wait_role = discord.utils.get(guild.roles, name=WAIT_ROLE)
    if wait_role:
        await member.add_roles(wait_role)
        print(f"{member}님에게 '{WAIT_ROLE}' 역할을 부여했어요!")

# 🪄 웹서버 실행 (24시간 유지용)
keep_alive()

# 💫 디스코드 봇 실행
bot.run(os.getenv("DISCORD_TOKEN"))
