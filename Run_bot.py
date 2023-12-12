# yt_dlp 모듈에서 YoutubeDL 클래스를 가져옵니다.
from yt_dlp import YoutubeDL
# YoutubeDL 클래스의 인스턴스를 생성하고 설정을 지정합니다.
ydl = YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'})

# 필요한 라이브러리들을 가져옵니다.
import openai, discord, os, re, boto3, asyncio, subprocess, tempfile, nest_asyncio, time, bs4, lxml, aiohttp
import pandas as pd

# Discord 관련 라이브러리들을 가져옵니다.
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import HelpCommand

# Selenium과 관련된 라이브러리들을 가져옵니다.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Discord 유틸리티 함수와 FFmpegPCMAudio 클래스를 가져옵니다.
from discord.utils import get
from discord import FFmpegPCMAudio

# 환경 변수 파일 경로를 설정하고 로드합니다.
dotenv_file_path = r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\토큰.env'
load_dotenv(dotenv_file_path)

# Discord 봇 토큰 및 기타 인증 정보를 환경 변수에서 가져옵니다.
token = os.environ.get('tik')
ai = os.environ.get('ai')
aws_access_key_id = os.environ.get('key')
aws_secret_access_key = os.environ.get('secret')
aws_region = os.environ.get('region')

# Amazon Polly 클라이언트를 생성합니다.
polly_client = boto3.client('polly', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=aws_region)

# FFmpeg 실행 파일 경로를 직접 설정합니다.
ffmpeg_options = {
    'executable': r'C:\Users\admin\Desktop\Jeong\Gwajae-Bot\ffmpeg-6.1-full_build-shared\bin\ffmpeg.exe',
}

# Selenium 설정 (ChromeDriver 기준)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# ChromeDriver를 사용하여 WebDriver 인스턴스를 생성합니다.
driver = webdriver.Chrome(options=chrome_options)

# Discord 봇을 생성합니다.
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = ai

# 음성 채널 연결 변수를 초기화합니다.
vc = None

# Help 명령어를 재정의하는 클래스를 선언합니다.
class MyHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        help_message = "사용 가능한 명령어들을 나열해볼게요:\n"
        for command in self.context.bot.commands:
            if command.name == 'help':
                help_message += f"!{command.name} - 저 또한 어떠한 명령어들이 있는지 보여드려요\n"
            else:
                help_message += f"!{command.name} - {command.help}\n"
        await self.get_destination().send(help_message)

# Help 명령어를 위해 생성한 클래스를 설정합니다.
bot.help_command = MyHelpCommand()

# 사용자 대화 기록을 저장하는 딕셔너리를 초기화합니다.
history = dict()

# YoutubeDL 인스턴스를 초기화하는 함수를 정의합니다.
def __init__(self, client):
    option = {
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
    self.client = client
    self.DL = YoutubeDL(option)

# 사용자 대화 기록을 추가하는 함수를 정의합니다.
def add_history(user: str, prompt: str, bot_answer: str):
    if user not in history:
        history[user] = []
    pair = dict(
        prompt=prompt,
        answer=bot_answer
    )
    history[user] = history[user][-9:] + [pair]

# 사용자 대화 기록을 조회하는 함수를 정의합니다.
def get_history(user: str) -> list:
    return history.get(user, [])

# GPT-3 모델의 답변을 정리하는 함수를 정의합니다.
def clean_bot_answer(answer: str) -> str:
    answer = answer.strip()
    answer = re.sub(r"^(\w.+\:) ", "", answer)
    return answer

# 사용자의 대화를 이전 대화 기록과 함께 반환하는 함수를 정의합니다.
def prompt_to_chat(user: str, prompt: str) -> str:
    previous = get_history(user)
    conversation = ""
    for chat in previous:
        conversation += f"Human: {chat}\nBot:"  # 이전 대화 기록을 가져와 문맥을 생성합니다.
    return conversation

# GPT-3 모델과 대화하는 함수를 정의합니다.
def chat_with_gpt(
    user: str,
    prompt: str,
    max_tokens: int = None,
    use_history: bool = None
) -> str:
    if max_tokens is None:
        max_tokens = 200
    if use_history is None or use_history:
        # 이전 대화 기록을 가져와서 문맥을 만듭니다.
        conversation = prompt_to_chat(user, prompt)
        prompt = conversation + f"\nHuman: {prompt}"
    print('prompt:', prompt)
    bot_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.25
    )
    print('bot response:', bot_response)
    bot_answer = '\n'.join([clean_bot_answer(choice.text) for choice in bot_response.choices])
    add_history(user, prompt, bot_answer)
    return bot_answer

# Discord 봇의 on_ready 이벤트를 처리하는 함수를 정의합니다.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("제발 구현.."))
 
# Discord 봇의 join 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='join', help='봇이 디스코드 방에서 입장합니다.')
async def join(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속해있지 않아요!")


# 봇이 음성 채널에서 퇴장하는 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='leave', help='봇이 디스코드 방에서 퇴장합니다.')
async def leave(ctx):
    try:
        # 음성 채널에서 퇴장
        await vc.disconnect()
    except:
        # 이미 퇴장 상태일 때 예외 처리
        await ctx.send("이미 그 채널에 속해있지 않아요.")

# TTS(Text-to-Speech) 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='tts', help='!tts <이름> <문장> 구조로 입력을 하면 봇이 와서 말해줍니다^^')
async def tts(ctx, voice_name: str, *, text: str):
    # 사용자가 음성 채널에 연결되어 있는지 확인
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("음성 채널에 연결되어 있지 않아요.")
        return

    # 음성 채널에 이미 조인되어 있으면 그대로 사용, 아니면 조인
    voice_channel = ctx.voice_client
    if voice_channel is None or not voice_channel.is_connected():
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

    # Amazon Polly를 통해 텍스트를 음성으로 변환
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_name
    )

    # 임시 파일을 생성하고 음성을 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(response['AudioStream'].read())
        tmp_file_path = tmp_file.name

    # FFmpegPCMAudio를 사용하여 음성 재생
    voice_channel.play(discord.FFmpegPCMAudio(tmp_file_path, **ffmpeg_options))

    # 음성 재생이 끝나기를 기다린 후, 임시 파일 삭제
    while voice_channel.is_playing():
        await asyncio.sleep(1)

    # 임시 파일 삭제
    os.remove(tmp_file_path)

