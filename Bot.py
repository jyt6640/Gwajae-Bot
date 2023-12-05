import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

dotenv_file_path = r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\토큰.env'

# .env 파일로부터 환경 변수 로드
load_dotenv(dotenv_file_path)

# .env 파일에서 토큰 가져오기
token = os.environ.get('tik')
print("Token from .env:", token)

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

    await bot.process_commands(message)

@bot.command(name='테스트')
async def test_command(ctx):
    await ctx.send(f'{ctx.author.mention}, hello')
    await ctx.author.send(f'{ctx.author.mention}, User, hello')

bot.run(token)
