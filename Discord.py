import discord
from discord.ext import commands, tasks

intents = discord.Intents.all()
intents.messages = True  # 이 부분을 추가

client = discord.Client(intents=intents)

@client.event
async def on_ready(): #봇이 실행되면 한번 실행됨
    print("터미널에서 실행 됨") #
    await client.change_presence(status=discord.Status.online, activity=discord.Game("과제"))

@client.event
async def on_message(message):
    if message.content == "테스트": #메세지 감지
        await message.channel.send("{} | {}, hello".format(message.author, message.author.mention)) #서버에 인사를 보냄
        await message.author.send("{} | {}, User, hello".format(message.author, message.author.mention)) #개인 메세지로 인사를 보냄

#봇을 실행시키기 위한 토큰을 작성해주는 곳
client.run('MTE4MTE2MjM1MDQxNDQwNTY5NA.Gh1bba.LdDajaB8F3B3laB5o6NWxQWJzAtum42Gf8vAZY')
