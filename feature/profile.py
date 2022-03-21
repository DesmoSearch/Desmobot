import nextcord
import re
import math
import asyncio
from setup import client,setupDpfp
pattern08=re.compile(r'!profile +(?:"([A-Za-z0-9]+)"(?:\?image=(.+))?)?(?:\n([\s\S]*))?')
pattern09=re.compile(r'!profile +([0-9]+|<@![0-9]+>)')
Dprofilechannel=950550255789830164

async def Dprofile(message):
  from setup import dpfplist
  Description=[ii.group(3) for ii in pattern08.finditer(message.content)][0]
  Image=[ii.group(2) for ii in pattern08.finditer(message.content)][0]
  Nick=[ii.group(1) for ii in pattern08.finditer(message.content)][0]
  if len(Description if Description is not None else '')<4000:
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
      await msgdel.delete()
    else:
      dpfpembed.add_field(name="Descoins", value="300", inline=False)
    message0=await channel.send(embed=dpfpembed) 
    await message.channel.send(embed=dpfpembed)
    await setupDpfp()

async def seeprofile(message):
  from setup import dpfplist
  channel = client.get_channel(Dprofilechannel)
  ifany=[i[0] for i in dpfplist if i[1]==int(re.sub('[<@!>]','',[ii.group(1) for ii in pattern09.finditer(message.content)][0]))]
  if len(ifany)==1:
    damsg=await channel.fetch_message(ifany[0])
    await message.channel.send(embed=damsg.embeds[0])