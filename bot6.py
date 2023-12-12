#라이브러리 및 모듈 임포트
import openai
import discord
import os
import re
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import HelpCommand
import boto3
import asyncio
import subprocess
import tempfile

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

#딕셔너리를 이용한 
history = dict()

def add_history(user: str, text: str):
    if user not in history:
        history[user] = []
    history[user].append(text)
    
def get_history(user: str) -> list:
    return history.get(user, [])  # 사용자가 없을 경우 빈 리스트 반환
    

#봇 이벤트 설정
@bot.event 
async def on_ready():  # 봇이 실행 될 때
    print(f'We have logged in as {bot.user}')  # 봇을 실행시 출력창에 출력

# OpenAi와 상호작용 (!chat 질문 형식으로 질의)
@bot.event
async def on_message(message):
    user = message.author
    if user == bot.user:
        return
    
    text = message.content

    if text.startswith('!chat'):  # 명령어
        prompt = text[6:]
        bot_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        add_history(user.id, prompt)  # 사용자를 사용자 식별자로 사용

        print('bot response:', bot_response)
        bot_text = bot_response['choices'][0]['text']
        await message.channel.send(f"> Your prompt is: {prompt}\nAnswer: {bot_text}")  # 출력 양식

    else:  # 직접 메시지를 입력한 경우
        # 직접 메시지에 대한 처리를 여기에 추가
        pass

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send('hello!')

bot.run(token)
