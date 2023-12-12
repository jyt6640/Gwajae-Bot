import discord
from discord.ext import commands
from discord.ext.commands import HelpCommand
import boto3
import asyncio
import subprocess
import os
import tempfile

# Discord 봇 토큰 입력
TOKEN = 'MTE4MTE2MjM1MDQxNDQwNTY5NA.GP1CGu.w3kXvloEgAhx5tBr8WrPtBXGrFekgMft8m8NIc'

# AWS 계정 및 리전 설정
aws_access_key_id = 'AKIAWEBICXRRJLGMY2ZF'
aws_secret_access_key = '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'
aws_region = 'ap-northeast-2'

# Amazon Polly 클라이언트 생성
polly_client = boto3.client('polly', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=aws_region)

# FFmpeg 경로를 직접 설정
ffmpeg_options = {
    'executable': r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\ffmpeg-6.1-full_build-shared\bin\ffmpeg.exe',
}


# 봇 객체 생성 및 Intents 설정
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class MyHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        help_message = "사용가능하신 명령어들을 나열해볼게요:\n"
        for command in self.context.bot.commands:
            if command.name == 'help':
                help_message += f"!{command.name} - 저 또한 어떠한 명령어들이 있는지 보여드려요\n"
            else:
                help_message += f"!{command.name} - {command.help}\n"
        await self.get_destination().send(help_message)
        await self.get_destination().send("\nTTS에 뭔가 부족한 것 같다에 대한 피드백 내용은 Aseol1104@gmail.com으로 메일을 보내주세요^^")

bot.help_command = MyHelpCommand()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("직무유기"))

# @bot.command(name='commands', help='어떠한 명령어들이 있는지 보여드릴게요')
# async def show_help(ctx):
#     """Show a list of available commands."""
#     help_message = "사용가능하신 명령어들을 나열해볼게요:\n"
#     for command in bot.commands:
#         help_message += f"!{command.name} - {command.help}\n"
#     await ctx.send(help_message)


@bot.command(name='join')
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_channel = ctx.voice_client

    if voice_channel and voice_channel.is_connected():
        await voice_channel.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f'봇이 {channel} 채널에 연결되었습니다.')

@bot.command(name='leave')
async def leave(ctx):
    voice_channel = ctx.voice_client

    if voice_channel and voice_channel.is_connected():
        await voice_channel.disconnect()
        await ctx.send(f'봇이 음성 채널에서 나갔습니다.')
    else:
        await ctx.send('봇이 현재 음성 채널에 연결되어 있지 않습니다.')
        
@bot.command(name='tts', help='!tts <이름> <문장> 구조로 입력을 하면 봇이 와서 말해줍니다^^')
async def tts(ctx, voice_name: str, *, text: str):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    # Voice Channel에 조인
    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    # Amazon Polly를 통해 텍스트를 음성으로 변환
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_name
    )

    # Create a temporary file to store the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(response['AudioStream'].read())
        tmp_file_path = tmp_file.name

    # Play the audio using FFmpegPCMAudio
    voice_channel.play(discord.FFmpegPCMAudio(tmp_file_path, **ffmpeg_options))


    # 음성 재생이 끝나기를 기다린 후, Voice Channel에서 나가기
    while voice_channel.is_playing():
        await asyncio.sleep(1)
    await voice_channel.disconnect()

    # Delete the temporary file
    os.remove(tmp_file_path)

@bot.command(name='voices', help='사용가능한 목소리들을 보여드릴게요\n(이외에도 !voices moreInfo와 같은 명령어를 입력하시면 더 예시를 보여드려요)')
async def list_polly_voices(ctx, language_code='ko-KR'):
    """List available Polly voices."""
    if language_code.lower() == 'moreinfo':
        await ctx.send("예시: `!voices en-GB`, `!voices es-ES`, `!voices fr-FR`, ...")
    else:
        voices = polly_client.describe_voices(LanguageCode=language_code)['Voices']
        voice_list = '\n'.join([f"{voice['Id']} - {voice['Name']}" for voice in voices])
        await ctx.send(f"Available Polly voices for {language_code}:\n{voice_list}")

# 봇 실행
bot.run(TOKEN)
