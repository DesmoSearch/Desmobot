from keep_alive import keep_alive
import nextcord
import os
import re
from replit import db
from setup import Onready, getready, client, record
from feature.DMS import DMrec, DMreact
from feature.Graph import GraphStuff
from feature.Comparison import DiffStuff
from feature.about import onmessage1,onmessage2,expandG
from feature.help import Dhelp, DhelpStuff

print(db.keys())
token = os.environ.get("DISCORD_BOT_SECRET")

@client.event
async def on_ready():
  await Onready()

@client.event
async def on_raw_reaction_add(payload):
  emoji=payload.emoji
  user=payload.member
  messageid=payload.message_id
  channelid=payload.channel_id
  channel0 = client.get_channel(channelid)
  message0 = await channel0.fetch_message(messageid)
  if user.id==client.user.id:
    return
  elif emoji.name=='✅' and user.id==686012491607572515 and channelid==945245411449372702:
    def combine(gifs0,users0):
      result = [None]*(len(gifs0)+len(users0))
      result[1::2]=gifs0
      result[0::2]=users0
      return(' , '.join(result))
    channel = client.get_channel(948482596197777442)
    gifs=[]
    users=[]
    async for msg in channel.history(limit=1):
      damsg=msg
      C=(msg.content.replace(" ", "")).split(",")
      gifs.extend(C[1::2])
      users.extend(C[0::2])
    ###
    pattern=re.compile(r"((http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png))")
    gifs2=([mm.url for mm in message0.attachments]+[ii.group(1) for ii in pattern.finditer(message0.content)])
    users2=[str(message0.author.id) for i in range(len(gifs2))]
    if len(combine(gifs+gifs2,users+users2))<2000 and damsg.author.id==944269890301345884:
      damsg=await damsg.edit(content=combine(gifs+gifs2,users+users2))
    else:
      await channel.send(content=combine(gifs2,users2))

  elif emoji.name=='🔭':
    await expandG(emoji,user,messageid,channelid,channel0,message0)
  elif channelid in [950332971842404382,950332992079925288]:
    contentarray=(re.sub('\nhttps:\/\/discord.com\/channels\/[0-9]+\/[0-9]+\/[0-9]+','',message0.content)).split('\n')
    content=('\n'.join(contentarray[0:-2]))[9:]
    author=contentarray[-2:-1][0][8:].split(';')
    Mid=contentarray[-1:][0][4:].split(';')
    Mchannel0 = client.get_channel(int(Mid[0]))
    Mid0 = await Mchannel0.fetch_message(int(Mid[1]))
    if emoji.name=='❌':
      await Mid0.delete()
      await message0.add_reaction('❌')
  elif emoji.name=='🔬':
    patternhh=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
    xhh=patternhh.finditer(message0.content)
    if len(list(xhh))>=1:
      thehashhh=[ii.group(1) for ii in patternhh.finditer(message0.content)][0]
      message0.content='!/'+thehashhh
      message0.author=user
      await DiffStuff(message0,True)
      
    


@client.event
async def on_message(message): 
  pattern=re.compile(r"!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?")
  x=pattern.finditer(message.content)
  pattern02=re.compile(r"!<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?")
  x02=pattern02.finditer(message.content)
  pattern03=re.compile(r"(!graph ([^?]+)(?: *\?(?:(x|y|size)(?:=(\[.*?,.*?\]))?)(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?)?)")
  x03=pattern03.finditer(message.content)
  pattern04=re.compile(r"!\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))(?: vs \/((?:[a-z0-9]{20})|(?:[a-z0-9]{10})))?")
  x04=pattern04.finditer(message.content)
  pattern05=re.compile(r'!dhelp\n\[([,A-Za-z0-9 ]+)\](?:\?image=(.+))?\n([\s\S]+)')
  x05=pattern05.finditer(message.content)
  pattern06=re.compile(r'!dhelp ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
  x06=pattern06.finditer(message.content)
  if message.author == client.user or message.author.bot:
    return
  elif len(list(x))==1:
    await onmessage1(message)
  elif len(list(x02))==1:
    await onmessage2(message)
  elif message.content=="!dhelp":
    #
    await getready(message)
    RecMsg = await record(message)
    #
    helpembed=nextcord.Embed(title="Commands",description="!dhelp, !desmos, ![+desmoslink], !/graph hash vs /graph hash")
    helpembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    await message.channel.send(embed=helpembed,content='')
  elif len(list(x03))==1:
    await GraphStuff(message)
  elif message.content=="!loading":
    await message.channel.send(embed=await getready(message))
  elif message.content=="sauce?":
    await message.channel.send('https://cdn.discordapp.com/attachments/709918138342572093/948783164518699078/bernie.png')
  elif len(list(x04))==1:
    await DiffStuff(message)
  elif len(list(x05))==1 and message.content.startswith("!dhelp"):
    await Dhelp(message)
  elif len(list(x06))==1:
    await DhelpStuff(message)

@client.listen()
async def on_message(msg):
  await DMrec(msg,client)

@client.listen()
async def on_raw_reaction_add(payload):
  emoji=payload.emoji
  user=await client.fetch_user(payload.user_id)
  messageid=payload.message_id
  channelid=payload.channel_id
  channel0 = client.get_channel(channelid)
  message0=''
  if payload.guild_id is None:
    message0 = await user.fetch_message(messageid)
  else:
    message0 = await channel0.fetch_message(messageid)
  await DMreact(emoji,user,message0,client,True)

@client.listen()
async def on_raw_reaction_remove(payload):
  emoji=payload.emoji
  user=await client.fetch_user(payload.user_id)
  messageid=payload.message_id
  channelid=payload.channel_id
  channel0 = client.get_channel(channelid)
  message0=''
  if payload.guild_id is None:
    message0 = await user.fetch_message(messageid)
  else:
    message0 = await channel0.fetch_message(messageid)
  await DMreact(emoji,user,message0,client,False)

keep_alive()
client.run(token)