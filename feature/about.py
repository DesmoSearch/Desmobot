import nextcord
import math
from treelib import Tree
import asyncio
import re
import maya
from getinfo import getinfo
from setup import Onready, getready, client, record
from Variables import objowner,GraphsList,thetitles,ParentGraphsList,bump,noofresults, checkIfDuplicates

pattern=re.compile(r"!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?")
pattern02=re.compile(r"!<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?")
async def expandG(emoji,user,messageid,channelid,channel0,message0):
  pattern002=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
  x02=pattern002.finditer(message0.content)
  if len(list(x02))>0:
    message0.author=user
    thehash01=[ii.group(1) for ii in pattern002.finditer(message0.content)][0]
    #
    msg2 = await message0.reply(embed=await getready(message0),mention_author=False)
    RecMsg = await record(message0)
    #
    first_run2 = True
    dachoose2=[1,0,0,RecMsg]
    while True:
      if first_run2:
          first_run2 = False
          dachoose2=[None,thehash01,[thehash01],RecMsg]
          dachoose2=await aboutchain(message0,thehash01,msg2,[True,-10,'','',dachoose2])

      reactmoji2=[]
      
      reactmoji2.append('✅')

      for react2 in reactmoji2:
          await msg2.add_reaction(react2)
          

      def check_react(reaction, user):
          if reaction.message.id != msg2.id:
              return False
          if user != message0.author:
              return False
          if str(reaction.emoji) not in reactmoji2 and str(reaction.emoji) not in ['👈','👉','🖱️']:
              return False
          return True

      try:
          res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
      except asyncio.TimeoutError:
          return await msg2.clear_reactions()
      if user2 != message0.author:
          pass
      elif '✅' in str(res2.emoji):
          return await msg2.clear_reactions()
      elif '🖱️' in str(res2.emoji) or '👈' in str(res2.emoji) or '👉' in str(res2.emoji):
          dachoose2=await aboutchain(message0,thehash01,msg2,[True,-10,res2,user2,dachoose2])

