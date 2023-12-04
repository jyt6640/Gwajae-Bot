import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os

# .env 파일로부터 환경 변수 로드
load_dotenv()

# .env 파일에서 토큰 가져오기
token = os.getenv('TOKEN')
print("Token from .env:", token)

# .env 파일에 'TOKEN'이라는 키가 없으면 KeyError가 발생할 수 있으므로 주의
# 가능하면 키가 없을 때 기본값을 사용하거나 예외 처리를 추가하는 것이 좋습니다.
# 예: token = os.getenv('TOKEN', 'default_token_value')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 준비 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("과제"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "테스트":
        await message.channel.send(f'{message.author.mention}, hello')
        await message.author.send(f'{message.author.mention}, User, hello')

    await bot.process_commands(message)

@bot.command(name='테스트')
async def test_command(ctx):
    await ctx.send(f'{ctx.author.mention}, hello')
    await ctx.author.send(f'{ctx.author.mention}, User, hello')

bot.run(token)
