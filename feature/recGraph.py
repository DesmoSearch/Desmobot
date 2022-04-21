import nextcord
import re
import setup
from setup import getready, client, record
from getinfo import getinfo
import Variables
from Variables import GraphsList, objowner
channelgraphs = 959405907857522728
async def recGraphE(message,hash,theauthor=None,first='!!!'):
  
  patternG2=re.compile(r"!contribute +([a-z0-9 ,]*) *(?:\?owner=(\S*))?")
  xG2=patternG2.finditer(message.content)
  xG3=patternG2.finditer(message.content)
  #
  link0='https://www.desmos.com/calculator/'+str(hash)
  geti=getinfo(link0)
  if geti!={}:
    if (hash not in GraphsList if len(list(xG2))!=1 else (first=='!!!' if hash in GraphsList else True)*(hash not in [ele[0] for ele in setup.HashPlusCard])) and (geti['title'] is not None if first=='!!!' else True):
      await setup.Onready()
      user=message.author
      embed=nextcord.Embed(title=str(geti['title']),description=link0)
      if hash in GraphsList and objowner.get(str(hash),None) is not None:
        if user.id in [468963362131279882,686012491607572515,879683888191012914]:
          embed.set_author(name=(str(user) if theauthor is None else theauthor))
        else:
          pass
      elif theauthor is None:
        embed.set_author(name=str(user), icon_url=user.display_avatar.url)
      else:
        embed.set_author(name=str(theauthor))
      embed.set_image(url=geti['thumbUrl'])
      embed.add_field(name="Parent", value=str(geti['parent_hash']), inline=True)
      embed.add_field(name="Graph", value=str(hash), inline=True)
      embed.add_field(name="Score", value=str(0), inline=False)
      embed.set_footer(text=str(user.id))
      des=''
      if 'Direct Message' in str(message.channel):
        des=str(message.author.id)+'|'+str(message.id)
      else:
        des=str(message.channel.id)+';'+str(message.id)
      channel = client.get_channel(channelgraphs)
      graphcard=await channel.send(content=des+(first if '!https://www.desmos.com/calculator' not in message.content else ''),embed=embed)
      #
      setup.HashPlusCard.append((str(hash),graphcard.id))
      if hash not in GraphsList:
        Variables.GraphsList.append(str(hash))
        Variables.ParentGraphsList.append(geti['parent_hash'])
        Variables.thetitles[str(hash)]=str(geti['title'])
      if first=='!!!' and objowner.get(str(hash),None) is None and '!https://www.desmos.com/calculator' not in message.content:
        Variables.objowner[str(hash)]=(str(user) if theauthor is None else theauthor)+'<@'+str(user.id)+'>'
      if first=='!!!' and objowner.get(str(hash),None) is not None and '!https://www.desmos.com/calculator' not in message.content and hash in GraphsList and user.id in [468963362131279882,686012491607572515,879683888191012914]:
        Variables.objowner[str(hash)]=(str(user) if theauthor is None else theauthor)+'<@'+str(user.id)+'>'
      #
      if geti['parent_hash'] is not None:
        await recGraphE(message,geti['parent_hash'],theauthor,first='')
      return graphcard
    elif (len(list(xG3))==1 and (hash in [ele[0] for ele in setup.HashPlusCard]) and first=='!!!'):
      await setup.Onready()
      user=message.author
      getid=[ele[1] for ele in setup.HashPlusCard if ele[0]==hash]
      channel = client.get_channel(channelgraphs)
      damsg0=await channel.fetch_message(int(getid[0]))
      if '!!!' not in damsg0.content:
        embed00=damsg0.embeds[0]
        if hash in GraphsList and objowner.get(str(hash),None) is not None:
          pass
        elif theauthor is None:
          embed00.set_author(name=str(user), icon_url=user.display_avatar.url)
        else:
          embed00.set_author(name=str(theauthor))
        graphcard=await damsg0.edit(content=damsg0.content+'!!!!',embed=embed00)
        Variables.objowner[str(hash)]=(str(user) if theauthor is None else theauthor)+'<@'+str(user.id)+'>'
        return graphcard
      elif '!!!' in damsg0.content and hash in GraphsList and objowner.get(str(hash),None) is not None and user.id in [468963362131279882,686012491607572515,879683888191012914]:
        embed00=damsg0.embeds[0]
        embed00.set_author(name=(str(user) if theauthor is None else theauthor))
        graphcard=await damsg0.edit(content=damsg0.content,embed=embed00)
        Variables.objowner[str(hash)]=(str(user) if theauthor is None else theauthor)+'<@'+str(user.id)+'>'
        return graphcard
        

      


async def OnMessageG(message):
  patternG=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
  xG=patternG.finditer(message.content)
  patternG2=re.compile(r"!contribute +([a-z0-9 ,]*) *(?:\?owner=(\S*))?")
  xG2=patternG2.finditer(message.content)
  patternG3=re.compile(r"!bump +((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
  xG3=patternG3.finditer(message.content)
  
  if message.author == client.user or message.author.bot or message.guild is None:
    return
  elif len(list(xG))>=1:
    Gss=[ii.group(1) for ii in patternG.finditer(message.content)]
    for Gs in Gss:
      await recGraphE(message,Gs)
  elif len(list(xG2))==1:
    await getready(message)
    RecMsg = await record(message)
    Gss=[ii.group(1) for ii in patternG2.finditer(message.content)][0].replace(' ','').split(',')
    Author=[ii.group(2) for ii in patternG2.finditer(message.content)][0]
    Earndescoin=0
    Togon=0
    for Gs in Gss:
      greturn=await recGraphE(message,Gs,Author)
      if greturn:
        RecMsg = await record(greturn,RecMsg)
        if greturn.embeds[0].author:
          Earndescoin=Earndescoin+10
        else:
          Togon=1
          await message.add_reaction('✅')
    if Earndescoin>0:
      await message.add_reaction('✅')
      await message.reply(f"!give {Earndescoin} to {message.author.id}")
    elif Togon==0:
      await message.reply("Invalid graph hash(s) or Graph card(s) already exist.")
    
  elif len(list(xG3))==1:
    RecMsg = await record(message)
    bumpG=str([ii.group(1) for ii in patternG3.finditer(message.content)][0])

    getid=[ele[1] for ele in setup.HashPlusCard if ele[0]==bumpG]
    
    if len(getid)==0:
      botstatement=await message.reply('To !bump you would need to create the graph card first by: ```!contribute {graph hash}?owner={author\'s name}```')
      RecMsg = await record(botstatement,RecMsg)
    else:
      channel = client.get_channel(channelgraphs)
      damsg0=await channel.fetch_message(int(getid[0]))
      daembed0=damsg0.embeds[0]
      daembed0.set_field_at(2,name='Score',value=str(10+int(daembed0.fields[2].value)),inline=False)
      Variables.bump[bumpG]=10+int(daembed0.fields[2].value)
      await damsg0.edit(embed=daembed0)
      await message.add_reaction('✅')