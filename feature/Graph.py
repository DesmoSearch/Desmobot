from setup import getready, client, record
from Variables import checkIfDuplicates
import asyncio
import re
import json
import math
import nextcord
pattern03=re.compile(r"(!graph ([^?]+)(?: *\?(?:(x|y|size)(?:=(\[.*?,.*?\]))?)(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?(?:&(x|y|size)(?:=(\[.*?,.*?\]))?)?)?)")

async def GraphStuff(message):
  #
  msg3 = await message.channel.send(embed=await getready(message))
  RecMsg = await record(message)
  #
  async with message.channel.typing():
    await asyncio.sleep(1)
  #
  wholeterm3=[ii.group(1) for ii in pattern03.finditer(message.content)][0]
  searchterm3=[ii.group(2) for ii in pattern03.finditer(message.content)][0]
  parameterterm3 = [[ii.group(iii) for ii in pattern03.finditer(message.content)][0] for iii in [3,5,7]]
  searchterm13=[ii.group(4) for ii in pattern03.finditer(message.content)][0]
  searchterm23=[ii.group(6) for ii in pattern03.finditer(message.content)][0]
  searchterm33=[ii.group(8) for ii in pattern03.finditer(message.content)][0]
  if checkIfDuplicates(parameterterm3):
    parameterterm3=[None,None,None]
    searchterm13=""
    searchterm23=""
    searchterm33=""
  searchterm3sub=[searchterm13,searchterm23,searchterm33]
  searchtermx, searchtermy, searchtermsize = "[-10,10]", "[-10,10]", "[500,500]" 
  try:
    searchtermx=searchterm3sub[parameterterm3.index('x')]
  except ValueError:
    searchtermx="[-10,10]"
  try:
    searchtermy=searchterm3sub[parameterterm3.index('y')]
  except ValueError:
    searchtermy="[-10,10]"
  try:
    searchtermsize=searchterm3sub[parameterterm3.index('size')]
  except ValueError:
    searchtermsize="[500,500]"
  if json.loads(searchtermx)[1]-json.loads(searchtermx)[0]<0:
    searchtermx="[-10,10]"
  if json.loads(searchtermy)[1]-json.loads(searchtermy)[0]<0:
    searchtermy="[-10,10]"
  if (json.loads(searchtermsize)[0]<50 or json.loads(searchtermsize)[1]<50) or not (1/2<=json.loads(searchtermsize)[0]/json.loads(searchtermsize)[1]<=2):
    searchtermsize="[500,500]"
  
  xtick=AutomateXYLabels(json.loads(searchtermx)[0],json.loads(searchtermx)[1])
  ytick=AutomateXYLabels(json.loads(searchtermy)[0],json.loads(searchtermy)[1])
  searchterm3=searchterm3.replace(" ", "")
  
  first_run3 = True
  strlist = lambda x, y: f"[{x},{y}]"
  while True:
      reactmoji3 = []
      if first_run3:
          if '&' in searchterm3:
            reactmoji3.append('🔄')
          reactmoji3.extend(['➡️','⬆️','⬅️','⬇️','🔬','🔭','✅'])
          first_run3 = False
          msg3=await msg3.edit(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
          RecMsg = await record(msg3,RecMsg)
        
      thex0=json.loads(searchtermx)[0]
      thex1=json.loads(searchtermx)[1]
      they0=json.loads(searchtermy)[0]
      they1=json.loads(searchtermy)[1]
      scalex=(thex1-thex0)/10
      scaley=(they1-they0)/10
      zoomf=1.5

      if '&' in searchterm3:
        reactmoji3.append('🔄')
      reactmoji3.extend(['➡️','⬆️','⬅️','⬇️','🔬','🔭','✅'])
      
      if str(message.author.id)=='686012491607572515':
         reactmoji3.append('❌')

      for react in reactmoji3:
          await msg3.add_reaction(react)

      def check_react(reaction, user):
          if reaction.message.id != msg3.id:
              return False
          if user != message.author:
              return False
          if str(reaction.emoji) not in reactmoji3:
              return False
          return True

      try:
          res3, user3 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
      except asyncio.TimeoutError:
          return await msg3.clear_reactions()
      if user3 != message.author:
          pass
      elif '✅' in str(res3.emoji):
          return await msg3.clear_reactions()
      elif '❌' in str(res3.emoji):
          await message.delete()
          return await msg3.delete()
      else:

        if '🔄' in str(res3.emoji):
            searchterm3='&'.join(searchterm3.split('&')[1:]+searchterm3.split('&')[:1])

        if '➡️' in str(res3.emoji):
            thex0,thex1=thex0+scalex,thex1+scalex
            searchtermx=strlist(thex0,thex1)
            
            
        if '⬆️' in str(res3.emoji):
            they0,they1=they0+scaley,they1+scaley
            searchtermy=strlist(they0,they1)

            
        if '⬅️' in str(res3.emoji):
            thex0,thex1=thex0-scalex,thex1-scalex
            searchtermx=strlist(thex0,thex1)

            
        if '⬇️' in str(res3.emoji):
            they0,they1=they0-scaley,they1-scaley
            searchtermy=strlist(they0,they1)
            await message.remove_reaction('⬇️',message.author)

            
        if '🔬' in str(res3.emoji):
            thex0,thex1=(thex0+thex1)/2-(1/zoomf)*(thex1-thex0)/2,(thex0+thex1)/2+(1/zoomf)*(thex1-thex0)/2
            they0,they1=(they0+they1)/2-(1/zoomf)*(they1-they0)/2,(they0+they1)/2+(1/zoomf)*(they1-they0)/2
            thex0,thex1,they0,they1=round(thex0,2),round(thex1,2),round(they0,2),round(they1,2)
            searchtermx=strlist(thex0,thex1)
            searchtermy=strlist(they0,they1)
            
        if '🔭' in str(res3.emoji):
            thex0,thex1=(thex0+thex1)/2-(zoomf)*(thex1-thex0)/2,(thex0+thex1)/2+(zoomf)*(thex1-thex0)/2
            they0,they1=(they0+they1)/2-(zoomf)*(they1-they0)/2,(they0+they1)/2+(zoomf)*(they1-they0)/2
            thex0,thex1,they0,they1=round(thex0,2),round(thex1,2),round(they0,2),round(they1,2)
            searchtermx=strlist(thex0,thex1)
            searchtermy=strlist(they0,they1)
            

      xtick=AutomateXYLabels(json.loads(searchtermx)[0],json.loads(searchtermx)[1])
      ytick=AutomateXYLabels(json.loads(searchtermy)[0],json.loads(searchtermy)[1])
      
      await msg3.remove_reaction(emoji= res3.emoji, member = user3) 
      
      msg3=await msg3.edit(embed=graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick))
      RecMsg = await record(msg3,RecMsg)