async def onmessage1(message):
  #
  msg = await message.channel.send(embed=await getready(message))
  RecMsg = await record(message)
  #
  async with message.channel.typing():
    searchterm=[ii.group(1) for ii in pattern.finditer(message.content)][0]
    parameterterm = [[ii.group(iii) for ii in pattern.finditer(message.content)][0] for iii in [2,4,6]]
    searchterm1=[ii.group(3) for ii in pattern.finditer(message.content)][0]
    searchterm2=[ii.group(5) for ii in pattern.finditer(message.content)][0]
    searchterm3=[ii.group(7) for ii in pattern.finditer(message.content)][0]
    if checkIfDuplicates(parameterterm):
      parameterterm=[None,None,None]
      searchterm1=""
      searchterm2=""
      searchterm3=""

    titlecond = True if parameterterm==[None,None,None] else ('title' in parameterterm)
    ownercond = True if parameterterm==[None,None,None] else ('owner' in parameterterm)
    hashcond = True if parameterterm==[None,None,None] else ('hash' in parameterterm)
    slashcheckterm,slashcheck1,slashcheck2,slashcheck3=False,False,False,False
    if "/" in searchterm:
      searchterm=searchterm[1:-1]
      slashcheckterm=True
    else:
      searchterm=searchterm.lower()
    if searchterm1 is None:
      searchterm1 = ""
    elif "/" in searchterm1:
      searchterm1=searchterm1[1:-1]
      slashcheck1=True
    else:
      searchterm1=searchterm1.lower()
    if searchterm2 is None:
      searchterm2 = ""
    elif "/" in searchterm2:
      searchterm2=searchterm2[1:-1]
      slashcheck2=True
    else:
      searchterm2=searchterm2.lower()
    if searchterm3 is None:
      searchterm3 = ""
    elif "/" in searchterm3:
      searchterm3=searchterm3[1:-1]
      slashcheck3=True
    else:
      searchterm3=searchterm3.lower()
    
    print(f'"{searchterm}"')

    searchterm0sub=[searchterm1,searchterm2,searchterm3]
    slashchecks=[slashcheck1,slashcheck2,slashcheck3]
    searchtermtitle, searchtermhash, searchtermowner = "", "", "" 
    slashtitlecheck, slashhashcheck, slashownercheck = False,False,False
    try:
      searchtermtitle=searchterm0sub[parameterterm.index('title')]
      slashtitlecheck=slashchecks[parameterterm.index('title')]
    except ValueError:
      searchtermtitle=""
    try:
      searchtermhash=searchterm0sub[parameterterm.index('hash')]
      slashhashcheck=slashchecks[parameterterm.index('hash')]
    except ValueError:
      searchtermhash=""
    try:
      searchtermowner=searchterm0sub[parameterterm.index('owner')]
      slashownercheck=slashchecks[parameterterm.index('owner')]
    except ValueError:
      searchtermowner=""
      

    searchtermpart = lambda data00 : data00 if slashcheckterm else data00.lower()
    searchterm0 = searchtermpart(searchterm)
    titlepart = lambda data00 : data00 if slashtitlecheck else data00.lower()
    hashpart = lambda data00 : data00 if slashhashcheck else data00.lower()
    ownerpart = lambda data00 : data00 if slashownercheck else data00.lower()
    
    searchresult = [hash for hash, title in thetitles.items() if (titlecond*bool(re.search(searchterm0, searchtermpart(str(title)))) or hashcond*bool(re.search(searchterm0, str(hash))) or ownercond*bool(re.search(searchterm0, searchtermpart(str(objowner.get(str(hash),None)))))) and (bool(re.search(titlepart(searchtermtitle), titlepart(str(title)))) and bool(re.search(hashpart(searchtermhash), hashpart(str(hash)))) and bool(re.search(ownerpart(searchtermowner), ownerpart(str(objowner.get(str(hash),None))))))]
    #sortsearchresult=[0 if bump.get(str(dah),None) is None else -bump.get(str(hash),None) for dah in searchresult]
    #searchresult = [x for _,x in sorted(zip(sortsearchresult,searchresult))]

  #https://gist.github.com/noaione/58cdd25a1cc19388021deb0a77582c97
  max_page=math.ceil(len(searchresult)/noofresults)
  first_run = True
  num = 1
  Gnum = 1
  GnumDisplay=0
  infograph=0
  dachoose=[1,0,0,None]
  while True:
    if first_run:
        first_run = False
        msg=await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))
        RecMsg = await record(msg,RecMsg)

    reactmoji = []

    if max_page == 1 and num == 1:
        pass
    elif num == 1:
        reactmoji.append('⏩')
    elif num == max_page:
        reactmoji.append('⏪')
    elif num > 1 and num < max_page:
        reactmoji.extend(['⏪', '⏩'])

    if len(searchresult) == 1 and Gnum == 1 and GnumDisplay==1:
        pass
    elif Gnum == 1:
        reactmoji.append('🔽')
    elif Gnum == len(searchresult) :
        reactmoji.append('🔼')
    elif Gnum > 1 and Gnum<len(searchresult):
        reactmoji.extend(['🔼', '🔽'])

    reactmoji.append('✅')
    if GnumDisplay==1:
      reactmoji.append('🔎')

    for react in reactmoji:
        await msg.add_reaction(react)
        

    def check_react(reaction, user):
        if reaction.message.id != msg.id:
            return False
        if user != message.author:
            return False
        if str(reaction.emoji) not in reactmoji and str(reaction.emoji) not in ['👈','👉','🖱️']:
            return False
        return True

    try:
        res, user = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
    except asyncio.TimeoutError:
        return await msg.clear_reactions()
    if user != message.author:
        pass
    elif '⏪' in str(res.emoji):
        num = num - 1
        Gnum = (num-1)*noofresults+1
        GnumDisplay=0
        infograph=0
        await msg.clear_reactions()
        msg=await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))
        RecMsg = await record(msg,RecMsg)
    elif '⏩' in str(res.emoji):
        num = num + 1
        Gnum = (num-1)*noofresults+1
        GnumDisplay=0
        infograph=0
        await msg.clear_reactions()
        msg=await msg.edit(embed=createembed(-1,num,searchresult,max_page,message))
        RecMsg = await record(msg,RecMsg)
    elif '🔽' in str(res.emoji):
        Gnum  = Gnum if GnumDisplay==0 else Gnum+1
        GnumDisplay=1
        num = math.ceil(Gnum/noofresults)
        await msg.clear_reactions()
        msg=await msg.edit(embed=createembed(Gnum,num,searchresult,max_page,message))
        RecMsg = await record(msg,RecMsg)
        dachoose=[None,searchresult[Gnum-1],[searchresult[Gnum-1]],RecMsg]
    elif '🔼' in str(res.emoji):
        Gnum  = Gnum if GnumDisplay==0 else Gnum-1
        GnumDisplay=1
        num = math.ceil(Gnum/noofresults)
        await msg.clear_reactions()
        msg=await msg.edit(embed=createembed(Gnum,num,searchresult,max_page,message))
        RecMsg = await record(msg,RecMsg)
        dachoose=[None,searchresult[Gnum-1],[searchresult[Gnum-1]],RecMsg]
    elif '✅' in str(res.emoji):
        return await msg.clear_reactions()
    elif '🔎' in str(res.emoji):
        infograph=1-infograph
        await msg.clear_reactions()
        dachoose=[None,searchresult[Gnum-1],[searchresult[Gnum-1]],RecMsg]
        if infograph==0:
          msg=await msg.edit(embed=createembed(-1 if GnumDisplay==0 else Gnum,num,searchresult,max_page,message))
          RecMsg = await record(msg,RecMsg)
    
    if infograph==1:
      dachoose=await aboutchain(message,searchresult[Gnum-1],msg,[True,Gnum,res,user,dachoose])
      RecMsg = dachoose[3]


