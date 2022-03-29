import nextcord
import re
import math
import asyncio
from setup import getready, client, record, setupDmodule
from Variables import noofresults
pattern05=re.compile(r'!module +"([A-Za-z0-9]+)"\n\[([,A-Za-z0-9 ]+)\]\n<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?\n([\s\S]+)')
Dmodulechannel=958219332922515476

async def Dmodule(message):
  from setup import dpfplist, dmodulelist
  nickname=[ele[2] for ele in dpfplist if ele[1]==message.author.id]
  if re.fullmatch('[A-Za-z0-9]+', str(nickname[0])) if 0<len(nickname) else False:
    #
    await getready(message)
    RecMsg = await record(message)
    #
    keywords=re.split(' *, *',[ii.group(2) for ii in pattern05.finditer(message.content)][0])
    Description=[ii.group(4) for ii in pattern05.finditer(message.content)][0]
    Name=[ii.group(1) for ii in pattern05.finditer(message.content)][0]
    Graph=[ii.group(3) for ii in pattern05.finditer(message.content)][0]
    
    if len(Description)<4000 and str(Name) not in [(ele[3])[ele[3].index('.')+1:] for ele in dmodulelist if ele[4]==message.author.id]:
      dmoduleembed=nextcord.Embed(title="!module",description=Description)
      dmoduleembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
      dmoduleembed.add_field(name="Desmodule", value='https://www.desmos.com/calculator/'+str(Graph), inline=False)
      dmoduleembed.add_field(name="Module name", value=str(Name), inline=False)
      dmoduleembed.add_field(name="Keywords", value=str(keywords), inline=False)
      dmoduleembed.set_footer(text=str(message.author.id))
      
      des=''
      if 'Direct Message' in str(message.channel):
        des=str(message.author.id)+'|'+str(message.id)
      else:
        des=str(message.channel.id)+';'+str(message.id)
      channel = client.get_channel(Dmodulechannel)
      message0=await channel.send(content=des,embed=dmoduleembed)
      await message.edit(suppress=True)
      await message.channel.send(embed=dmoduleembed)
      await message0.add_reaction('✅')
    elif str(Name) in [(ele[3])[ele[3].index('.')+1:] for ele in dmodulelist if ele[4]==message.author.id]:
      await message.reply(str(nickname[0])+'.'+str(Name)+" module already exists. Try a unique name.")
  else:
    await message.reply("First create a profile using !profile and try again.")

async def Dmodulereact(emoji,user,message,client,addStatus):
  if user.id==686012491607572515 and message.channel.id==Dmodulechannel:
    firstline=message.content.split('\n')[0]
    approve=client.get_channel(952361570317529140)
    if ';' in message.content:
      channel0 = client.get_channel(int(firstline.split(';')[0]))
      message0 = await channel0.fetch_message(int(firstline.split(';')[1]))
      if addStatus:
        await message0.add_reaction(emoji)
      else:
        await message0.remove_reaction(emoji,client.user)
    elif '|' in message.content:
      msgIDget=firstline.split('|')[1]
      user00 = await client.fetch_user(firstline.split('|')[0])
      message0 = await user00.fetch_message(msgIDget)
      if addStatus:
        await message0.add_reaction(emoji)
      else:
        await message0.remove_reaction(emoji,client.user)
    if emoji.name=='✅' and ('|' in message.content or ';' in message.content):
      if addStatus:
        appmsg=await approve.send(embed=message.embeds[0])
        await appmsg.edit(content='desmodule!'+str(appmsg.id))
        await message.edit(content=message.content+'\n'+appmsg.jump_url)
      else:
        link=message.content.split('\n')[1]
        delmsg=await approve.fetch_message(int(link.split('/')[-1]))
        await delmsg.delete()
        await message.edit(content=firstline)
        
    await setupDmodule()

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
  await Dmodulereact(emoji,user,message0,client,True)

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
  await Dmodulereact(emoji,user,message0,client,False)

