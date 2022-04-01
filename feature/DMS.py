import nextcord
from nextcord import Webhook, DMChannel
import aiohttp
from replit import db
import re

DMurl=db['dm']
DMthread=953517900172501042
def Encode(msg):
  string=format(int(msg.id), '#010b')
  string=string.replace('0b','\u200B\u200B\u200B')
  string=string.replace('0','\uFEFF­')
  string=string.replace('1','\u200E­')
  string=string+'\u200B\u200B\u200B'
  return string

def Decode(msg):
  if msg!='':
    if '\u200B\u200B\u200B' in msg.content and msg.author.id==944269890301345884:
      pattern=re.compile("\u200B\u200B\u200B(.*)\u200B\u200B\u200B")
      string=[ii.group(1) for ii in pattern.finditer(msg.content)][0]
      string=string.replace('\uFEFF­','0')
      string=string.replace('\u200E­','1')
      return(int(string,2))
    
async def Wholesome(x,webhook,channelsendto ):
  if 'Direct Message' in str(x.channel):
    des=str(x.author.id)+'|'+str(x.id)
  else:
    des=str(x.channel.id)+';'+str(x.id)

  return await webhook.send(content=x.content, username=str(x.author), avatar_url=x.author.display_avatar.url,embed=nextcord.Embed(description=des),files=[await f.to_file() for f in x.attachments],wait=True)

async def DMrec(msg,client):
  REPmessage=''
  if msg.reference is not None:
    REPmessage = await msg.channel.fetch_message(msg.reference.message_id)
  if msg.author==client.user:
    return
  elif 'Direct Message with' in str(msg.channel) or (getattr(getattr(REPmessage,'author',0),'id',0)==client.user.id and msg.channel.id!=DMthread) or ('<@!'+str(client.user.id)+'>' in msg.content and msg.channel.id!=DMthread):
    channel = client.get_channel(DMthread)
    Check=(Decode(REPmessage))
    REPLYTO=''
    if Check:
      REPLYTO = await channel.fetch_message(Check)
    elif 'Direct Message' not in str(msg.channel) and getattr(getattr(REPmessage,'author',0),'id',0)==client.user.id:
      REPLYTO=await channel.send(content='content: '+str(REPmessage.content)+'\nauthor: '+str(REPmessage.author)+';'+str(REPmessage.author.id)+'\nid: '+str(REPmessage.channel.id)+';'+str(REPmessage.id),embed=(REPmessage.embeds[0]) if REPmessage.embeds else None,files=[await f.to_file() for f in REPmessage.attachments])
    async with aiohttp.ClientSession() as session: 
      webhook = Webhook.from_url(DMurl, session=session)
      save0=await Wholesome(msg,webhook,channel)
      if REPLYTO:
        await save0.edit(content=REPLYTO.jump_url+'\n'+save0.content)
      

  elif msg.channel.id==DMthread:
    if getattr(REPmessage,'embeds',False):
      if ';' in REPmessage.embeds[0].description:
        channel0 = client.get_channel(int(REPmessage.embeds[0].description.split(';')[0]))
        message0 = await channel0.fetch_message(int(REPmessage.embeds[0].description.split(';')[1]))
        await message0.reply(Encode(msg)+msg.content,files=[await f.to_file() for f in msg.attachments])
      elif '|' in REPmessage.embeds[0].description:
        msgIDget=REPmessage.embeds[0].description.split('|')[1]
        user00 = await client.fetch_user(REPmessage.embeds[0].description.split('|')[0])
        historyget=await user00.history(limit=6).flatten()
        historygetfirst=next(filter(lambda l: l.author.id==user00.id,historyget),False)
        if getattr(historygetfirst,'id',False)==int(msgIDget):
          await DMChannel.send(user00,Encode(msg)+msg.content,files=[await f.to_file() for f in msg.attachments])
        else:
          messagereplyto = await user00.fetch_message(msgIDget)
          await messagereplyto.reply(Encode(msg)+msg.content,files=[await f.to_file() for f in msg.attachments])
    else:
      #to directly dm, message or reply in a channel
      await custome314(msg,client)
        
##################

async def DMreact(emoji,user,message,client,addStatus):
  if user.id==686012491607572515 and message.channel.id==DMthread:
    if getattr(message,'embeds',False):
      if ';' in message.embeds[0].description:
        channel0 = client.get_channel(int(message.embeds[0].description.split(';')[0]))
        message0 = await channel0.fetch_message(int(message.embeds[0].description.split(';')[1]))
        if addStatus:
          await message0.add_reaction(emoji)
        else:
          await message0.remove_reaction(emoji,client.user)
      elif '|' in message.embeds[0].description:
        msgIDget=message.embeds[0].description.split('|')[1]
        user00 = await client.fetch_user(message.embeds[0].description.split('|')[0])
        message0 = await user00.fetch_message(msgIDget)
        if addStatus:
          await message0.add_reaction(emoji)
        else:
          await message0.remove_reaction(emoji,client.user)
  elif 'Direct Message with' in str(message.channel) or (getattr(getattr(message,'author',0),'id',0)==client.user.id and message.channel.id!=DMthread):
    channel = client.get_channel(DMthread)
    Check=(Decode(message))
    if Check:
      message0 = await channel.fetch_message(Check)
      if addStatus:
        await message0.add_reaction(emoji)
#############
async def custome314(msg,client):
  #to directly dm, message or reply in a channel
  if msg.content[:2]=='!;' and msg.author.id==686012491607572515:
    thecontent=msg.content.split('!;')
    if len(thecontent)==3:
      dmuser=await client.fetch_user(thecontent[1])
      await dmuser.send(content=Encode(msg)+thecontent[2])
  elif msg.content[:2]==';!' and msg.author.id==686012491607572515:
    thecontent=msg.content.split(';!')
    if len(thecontent)==3:
      msgchannel=client.get_channel(int(thecontent[1]))
      await msgchannel.send(content=Encode(msg)+thecontent[2])
    elif len(thecontent)==4:
      msgchannel=client.get_channel(int(thecontent[1]))
      msgtoreply=await msgchannel.fetch_message(int(thecontent[2]))
      await msgtoreply.reply(content=Encode(msg)+thecontent[3])