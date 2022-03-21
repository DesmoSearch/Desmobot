import nextcord
import random
from nextcord.ext import commands
from nextcord import DMChannel
from replit import db
gifsG=[]
usersG=[]
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="_",intents=intents)
setup = True
#
dhelplist=[]
dpfplist=[]

async def Onready():
  await client.change_presence(activity=nextcord.Game(name=f"on {len(client.guilds)} servers | {db['searches']} searches done!"))
  global setup
  if setup:
    await setuploading()
    await setupDhelp()
    await setupDpfp()
    setup=False

async def loadinggif(msg0):
  selectR=random.randint(0,len(gifsG)-1)
  user = await client.fetch_user(str(usersG[selectR]))
  embed=nextcord.Embed(title='Loading...') 
  embed.set_author(name='Gif by '+str(user), icon_url=user.display_avatar.url)
  embed.set_image(url=gifsG[selectR])
  embed.set_footer(text='Shared in #looping-gifs in the https://dsc.gg/me314 discord server')
  return embed

async def setuploading():
  channelG = client.get_channel(948482596197777442)
  async for msgG in channelG.history(limit=10000):
    C=(msgG.content.replace(" ", "")).split(",")
    gifsG.extend(C[1::2])
    usersG.extend(C[0::2])

async def getready(message):
  db['searches']=db['searches']+1
  await Onready()
  await dmsend(repr(message)+"\n\n"+message.content)
  return await loadinggif(message)

async def dmsend(msg):
    user = await client.fetch_user("686012491607572515")
    await DMChannel.send(user,"```"+msg+"```")

async def record(msg0,msg1=''):
  if msg1 == '':
    channel = client.get_channel(950332971842404382)
    return await channel.send(content='content: '+str(msg0.content)+'\nauthor: '+str(msg0.author)+';'+str(msg0.author.id)+'\nid: '+str(msg0.channel.id)+';'+str(msg0.id),embed=(msg0.embeds[0]) if msg0.embeds else None,files=[await f.to_file() for f in msg0.attachments])
  else:
    if (msg1.channel.id==950332971842404382):
      channel001 = client.get_channel(950332992079925288)
      msg01 = await channel001.send(msg1.jump_url)
      msg1=await msg1.edit(content=msg1.content+'\n'+msg01.jump_url)
      msg1=msg01
    return await msg1.reply(content='content: '+str(msg0.content)+'\nauthor: '+str(msg0.author)+';'+str(msg0.author.id)+'\nid: '+str(msg0.channel.id)+';'+str(msg0.id),embed=(msg0.embeds[0]) if msg0.embeds else None,files=[await f.to_file() for f in msg0.attachments])

import json
async def setupDhelp():
  global dhelplist
  dhelplist=[]
  channel=client.get_channel(954961640183455804)
  async for msgg in channel.history(limit=10000):
    dhelplist.append((json.loads(msgg.embeds[0].fields[0].value.replace('\'', '\"')),msgg.embeds[0],msgg.content))

async def setupDpfp():
  global dpfplist
  dpfplist=[]
  channel=client.get_channel(950550255789830164)
  async for msgg in channel.history(limit=10000):
    dpfplist.append((msgg.id,int(msgg.embeds[0].footer.text),msgg.embeds[0].title))