import discord
from discord import app_commands
from datetime import datetime
import os

TOKEN = "MTQ3NDAzNDY3MjQ5MjIyMDQ5OQ.Ga54iW.up5QHiYVkQ3zLD1S79QXLYA3BHx5-UljATVZJg"

LOG_CHANNEL_ID = 1474037746463932612  # 🔹 로그 채널 ID
BOG_ROLE_ID = 1472071539586240634     # 🔹 명령어 사용 가능한 역할 ID

intents = discord.Intents.default()
intents.members = True


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


client = MyClient()


@client.tree.command(name="역할삽입", description="유저에게 역할을 부여하고 로그를 남깁니다")
@app_commands.describe(대상유저="역할을 받을 유저", 역할="추가할 역할")
async def 역할삽입(interaction: discord.Interaction, 대상유저: discord.Member, 역할: discord.Role):

    # 🔹 역할 권한 체크
    if BOG_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message(
            "이 명령어는 '이사진 | BOG' 역할이 있는 사람만 사용할 수 있습니다.",
            ephemeral=True
        )
        return

    # 🔹 역할 추가
    await 대상유저.add_roles(역할)

    await interaction.response.send_message(
        f"{대상유저.mention} 님에게 {역할.mention} 역할을 추가했습니다.",
        ephemeral=True
    )

    # 🔹 로그 채널 가져오기
    log_channel = client.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="📌 역할 삽입 로그",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        embed.add_field(
            name="명령어 사용자",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="대상 유저",
            value=대상유저.mention,
            inline=False
        )

        embed.add_field(
            name="추가된 역할",
            value=역할.mention,
            inline=False
        )

        embed.set_footer(text="Role Management System")

        await log_channel.send(embed=embed)


client.run(TOKEN)