async def onmessage2(message):
  thehash01=[ii.group(1) for ii in pattern02.finditer(message.content)][0]
  message=await message.edit(suppress=True)
  #
  msg2 = await message.channel.send(embed=await getready(message))
  RecMsg = await record(message)
  RecMsg = await RecMsg.edit(suppress=True)
  #

  first_run2 = True
  dachoose2=[1,0,0,RecMsg]
  while True:
    if first_run2:
        first_run2 = False
        dachoose2=[None,thehash01,[thehash01],RecMsg]
        dachoose2=await aboutchain(message,thehash01,msg2,[True,None,'','',dachoose2])
  
    reactmoji2=[]
    
    reactmoji2.append('✅')
  
    for react2 in reactmoji2:
        await msg2.add_reaction(react2)
        
    def check_react(reaction, user):
        if reaction.message.id != msg2.id:
            return False
        if user != message.author:
            return False
        if str(reaction.emoji) not in reactmoji2 and str(reaction.emoji) not in ['👈','👉','🖱️']:
            return False
        return True
  
    try:
        res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
    except asyncio.TimeoutError:
        return await msg2.clear_reactions()
    if user2 != message.author:
        pass
    elif '✅' in str(res2.emoji):
        return await msg2.clear_reactions()
    elif '🖱️' in str(res2.emoji) or '👈' in str(res2.emoji) or '👉' in str(res2.emoji):
        dachoose2=await aboutchain(message,thehash01,msg2,[True,None,res2,user2,dachoose2])


#################################


