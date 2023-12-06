import openai
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

dotenv_file_path = r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\토큰.env'
load_dotenv(dotenv_file_path)

token = os.environ.get('tik')
ai = os.environ.get('ai')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='$', intents=intents)
openai.api_key = ai

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    print(message)

    if message.author == bot.user:
        return
    text = message.content
    if text.startswith('!chat'):
        prompt = text[6:]
        bot_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        print('bot response:', bot_response)
        bot_text = bot_response['choices'][0]['text']
        await message.channel.send(f"> Your prompt is: {prompt}\nAnswer: {bot_text}")

@bot.command()
async def hello(ctx):
    await ctx.send('hello!')

bot.run(token)
