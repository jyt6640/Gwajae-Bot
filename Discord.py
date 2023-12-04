import discord, asyncio

client = discord.Client()

@client.event
async def on_ready():
    print("터미널에서 실행 됨")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("봇의 상태메세지"))
    
@client.event
async def on_message(message):
    if message.content == "테스트":
        await message.channel.send ("{} | {}, hello".format(message.author, message.author.mention))
        await message.author.send ("{} | {}, User, hello".format(message.author, message.author.mention))        
        
    
client.run('MTE4MTE2MjM1MDQxNDQwNTY5NA.GOexcR.P-k1zvn1-b-h9dKlUJzCCulF_Ac3bmLhhYIqEg')    