async def aboutchain(message,thehash01,msg2,fromSearch):
  async with message.channel.typing():
    newhash=fromSearch[4][1] if fromSearch[0] else thehash01
    historylist=fromSearch[4][2] if fromSearch[0] else [thehash01]
    theinfo = getinfo("https://www.desmos.com/calculator/"+newhash)
    subgraphs = []
    if theinfo['parent_hash'] is not None:
      subgraphs.append(theinfo['parent_hash'])
    choose = fromSearch[4][0] if fromSearch[4][0] is not None else len(subgraphs)
    subgraphs.append(newhash)
    thevalue=','.join([GraphsList[i] for i in range(len(GraphsList)) if (newhash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
    if thevalue!="":
      subgraphs.extend(thevalue.split(','))

  reactmoji2 = []


  def check_react(reaction, user):
      if reaction.message.id != msg2.id:
          return False
      if user != message.author:
          return False
      if str(reaction.emoji) not in reactmoji2:
          return False
      return True
  res2, user2 = '',''
  try:
      if fromSearch[0]:
        res2, user2 = fromSearch[2], fromSearch[3]
      else:
        res2, user2 = await client.wait_for('reaction_add', timeout=100.0, check=check_react)
  except asyncio.TimeoutError:
      return await msg2.clear_reactions()
  if user2 != message.author:
      pass
  elif '👉' in str(res2.emoji):
      choose=choose+1
  elif '👈' in str(res2.emoji):
      choose=choose-1
  elif '🖱️' in str(res2.emoji):
    newhash=subgraphs[choose%len(subgraphs)]
    choose=1
    historylist.append(newhash)
    subgraphs=[newhash]

  if res2!='' and user2!='':
    await msg2.remove_reaction(emoji= "👉", member = user2)
    await msg2.remove_reaction(emoji= "👈", member = user2)
    await msg2.remove_reaction(emoji= "🖱️", member = user2)
  msg2=await msg2.edit(embed=aboutembed(message,newhash,fromSearch,subgraphs[choose%len(subgraphs)],historylist),content='')
  #
  RecMsg = fromSearch[4][3]
  if RecMsg is None:
    RecMsg = await record(msg2)
  else:
    RecMsg = await record(msg2,RecMsg)
  #
  reactmoji2.extend(['👈','👉','🖱️'])

  for react in reactmoji2:
      await msg2.add_reaction(react)

  return ([choose,newhash,historylist,RecMsg])

def aboutembed(message,thehash,fromSearch,underline,historylist):
  dainfo=getinfo("https://www.desmos.com/calculator/"+thehash)
  embed = nextcord.Embed(color=0x12793e, title=dainfo['title'],description="https://www.desmos.com/calculator/"+thehash)
  if 'thumbUrl' in dainfo.keys():
    embed.set_image(url=dainfo['thumbUrl'])
  if objowner.get(str(thehash),None) is not None:
    embed.add_field(name="Shared by", value=re.sub('<@!?[0-9]*>','',objowner.get(str(thehash),None)), inline=False)
  
  embed.add_field(name="Date Created", value="<t:"+str(round(maya.parse(dainfo['created']).datetime().timestamp()))+":F>", inline=True)
  embed.add_field(name="Version", value="```"+str(dainfo['version'])+"```", inline=True)
  if len([] if dainfo['notes'] is None else dainfo['notes'])>0 and len(str(dainfo['notes']))<=1020:
    embed.add_field(name="Notes", value="".join(f"\n{iii+1}. [#{str(dainfo['notes'][iii]['id'])}]{(dainfo['notes'][iii]['text'])}" for iii in range(len(dainfo['notes']))), inline=False)
  elif len(str(dainfo['notes']))>1020:
    embed.add_field(name="Notes", value="Contains "+str(len(dainfo['notes']))+" notes", inline=False)
  if len([] if dainfo['folders'] is None else dainfo['folders'])>0 and len(str(dainfo['folders']))<=1020:
    embed.add_field(name="Folders", value="".join(f"\n{iii+1}. [#{str(dainfo['folders'][iii]['id'])}]{dainfo['folders'][iii]['title']}" for iii in range(len(dainfo['folders']))), inline=False)
  elif len(str(dainfo['folders']))>1020:
    embed.add_field(name="Folders", value="Contains "+str(len(dainfo['folders']))+" folders", inline=False)
  if len([] if dainfo['variables'] is None else dainfo['variables'])>0 and len(str(dainfo['variables']))<=1020:
    embed.add_field(name="Variables", value="```"+' , '.join(dainfo['variables'])+"```", inline=False)
  elif len(str(dainfo['variables']))>1020:
    embed.add_field(name="Variables", value="```"+"Contains "+str(len(dainfo['variables']))+" variables"+"```", inline=False)
  embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)

#history
  graphnodes=[]
  parentnodes=[]
  for newhash in historylist:
    theinfo0 = getinfo("https://www.desmos.com/calculator/"+newhash)
    if theinfo0['parent_hash'] is not None:
      graphnodes.append(theinfo0['parent_hash'])
    graphnodes.append(newhash)
    thevalue0=','.join([GraphsList[i] for i in range(len(GraphsList)) if (newhash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
    if thevalue0!="":
      graphnodes.extend(thevalue0.split(','))
  graphnodes=list(set(graphnodes))
  for iI in range(len(graphnodes)):
    Get=getinfo("https://www.desmos.com/calculator/"+graphnodes[iI])
    if 'parent_hash' in Get.keys():
      parentnodes.append(Get['parent_hash'])
  gtree = Tree()
  gtree.create_node("Graphs", "Graphs")
  for iI2 in range(len(graphnodes)):
    gtree.create_node(graphnodes[iI2],  graphnodes[iI2]   , parent='Graphs')
  for iI3 in range(len(graphnodes)):
    if gtree.contains(parentnodes[iI3]):
      gtree.move_node(graphnodes[iI3], parentnodes[iI3])
  gtree=str(gtree.show(line_type="ascii-ex",stdout=False))
  gtree='```ini\n'+(gtree).replace(underline,"["+underline+"]")+'```'

    
  if fromSearch[0] and fromSearch[1] is not None:
    if fromSearch[1]==-10:
      pattern020=re.compile(r"https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))")
      thehash010=[ii.group(1) for ii in pattern020.finditer(message.content)][0]
      embed.set_footer(text='First desmos url in the message: https://www.desmos.com/calculator/'+thehash010+'\n'+'→'.join(historylist))
    else:
      pattern2=re.compile(r"(!desmos ([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
      searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
      ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
      embed.set_footer(text=ordinal(fromSearch[1])+" graph from \""+searchterm+"\"\n"+'→'.join(historylist))
  elif fromSearch[0] and fromSearch[1] is None:
    pattern020=re.compile(r"!<?https:\/\/www.desmos.com\/calculator\/((?:[a-z0-9]{20})|(?:[a-z0-9]{10}))>?")
    thehash010=[ii.group(1) for ii in pattern020.finditer(message.content)][0]
    embed.set_footer(text='!https://www.desmos.com/calculator/'+thehash010+'\n'+'→'.join(historylist))

  embed.add_field(name="Des[sub]Tree", value=gtree, inline=False)
  if dainfo['parent_hash'] is not None:
    embed.add_field(name="Parent Graph", value=("__**"+dainfo['parent_hash']+"**__" if dainfo['parent_hash']==underline else dainfo['parent_hash']), inline=True)
  embed.add_field(name="Current Graph", value=("__**"+thehash+"**__" if thehash==underline else thehash), inline=True)
  davalue=' , '.join([("__**"+GraphsList[i]+"**__" if GraphsList[i]==underline else GraphsList[i]) for i in range(len(GraphsList)) if (thehash in str(ParentGraphsList[i]) and ParentGraphsList[i] is not None)])
  if davalue!="":
    embed.add_field(name="Child Graphs", value=davalue, inline=True)
  
  
  return embed

############
def createembed(Gnum,num,result,max_page,message):
  datahashes=result[noofresults*(num-1):noofresults*num+1]
  thedescription="".join(f'{"> __**" if Gnum==(num-1)*noofresults+i+1 else ""}{(num-1)*noofresults+i+1}. {"" if objowner.get(str(datahashes[i]),None) is None else (re.sub("<@!?[0-9]*>","",str(objowner.get(str(datahashes[i]),None))))+": "}[{thetitles[datahashes[i]]}](https://www.desmos.com/calculator/{datahashes[i]}){"**__" if Gnum==(num-1)*noofresults+i+1 else ""}\n'for i in range(len(datahashes)))
  
  pattern2=re.compile(r"!desmos (([a-zA-Z0-9 ]{3,}|\/.*?\/)(?: *\?(?:(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?(?:&(title|hash|owner)(?:=([a-zA-Z0-9 ]{3,}|\/.*?\/))?)?)?)")
  searchterm=[ii2.group(1) for ii2 in pattern2.finditer(message.content)][0]
  embed = nextcord.Embed(color=0x12793e, title=str(len(result))+" graphs for \""+searchterm+"\"",description=thedescription)
  embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
  embed.set_footer(text="Page: "+str(num)+"/"+str(max_page))
  if Gnum>-1:
    dahash=result[Gnum-1]
    #dainfo=getinfo("https://www.desmos.com/calculator/"+dahash)
    embed.set_image(url=f"https://saved-work.desmos.com/calc_thumbs/production/{dahash}.png")
    embed.add_field(name="Graph Selected:", value=f"https://www.desmos.com/calculator/{dahash}", inline=False)
    #embed.add_field(name="Date Created", value=dainfo['date'], inline=False)
  return embed