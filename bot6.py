#라이브러리 및 모듈 임포트
import openai
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

#환경 변수 및 토큰 설정
dotenv_file_path = r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\토큰.env'
load_dotenv(dotenv_file_path)

token = os.environ.get('tik')
ai = os.environ.get('ai')

#봇 설정 및 이벤트 핸들링
intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='$', intents=intents)
openai.api_key = ai

#봇 이벤트 설정
@bot.event 
async def on_ready(): #봇이 실행 될 때
    print(f'We have logged in as {bot.user}') #봇을 실행시 출력창에 출력

#OpenAi와 상호작용 (!chat 질문 형식으로 질의)
@bot.event
async def on_message(message):
    print(message)

    if message.author == bot.user:
        return
    text = message.content
    if text.startswith('!chat'): #명령어
        prompt = text[6:]
        bot_response = openai.Completion.create( #gpt 모델 설정
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        print('bot response:', bot_response)
        bot_text = bot_response['choices'][0]['text']
        await message.channel.send(f"> Your prompt is: {prompt}\nAnswer: {bot_text}") #출력 양식

@bot.command()
async def hello(ctx):
    await ctx.send('hello!')

bot.run(token)