#https://studio.code.org/projects/applab/kEUCxMdKd7P-a1y4zo4cO3IQasxWXeHipAoDwk1dS4w/view
def AutomateXYLabels(first,second):
  XLabel=(second-first)/5
  NumberOfDigits=round(math.log(XLabel,10))
  NearestArray=[1,2,5]
  MultiplyNearestArrayBy = [NumberOfDigits-1,NumberOfDigits]
  XLabelList = [NearestArray[j]*(10**MultiplyNearestArrayBy[i]) for i in range(2) for j in range(3)];
  LeastDiff = [abs(NearestArray[j]*(10**MultiplyNearestArrayBy[i])-XLabel) for i in range(2) for j in range(3)];
  XLabel=XLabelList[LeastDiff.index(min(LeastDiff))]
  return (XLabel/5)

def graphembed(message,wholeterm3,searchterm3,searchtermx,searchtermy,searchtermsize,xtick,ytick):
  import urllib.parse
  searchterm3=searchterm3.replace('&',',')
  thelink=f"https://graphsketch.com/render.php?eqn1_eqn={urllib.parse.quote(searchterm3)}&x_min={json.loads(searchtermx)[0]}&x_max={json.loads(searchtermx)[1]}&y_min={json.loads(searchtermy)[0]}&y_max={json.loads(searchtermy)[1]}&image_w={json.loads(searchtermsize)[0]}&image_h={json.loads(searchtermsize)[1]}&do_grid=1&x_tick={xtick}&y_tick={ytick}&x_label_freq=5&y_label_freq=5"
  gembed=nextcord.Embed(title=wholeterm3,description=f"[Open image in a new tab]({thelink})")
  gembed.add_field(name="Graph(s)", value=searchterm3, inline=False)
  gembed.add_field(name="Domain", value=searchtermx, inline=True)
  gembed.add_field(name="Range", value=searchtermy, inline=True)
  gembed.add_field(name="Image Dimensions", value=f"[width,height]: {searchtermsize}", inline=False)
  gembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
  gembed.set_image(url=thelink)
  return gembed