async def DmoduleStuff(message):
  from setup import dmodulelist
  pattern06=re.compile(r'!module ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
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

    searchterm0 = [searchterm0] if slashcheckterm else re.split(' +',searchterm0)
    searchresult4=[tup for tup in dmodulelist if any([bool(re.search(searchword, searchtermpart(str(ele)))) for ele in tup[0]+[tup[3]] for searchword in searchterm0])]
    sortsearchresult4=([-sum([any([bool(re.search(searchword, searchtermpart(str(ele)))) for ele in tup[0]+[tup[3]]]) for searchword in searchterm0]) for tup in searchresult4])
    searchresult4= [x for _,x in sorted(zip(sortsearchresult4,searchresult4))]

  max_page4=math.ceil(len(searchresult4)/noofresults)
  first_run4 = True
  num4 = 1
  Gnum4 = 1
  GnumDisplay = 0
  infocard=0
  while True:
    if first_run4:
        first_run4 = False
        msg4=await msg4.edit(embed=dmoduleembed(-1,num4,searchresult4,max_page4,message))
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
        msg4=await msg4.edit(embed=dmoduleembed(-1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '⏩' in str(res4.emoji):
        num4 = num4 + 1
        Gnum4 = (num4-1)*noofresults+1
        GnumDisplay = 0
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dmoduleembed(-1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '🔽' in str(res4.emoji):
        Gnum4  = Gnum4 if GnumDisplay==0 else Gnum4+1
        num4 = math.ceil(Gnum4/noofresults)
        GnumDisplay = 1
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=dmoduleembed(Gnum4,num4,searchresult4,max_page4,message))
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
        msg4=await msg4.edit(embed=dmoduleembed(Gnum4 if GnumDisplay == 1 else -1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '🔎' in str(res4.emoji):
      infocard=1-infocard
      await msg4.clear_reactions()
      if infocard==0:
        msg4=await msg4.edit(embed=dmoduleembed(Gnum4 if GnumDisplay == 1 else -1,num4,searchresult4,max_page4,message))
        RecMsg = await record(msg4,RecMsg)
    elif '✅' in str(res4.emoji):
        return await msg4.clear_reactions()
    elif '❌' in str(res4.emoji):
        await message.delete()
        return await msg4.delete()
    if infocard==1:
      msg4=await msg4.edit(embed=dmoduleembed(Gnum4,num4,searchresult4,max_page4,message,True))
      RecMsg = await record(msg4,RecMsg)

def dmoduleembed(Gnum,num,result,max_page,message,infocard=False):
  datahashes=result[noofresults*(num-1):noofresults*num+1]
  n1='\n'
  thedescription="".join(f'{"⇓⇓⇓"+n1+"> " if Gnum==(num-1)*noofresults+i+1 else ""}{(num-1)*noofresults+i+1}. **{datahashes[i][3]}**:  {" ".join(datahashes[i][1].description.split()[:10])} ...\n'for i in range(len(datahashes)))
  
  pattern06=re.compile(r'!module ([a-zA-Z0-9 ]{3,}|\/.*?\/)')
  searchterm=[ii2.group(1) for ii2 in pattern06.finditer(message.content)][0]
  embed=''
  if not infocard:
    embed = nextcord.Embed(color=0x12793e, title=str(len(result))+" modules for \""+searchterm+"\"",description=thedescription)
    embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    embed.set_footer(text="Page: "+str(num)+"/"+str(max_page))
    if Gnum!=-1:
      embed00=result[Gnum-1][1]
      embed.add_field(name="Keywords", value='```'+str(embed00.fields[2].value)+'```\n🔎 to expand a card', inline=False)
  if Gnum!=-1 and infocard:
    embed=result[Gnum-1][1]
    ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
    embed.title=result[Gnum-1][2]
    #
    embed.set_field_at(1,name='Module name',value=result[Gnum-1][3],inline=False)
    #
    embed.set_footer(text=ordinal(Gnum)+" result for \""+searchterm+"\"")
  return embed

async def desmodule(message,id):
  from setup import dpfplist
  #
  await getready(message)
  RecMsg = await record(message)
  #
  approve=client.get_channel(952361570317529140)
  msg=await approve.fetch_message(int(id))
  embed=msg.embeds[0]
  embed.title=msg.content
  modname=str([ele[2] for ele in dpfplist if ele[1]==int(embed.footer.text)][0])+'.'+str(embed.fields[1].value)
  embed.set_field_at(1,name='Module name',value=modname,inline=False)
  msgg0=await message.channel.send(embed=embed)
  RecMsg = await record(msgg0,RecMsg)
