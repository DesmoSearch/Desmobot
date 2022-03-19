import nextcord
import re
import math
import asyncio
from setup import getready, client, record, dhelplistupdate
from Variables import noofresults
pattern05=re.compile(r'!dhelp\n\[([,A-Za-z0-9 ]+)\](?:\?image=(.+))?\n([\s\S]+)')
Dhelpchannel=954531626434560048

async def Dhelp(message):
  #
  await getready(message)
  RecMsg = await record(message)
  #
  keywords=re.split(' ?, ?',[ii.group(1) for ii in pattern05.finditer(message.content)][0])
  Description=[ii.group(3) for ii in pattern05.finditer(message.content)][0]
  Image=[ii.group(2) for ii in pattern05.finditer(message.content)][0]
  if len(Description)<1000:
    dhelpembed=nextcord.Embed(title="!dhelp",description=Description)
    dhelpembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    dhelpembed.add_field(name="Keywords", value=str(keywords), inline=False)
    dhelpembed.set_thumbnail(url=Image if Image is not None else '')
    des=''
    if 'Direct Message' in str(message.channel):
      des=str(message.author.id)+'|'+str(message.id)
    else:
      des=str(message.channel.id)+';'+str(message.id)
    channel = client.get_channel(Dhelpchannel)
    message0=await channel.send(content=des,embed=dhelpembed)
    await message.edit(suppress=True)
    await message.channel.send(embed=dhelpembed)
    await message0.add_reaction('✅')

async def Dhelpreact(emoji,user,message,client,addStatus):
  if user.id==686012491607572515 and message.channel.id==Dhelpchannel:
    if ';' in message.content:
      channel0 = client.get_channel(int(message.content.split(';')[0]))
      message0 = await channel0.fetch_message(int(message.content.split(';')[1]))
      if addStatus:
        await message0.add_reaction(emoji)
      else:
        await message0.remove_reaction(emoji,client.user)
    elif '|' in message.content:
      msgIDget=message.content.split('|')[1]
      user00 = await client.fetch_user(message.content.split('|')[0])
      message0 = await user00.fetch_message(msgIDget)
      if addStatus:
        await message0.add_reaction(emoji)
      else:
        await message0.remove_reaction(emoji,client.user)
    await dhelplistupdate()

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
  await Dhelpreact(emoji,user,message0,client,True)

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
  await Dhelpreact(emoji,user,message0,client,False)

async def DhelpStuff(message):
  from setup import dhelplist
  pattern06=re.compile(r'!dhelp ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
  #
  msg4 = await message.channel.send(embed=await getready(message))
  RecMsg = await record(message)
  #
  async with message.channel.typing():
    searchterm=[ii.group(1) for ii in pattern06.finditer(message.content)][0]
    
    slashcheckterm=False
    if "/" in searchterm:
      searchterm=searchterm[1:-1]
      slashcheckterm=True
    else:
      searchterm=searchterm.lower()
    searchtermpart = lambda data00 : data00 if slashcheckterm else data00.lower()
    searchterm0 = searchtermpart(searchterm)
    searchresult4=[tup for tup in dhelplist if any([bool(re.search(searchterm0, searchtermpart(str(ele)))) for ele in tup[0]])]

  max_page4=math.ceil(len(searchresult4)/noofresults)
  first_run4 = True
  num4 = 1
  Gnum4 = 1
  GnumDisplay = 0
  infocard=0
  while True:
    if first_run4:
        first_run4 = False
        msg4=await msg4.edit(embed=dhelpembed(-1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
  
    reactmoji4 = []
    if max_page4 == 1 and num4 == 1:
        pass
    elif num4 == 1:
        reactmoji4.append('⏩')
    elif num4 == max_page4:
        reactmoji4.append('⏪')
    elif num4 > 1 and num4 < max_page4:
        reactmoji4.extend(['⏪', '⏩'])
  
    if len(searchresult4) == 0 and Gnum4 == 1:
        pass
    elif not (Gnum4>=len(searchresult4)):
        reactmoji4.append('🔽')
    elif Gnum4 == len(searchresult4) :
        reactmoji4.append('🔼')
    elif Gnum4 > 1 and Gnum4<len(searchresult4):
        reactmoji4.extend(['🔼', '🔽'])
    if GnumDisplay==1:
      reactmoji4.append('🔎')
    reactmoji4.append('✅')
    if str(message.author.id)=='686012491607572515':
       reactmoji4.append('❌')
  
    for react in reactmoji4:
        await msg4.add_reaction(react)
  
    def check_react(reaction, user):
        if reaction.message.id != msg4.id:
            return False
        if user != message.author:
            return False
        if str(reaction.emoji) not in reactmoji4:
            return False
        return True
  
    try:
        res4, user4 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
    except asyncio.TimeoutError:
        return await msg4.clear_reactions()
    if user4 != message.author:
        pass
    elif '⏪' in str(res4.emoji):
        num4 = num4 - 1
        Gnum4 = (num4-1)*noofresults+1
        GnumDisplay = 0
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dhelpembed(-1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '⏩' in str(res4.emoji):
        num4 = num4 + 1
        Gnum4 = (num4-1)*noofresults+1
        GnumDisplay = 0
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dhelpembed(-1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '🔽' in str(res4.emoji):
        Gnum4  = Gnum4 if GnumDisplay==0 else Gnum4+1
        num4 = math.ceil(Gnum4/noofresults)
        GnumDisplay = 1
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dhelpembed(Gnum4,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '🔼' in str(res4.emoji):
        Gnum4  = Gnum4 if GnumDisplay==0 else Gnum4-1
        num4 = math.ceil(Gnum4/noofresults)
        GnumDisplay = 1
        if (num4==0):
          num4 = 1
          Gnum4 = 1
          GnumDisplay = 0
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dhelpembed(Gnum4 if GnumDisplay == 1 else -1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '🔎' in str(res4.emoji):
      infocard=1-infocard
      await msg4.clear_reactions()
      if infocard==0:
        msg4=await msg4.edit(embed=dhelpembed(Gnum4 if GnumDisplay == 1 else -1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '✅' in str(res4.emoji):
        return await msg4.clear_reactions()
    elif '❌' in str(res4.emoji):
        await message.delete()
        return await msg4.delete()
    if infocard==1:
      msg4=await msg4.edit(embed=dhelpembed(Gnum4,num4,searchresult4,max_page4,message,True))
      RecMsg = await record(msg4,RecMsg)

def dhelpembed(Gnum,num,result,max_page,message,infocard=False):
  datahashes=result[noofresults*(num-1):noofresults*num+1]
  n1='\n'
  thedescription="".join(f'{"⇓⇓⇓"+n1+"> " if Gnum==(num-1)*noofresults+i+1 else ""}{(num-1)*noofresults+i+1}. {" ".join(datahashes[i][1].description.split()[:10])} ...\n'for i in range(len(datahashes)))
  
  pattern06=re.compile(r'!dhelp ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
  searchterm=[ii2.group(1) for ii2 in pattern06.finditer(message.content)][0]
  embed=''
  if not infocard:
    embed = nextcord.Embed(color=0x12793e, title=str(len(result))+" results for \""+searchterm+"\"",description=thedescription)
    embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    embed.set_footer(text="Page: "+str(num)+"/"+str(max_page))
  if Gnum!=-1 and infocard:
    embed=result[Gnum-1][1]
    embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
    embed.set_footer(text=ordinal(Gnum)+" result for \""+searchterm+"\"")
    
  return embed