# Polly에서 사용 가능한 목소리들을 조회하는 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='voices', help='사용가능한 목소리들을 보여드릴게요\n(이외에도 !voices moreInfo와 같은 명령어를 입력하시면 더 예시를 보여드려요)')
async def list_polly_voices(ctx, language_code='ko-KR'):
    """List available Polly voices."""
    if language_code.lower() == 'moreinfo':
        await ctx.send("예시: `!voices en-GB`, `!voices es-ES`, `!voices fr-FR`, ...")
    else:
        voices = polly_client.describe_voices(LanguageCode=language_code)['Voices']
        voice_list = '\n'.join([f"{voice['Id']} - {voice['Name']}" for voice in voices])
        await ctx.send(f"Available Polly voices for {language_code}:\n{voice_list}")

# GPT 모델과 대화하는 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='chat', help='GPT 모델과 대화합니다.')
async def chat(ctx, *, prompt: str):
    user = ctx.author
    bot_answer = chat_with_gpt(user.id, prompt)
    await ctx.send(f"> Your prompt is: {prompt}\nAnswer: {bot_answer}")

# 대학교 일정을 조회하는 명령어를 처리하는 함수를 정의합니다.
@bot.command(name='일정', help='대학교 일정을 보여줍니다.')
async def show_schedule(ctx):
    # 대상 웹페이지로 이동
    url = 'https://www.andong.ac.kr/main/board/index.do?menu_idx=68&manage_idx=1&search.category1=102'
    driver.get(url)

    # 웹페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 정보 추출
    infos = soup.select('tr')[1:]
    data = []
    for info in infos:
        title = info.select('a > span')[0].text
        date_tag = info.select('td.date')
        date = date_tag[0].text
        data.append({'title': title, 'date': date})

    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # 날짜를 기준으로 정렬
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d', errors='coerce')
    df = df.sort_values(by='date')

    # 중복 일정 제거
    df = df.drop_duplicates()

    # 일정 정보를 텍스트로 변환
    schedule_text = df.to_string(index=False)

    # Discord에 일정 정보 전송 (여러 메시지로 나누어 보내기)
    for row in df.itertuples(index=False):
        # Discord Embed으로 감싸서 출력, strftime 메서드를 사용하여 날짜 포맷을 지정
        embed = discord.Embed(title=row.date.strftime('%Y-%m-%d'), description=row.title.strip(), color=0x00ff00)
        await ctx.send(embed=embed)

# Nest Asyncio 적용
nest_asyncio.apply()

# 노래 재생을 처리하는 명령어를 정의합니다.
@bot.command(name='노래재생', help='노래를 재생합니다.')
async def 노래재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    FFMPEG_OPTIONS['executable'] = ffmpeg_options['executable']
    
    # 봇이 음성 채널에 조인되어 있는지 확인
    if not ctx.voice_client:
        # 봇이 음성 채널에 조인되어 있지 않으면 조인
        try:
            channel = ctx.author.voice.channel
            ctx.voice_client = await channel.connect()
        except AttributeError:
            await ctx.send("음성 채널에 조인할 수 없습니다.")
            return

    if not ctx.voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        ctx.voice_client.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed=discord.Embed(title="노래 재생", description=f"현재 {url} 을(를) 재생하고 있습니다.", color=0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")

# 음악 재생을 처리하는 명령어를 정의합니다.
@bot.command(name="음악재생", help='음악을 재생합니다.')
async def play_music(ctx, url=None):
    if url is None:
        # URL이 입력되지 않았을 때의 처리
        embed = discord.Embed(title='오류 발생', description='음악 재생을 위한 URL을 제공해주세요!', color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    # 봇의 음성 채널 연결이 없으면
    if ctx.voice_client is None: 
        # 명령어(ctx) 작성자(author)의 음성 채널에 연결 상태(voice)
        if ctx.author.voice:
            # 봇을 명령어 작성자가 연결되어 있는 음성 채널에 연결
            await ctx.author.voice.channel.connect()
        else:
            embed = discord.Embed(title='오류 발생', description='음성 채널에 들어간 후 명령어를 사용 해 주세요!', color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("Author not connected to a voice channel.")
    
    # 봇이 음성 채널에 연결되어 있고, 재생중이라면
    elif ctx.voice_client.is_playing():
        # 현재 재생중인 음원을 종료
        ctx.voice_client.stop()
    
    await ctx.send(url)
    
    # 음악 재생을 위한 정보 추출 및 재생
    data = ydl.extract_info(url, download=False)
    link = data['url']
    title = data['title']

    ffmpeg_options = {
        'options': '-vn',
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    }
    player = discord.FFmpegPCMAudio(link, **ffmpeg_options, executable=r"C:\Users\admin\Desktop\Jeong\Gwajae-Bot\chromedriver-win64\chromedriver.exe")
    ctx.voice_client.play(player)

    embed = discord.Embed(title='음악 재생', description=f'{title} 재생을 시작힐게요!', color=discord.Color.blue())
    await ctx.send(embed=embed)

# 봇 실행
bot.run(token)
