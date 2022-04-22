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
from feature.help import Dhelp, DhelpStuff, card
from feature.profile import Dprofile, seeprofile, give
from feature.create import compiledesmython
from feature.module import Dmodule, DmoduleStuff, desmodule

print(db.keys())
token = os.environ.get("DISCORD_BOT_SECRET")

@client.event
async def on_ready():
  await Onready()

@client.event
async def on_raw_reaction_add(payload):
  from setup import banned
  emoji=payload.emoji
  user=payload.member
  messageid=payload.message_id
  channelid=payload.channel_id
  channel0 = client.get_channel(channelid)
  message0 = await channel0.fetch_message(messageid)
  if user.id==client.user.id or user.id in banned:
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
  import setup
  from setup import banned
  pattern=re.compile(r"!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?")
  x=pattern.finditer(message.content)
  pattern02=re.compile(r"!<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?")
  x02=pattern02.finditer(message.content)
  pattern03=re.compile(r"(!graph ([^?]+)(?: *\?(?:(x|y|size)(?:=(\[.*?,.*?\])))(?:&(x|y|size)(?:=(\[.*?,.*?\])))?(?:&(x|y|size)(?:=(\[.*?,.*?\])))?)?)")
  x03=pattern03.finditer(message.content)
  pattern04=re.compile(r"!\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))(?: vs \/((?:[a-z0-9]{20})|(?:[a-z0-9]{10})))?")
  x04=pattern04.finditer(message.content)
  pattern05=re.compile(r'!dhelp\n\[([,A-Za-z0-9 ]+)\](?:\?image=(.+))?\n([\s\S]+)')
  x05=pattern05.finditer(message.content)
  pattern06=re.compile(r'!dhelp ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
  x06=pattern06.finditer(message.content)
  pattern07=re.compile(r'card!([0-9]+)')
  x07=pattern07.finditer(message.content)
  pattern08=re.compile(r'!profile +"([A-Za-z0-9]+)"(?:\?image=(.+))?(?:\n([\s\S]*))?')
  x08=pattern08.finditer(message.content)
  pattern09=re.compile(r'!profile +([0-9]+|<@!?[0-9]+>)')
  x09=pattern09.finditer(message.content)
  pattern10=re.compile(r'!give +([0-9]+) +to +([0-9,<>!@ ]+)')
  x10=pattern10.finditer(message.content)
  pattern11=re.compile(r'!create *(?:"([A-Za-z0-9 \[\]]+)"(\?[a-z0-9]{10})?)?(?:\n\[!(.*)\])?\n+```.*\n(?:import +([A-Za-z0-9\.\,! ]+) +as +([A-Za-z0-9\, ]+)\n)?([\s\S]*?)\n?```')
  x11=pattern11.finditer(message.content)
  #
  mpattern05=re.compile(r'!module +"([A-Za-z0-9]+)"\n\[([,A-Za-z0-9 ]+)\]\n<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?\n([\s\S]+)')
  mx05=mpattern05.finditer(message.content)
  mpattern06=re.compile(r'!module ([a-zA-Z0-9\. ]{3,}|\/.*?\/)')
  mx06=mpattern06.finditer(message.content)
  mpattern07=re.compile(r'desmodule!([0-9]+)')
  mx07=mpattern07.finditer(message.content)

  if getattr(message.channel,"category_id",None)==948463189346119710 or setup.setup==True:
    return
  elif message.author == client.user or message.author.bot or message.guild is None or message.author.id in banned:
    if len(list(x10))==1 and message.content.startswith("!give") and message.author == client.user:
      await give(message)
    else:
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
    helpembed=nextcord.Embed(title="Commands",description="\"{enter parameter value}\" omit the `{`,`}`\n\"?parameter\" in command is optional")
    helpembed.add_field(name="README/Manual", value='➡️ https://mathenthusiastpi.gitbook.io/desmobot/ ⬅️', inline=False)
    helpembed.add_field(name="Search", value='```!desmos {search term}?owner={search term for author}&title={search term for title}&hash={search term for hash}```\n\"={sub-search term}\" can be ommitted', inline=False)
    helpembed.add_field(name="Graph info.", value='```!{graph link}```', inline=True)
    helpembed.add_field(name="Compare graphs", value='```!/{graph hash1} vs /{graph hash2}```', inline=True)
    helpembed.add_field(name="Create/View profile", value='*Create:*```!profile "{nickname}"?image={profile image url}\n{description}```\n*View:*```!profile {@mention or user-id}```', inline=False)
    helpembed.add_field(name="Create Dhelp cards", value='```!dhelp\n[{list of keywords}]?image={image url}\n{description (markdown allowed)}```', inline=False)
    helpembed.add_field(name="Search Dhelp cards", value='```!dhelp {search term}```', inline=True)
    helpembed.add_field(name="View Dhelp cards", value='```card!{dhelp-card-id}``` Example: card!959614757776801802', inline=True)
    helpembed.add_field(name="Create Desmodule", value='```!module "{module name}"\n[{list of keywords}]\n{desmos graph link}\n{description (markdown allowed)}```', inline=False)
    helpembed.add_field(name="Search Modules", value='```!module {search term}```', inline=True)
    helpembed.add_field(name="View Desmodule cards", value='```desmodule!{desmodule-card-id}``` Example: desmodule!959613976046620672', inline=True)
    helpembed.add_field(name="Bulk Contribute/Set owner of a graph", value='```!contribute {list of graph hashes}?owner={author name}```', inline=False)
    helpembed.add_field(name="Quick Graph f(x)", value='```!graph {some f(x) function}```', inline=True)
    helpembed.add_field(name="Create Desmos Graph", value='```!create```\nSee README to learn more about !create', inline=True)
    helpembed.add_field(name="README/Manual", value='➡️ https://mathenthusiastpi.gitbook.io/desmobot/ ⬅️', inline=False)
    helpembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    await message.channel.send(embed=helpembed,content='DM me for desmos/bot related help:)\n\u200B')
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
  elif len(list(x07))==1:
    await card(message,[ii.group(1) for ii in pattern07.finditer(message.content)][0])
  elif message.content=='!profile':
    message.content='!profile '+str(message.author.id)
    await seeprofile(message)
  elif len(list(x09))==1 and message.content.startswith("!profile"):
    await seeprofile(message)
  elif len(list(x08))==1 and message.content.startswith("!profile"):
    await Dprofile(message)
  elif len(list(x10))==1 and message.content.startswith("!give"):
    await give(message)
  elif len(list(x11))==1 and message.content.startswith("!create"):
    print('Createe')
    await compiledesmython(message.content,message)
    ###
  elif len(list(mx05))==1 and message.content.startswith("!module"):
    await Dmodule(message)
  elif len(list(mx06))==1:
    await DmoduleStuff(message)
  elif len(list(mx07))==1:
    await desmodule(message,[ii.group(1) for ii in mpattern07.finditer(message.content)][0])

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

from feature.recGraph import OnMessageG
@client.listen()
async def on_message(message):
  await OnMessageG(message)

@client.listen()
async def on_message(message):
  if message.channel.id==959631837980925993:
    from setup import bannedU
    await bannedU()

@client.event
async def on_member_join(member):
  if member.guild.id==931036887693533204:
    embed=nextcord.Embed(title="<a:m_welcome1:932191399087046687><a:m_welcome2:932191456846819398> to "+member.guild.name+'!',description='Enjoy your stay here.')
    ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
    print(member.guild.member_count)
    embed.set_author(name=ordinal(member.guild.member_count+1)+' member')
    embed.add_field(name="Read the rules and verify!", value='<#931036888196845649>', inline=False)
    embed.add_field(name="Claim roles!", value='<#931410233232871484>', inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    channelW = client.get_channel(931048065601785896)
    await channelW.send(content=member.mention,embed=embed)

keep_alive()
client.run(token)