from setup import getready, client, record
from getinfo import difference
from Variables import noofresults
import re
import nextcord
import math
import asyncio
pattern04=re.compile(r"!\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))(?: vs \/((?:[a-z0-9]{20})|(?:[a-z0-9]{10})))?")
async def DiffStuff(message,reactmode=False):
  #
  msg4=''
  if reactmode:
    msg4 = await message.reply(embed=await getready(message),mention_author=False)
  else:
    msg4 = await message.channel.send(embed=await getready(message))
  RecMsg = await record(message)
  #
  async with message.channel.typing():
    hash1=[ii.group(1) for ii in pattern04.finditer(message.content)][0]
    hash2=[ii.group(2) for ii in pattern04.finditer(message.content)][0]
    searchresult04=difference(hash1,hash1 if hash2 is None else hash2)
    searchresult4=searchresult04[1]
    parentofhash1=searchresult04[2]
  max_page4=math.ceil(len(searchresult4)/noofresults)
  first_run4 = True
  num4 = 1
  Gnum4 = 1
  GnumDisplay = 0
  ghash1list=[hash1]
  while True:
    if first_run4:
        first_run4 = False
        msg4=await msg4.edit(embed=diffembed(-1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
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

    if parentofhash1 is not None:
      reactmoji4.append('👈')
    if ghash1list.index(hash1)>1:
      reactmoji4.append('👉')
    
    reactmoji4.append('✅')
  
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
        msg4=await msg4.edit(embed=diffembed(-1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
        RecMsg = await record(msg4,RecMsg)
    elif '⏩' in str(res4.emoji):
        num4 = num4 + 1
        Gnum4 = (num4-1)*noofresults+1
        GnumDisplay = 0
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=diffembed(-1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
        RecMsg = await record(msg4,RecMsg)
    elif '🔽' in str(res4.emoji):
        Gnum4  = Gnum4 if GnumDisplay==0 else Gnum4+1
        num4 = math.ceil(Gnum4/noofresults)
        GnumDisplay = 1
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=diffembed(Gnum4,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
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
        msg4=await msg4.edit(embed=diffembed(Gnum4 if GnumDisplay == 1 else -1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
        RecMsg = await record(msg4,RecMsg)
    elif '👈' in str(res4.emoji):
        async with message.channel.typing():
          hash1,hash2=parentofhash1, hash1
          if hash1 not in ghash1list:
            ghash1list.append(hash1)
          searchresult04=difference(hash1,hash2)
          searchresult4=searchresult04[1]
          parentofhash1=searchresult04[2]
        num4 = 1
        Gnum4 = 1
        GnumDisplay = 0
        max_page4=math.ceil(len(searchresult4)/noofresults)
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=diffembed(-1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
        RecMsg = await record(msg4,RecMsg)
    elif '👉' in str(res4.emoji):
        async with message.channel.typing():
          hash1,hash2=hash2,ghash1list[-1+ghash1list.index(hash2)]
          searchresult04=difference(hash1,hash2)
          searchresult4=searchresult04[1]
          parentofhash1=searchresult04[2]
        num4 = 1
        Gnum4 = 1
        GnumDisplay = 0
        max_page4=math.ceil(len(searchresult4)/noofresults)
        await msg4.clear_reactions()
        msg4=await msg4.edit(embed=diffembed(-1,num4,searchresult04,max_page4,message,hash1,hash2,ghash1list))
        RecMsg = await record(msg4,RecMsg)
    elif '✅' in str(res4.emoji):
        return await msg4.clear_reactions()


def diffembed(Gnum,num,result,max_page,message,graph1,graph2,ghash1list):
  #from createembed()
  daexps=result[4][noofresults*(num-1):noofresults*num+1]
  thedescription='\n'.join(f'{"⇓⇓⇓" if Gnum==(num-1)*noofresults+i+1 else ""}{(daexps[i])}' for i in range(len(daexps)))
  pattern4=re.compile(r"!\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))(?: vs \/((?:[a-z0-9]{20})|(?:[a-z0-9]{10})))?")
  if len(thedescription)>4000:
    thedescription = 'Description is greater than 4000 characters.\nSelect expressions using :arrow_down_small: , :arrow_up_small:'

  if graph2 is None:
    embed = nextcord.Embed(color=0x12793e, title='/'+graph1,description=thedescription)
  else:
    embed = nextcord.Embed(color=0x12793e, title='/'+graph1+' vs /'+graph2,description=thedescription)
  embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
  embed.set_footer(text="Page: "+str(num)+"/"+str(max_page)+'\n'+'←'.join(reversed(['*'+gg+'*' if gg==graph1 else gg for gg in ghash1list])))
  if graph2 is not None:
    embed.add_field(name="Similarity percentage", value=str(round(result[0]*100,2))+'%', inline=False)
  if Gnum>-1:
    dahash=result[1][Gnum-1][8:-3]
    embed.add_field(name=f"Selected ({result[3][Gnum-1]}):" if graph2 is None else "Selected:", value=result[4][Gnum-1] if len(result[4][Gnum-1])<1000 else result[4][Gnum-1][:1000]+'```...', inline=False)
    '''def rremove(match_obj):
      if match_obj.group(1) is not None:
        return ''
    before = (re.sub(r"(\[#.*?\] )",rremove, ''.join(difflib.restore(dahash.splitlines(), 1)), count=1))
    after = (re.sub(r"(\[#.*?\] )",rremove, ''.join(difflib.restore(dahash.splitlines(), 2)), count=1))
    embed.set_image(url=r"https://latex.codecogs.com/png.image?\dpi{200}%20\left\{\begin{matrix}"+before+r"\\"+after+r"\end{matrix}\right.")'''

  return embed