import nextcord
import re
import math
import asyncio
from setup import client,setupDpfp, getready, record
pattern08=re.compile(r'!profile +"([A-Za-z0-9]+)"(?:\?image=(.+))?(?:\n([\s\S]*))?')
pattern09=re.compile(r'!profile +([0-9]+|<@![0-9]+>)')
Dprofilechannel=950550255789830164

async def Dprofile(message):
  from setup import dpfplist
  Description=[ii.group(3) for ii in pattern08.finditer(message.content)][0]
  Image=[ii.group(2) for ii in pattern08.finditer(message.content)][0]
  Nick=[ii.group(1) for ii in pattern08.finditer(message.content)][0]
  if len(Description if Description is not None else '')<4000 and Nick not in [ele[2] for ele in dpfplist if ele[1]!=message.author.id]:
    dpfpembed=nextcord.Embed(title=message.author.name if Nick is None else Nick,description=Description if Description is not None else '')
    dpfpembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
    dpfpembed.set_thumbnail(url=Image if Image is not None else message.author.display_avatar.url)
    dpfpembed.set_footer(text=str(message.author.id))
    channel = client.get_channel(Dprofilechannel)
    await message.edit(suppress=True)
    
    ifany=[i[0] for i in dpfplist if i[1]==(message.author.id)]
    if len(ifany)==1:
      msgdel=await channel.fetch_message(ifany[0])
      dpfpembed.add_field(name="Descoins", value=msgdel.embeds[0].fields[0].value, inline=False)
      #
      await updateModulelist(msgdel.embeds[0].title,Nick,message.author.id)
      #
      await msgdel.delete()
    else:
      dpfpembed.add_field(name="Descoins", value=str(300), inline=False)
    await channel.send(embed=dpfpembed) 
    sentmessage=await message.channel.send(embed=dpfpembed)
    await setupDpfp()
  elif Nick in [ele[2] for ele in dpfplist if ele[1]!=message.author.id]:
    await message.reply("Profile name already exists. Try a unique name.")

async def seeprofile(message):
  #
  await getready(message)
  RecMsg = await record(message)
  #
  from setup import dpfplist
  channel = client.get_channel(Dprofilechannel)
  ruserid=re.sub('[<@!>]','',[ii.group(1) for ii in pattern09.finditer(message.content)][0])
  ifany=[i[0] for i in dpfplist if i[1]==int(ruserid)]
  if len(ifany)==1:
    damsg=await channel.fetch_message(ifany[0])
    output=damsg.embeds[0]
    THEuser = await client.fetch_user(str(ruserid))
    output.set_author(name=str(THEuser), icon_url=THEuser.display_avatar.url)
    output.set_field_at(0,name='Descoins',value='```ansi\n[1;33m ⏣'+output.fields[0].value+'```',inline=False)
    #
    from setup import dmodulelist
    modnamesl=[ele[3] for ele in dmodulelist if ele[4]==int(ruserid)]
    if len(modnamesl)>0:
      output.add_field(name="Modules", value='```'+','.join(modnamesl)+'```', inline=False)
    #
    await message.channel.send(embed=output)

pattern10=re.compile(r'!give +([0-9]+) +to +([0-9,<>!@ ]+)')
async def give(message):
  from setup import dpfplist
  much=int([ii.group(1) for ii in pattern10.finditer(message.content)][0])
  to=[ii.group(2) for ii in pattern10.finditer(message.content)][0].split(',')
  ifany=[i[0] for i in dpfplist if i[1]==(message.author.id)]
  channel = client.get_channel(Dprofilechannel)
  
  if len(ifany)==1:
    giver=await channel.fetch_message(ifany[0])
    amount=int(giver.embeds[0].fields[0].value)
    if much*len(to)<amount or message.author.id==686012491607572515:
      #
      await getready(message)
      RecMsg = await record(message)
      #
      for p in to:
        p=re.sub('[<@!>]','',p)
        try:
          user=await client.fetch_user(p)
          ifanyuser=[i[0] for i in dpfplist if i[1]==(user.id)]

          if len(ifanyuser)==1:
            await appendamount(message,ifanyuser[0],much)
            await appendamount(message,ifany[0],-much)
          else:
            await defaultpfp(user,much)
            await appendamount(message,ifany[0],-much)
        except:
          await message.reply("{} is an invalid user id".format(p))
      await message.add_reaction('✅')
    else:
      await message.reply("You don't have enough descoins to !give")
  else:
    await message.reply("First create a profile using !profile and try again.")

async def defaultpfp(user,much):
  dpfpembed=nextcord.Embed(title=user.name,description='')
  dpfpembed.set_author(name=str(user), icon_url=user.display_avatar.url)
  dpfpembed.set_thumbnail(url=user.display_avatar.url)
  dpfpembed.set_footer(text=str(user.id))
  dpfpembed.add_field(name="Descoins", value=str(300+much), inline=False)
  channel = client.get_channel(Dprofilechannel)
  message0=await channel.send(embed=dpfpembed) 
  await setupDpfp()

async def appendamount(message,user000,amount):
  channel = client.get_channel(Dprofilechannel)
  if message.author.id==686012491607572515 and amount<0:
    pass
  else:
    damsg0=await channel.fetch_message(user000)
    daembed0=damsg0.embeds[0]
    daembed0.set_field_at(0,name='Descoins',value=str(amount+int(daembed0.fields[0].value)),inline=False)
    await damsg0.edit(embed=daembed0)

async def updateModulelist(Nick0,Nick1,userid):
  if Nick0!=Nick1:
    import setup
    from setup import dmodulelist
    setup.dmodulelist=[(ele[0],ele[1],ele[2],Nick1+(ele[3])[ele[3].index('.'):] if userid==ele[4] else ele[3],ele[4]) for ele in dmodulelist]