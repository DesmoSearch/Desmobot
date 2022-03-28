from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import asyncio
import re
from setup import getready, record
import nextcord

from random import choice
def randomcharlen(leng):
  return(''.join(map(choice,["bcdfghjklmnpqrstvwxz7","aeiouyaeiouy0"]*int(leng/2))))

def variablerep(string):
  string=re.sub('\)',')\ue014',string)
  return re.sub('(.)_([A-Za-z0-9]*)', '\\1_\\2\ue014', string)
  
def desmotable2(table):
  def flatten(t):
    return [item for sublist in t for item in sublist]

  rows=table.split('|')
  string='\n'
  if len(rows)>1:
    string='table\ue013'
    string=string+''.join([elem+'\ue014' for elem in rows[0].split(',')])
    rest=flatten([row.split(',') for row in rows[1:]])
    string=string+'\t'+'\t'.join(rest)+'\n'
  return string

async def screenshotdes(graphkeys,settings,Settings,Title,dAhAsH,URL='https://www.desmos.com/calculator'):
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options=chrome_options)
  
  driver.get(URL)
  await asyncio.sleep(3)
  selectfirst=driver.find_element(By.CLASS_NAME, "dcg-mq-root-block")
  action =  ActionChains(driver);
  action.click(on_element = selectfirst)
  CREDITS='"Graph created using https://github.com/DesmoSearch/Desmobot discord bot | MathEnthusiast314'
  #action.send_keys(graphkeys+CREDITS)
  graphkeyssplit=graphkeys.split('\n')
  for gks in graphkeyssplit:
    action.send_keys(gks)
    action.key_down(Keys.CONTROL)
    action.key_down(Keys.ALT)
    action.key_down('x')
    action.key_up(Keys.CONTROL)
    action.key_up(Keys.ALT)
    action.key_up('x')
  action.send_keys(CREDITS)
  action.key_down(Keys.ALT)
  action.key_down(Keys.SHIFT)
  action.key_down(Keys.UP)
  action.key_up(Keys.ALT)
  action.key_up(Keys.SHIFT)
  action.key_up(Keys.UP)
  action.perform()
  exprmodification=[]
  for s in settings:
    s='' if s=='' else s[1:-1].replace(" ","")
    li=filter(lambda v: '=' in v and v.split('=')[0].isalnum() and v.split('=')[0] not in ['id','type'], s.split(','))
    li0='{'+','.join('"'+v.split('=')[0]+'":'+v.split('=')[1].replace("'", "\"") for v in li)+'}'
    exprmodification.append(('{}' if li0=='' else li0))
  driver.execute_script("""mod=eval('"""+'['+','.join(exprmodification)+']'+"""'.replace('Calc',''))
function update(obj/*, …*/) {
    for (var i=1; i<arguments.length; i++) {
        for (var prop in arguments[i]) {
            var val = arguments[i][prop];
            if (typeof val == "object") // this also applies to arrays or null!
                update(obj[prop], val);
            else
                obj[prop] = val;
        }
    }
    return obj;
}
state=Calc.getState()
expressionss=state.expressions.list
updateexpr=[];
for (i=0; i<expressionss.length; i++){
objj=expressionss[i]
updateexpr.push(update(objj,mod[i]))
}
Calc.setExpressions(updateexpr)""")
  Graphupdate=''
  s2='' if Settings is None else Settings.replace(" ","")
  li2=filter(lambda v: '=' in v and v.split('=')[0].isalnum() and v.split('=')[0] not in ['bounds'], s2.split(','))
  li02='{'+','.join('"'+v.split('=')[0]+'":'+v.split('=')[1].replace("'", "\"") for v in li2)+'}'
  Graphupdate=[('{}' if li02=='' else li02)]
  li3=list(filter(lambda v: '=' in v and v.split('=')[0].isalnum() and v.split('=')[0] in ['bounds'], s2.split(',')))
  if len(li3)==1:
    li3 = li3[0]
    li03='{'+('"'+li3.split('=')[0]+'":'+str(li3.split('=')[1].split('|')).replace("'","\""))+'}'
    Graphupdate.append(('{}' if li03=='' else li03))
  driver.execute_script("""mod2=eval('["""+','.join(Graphupdate)+"""]'.replace('Calc',''))
Calc.updateSettings(mod2[0]);
if(mod2.length==2 && mod2[1].bounds.length==4){
Calc.setMathBounds({
  left: Number(mod2[1].bounds[0]),
  right: Number(mod2[1].bounds[1]),
  bottom: Number(mod2[1].bounds[2]),
  top: Number(mod2[1].bounds[3])
});
}""")
  saveg=r"""function SaveGraph(parenthash,graphhash,graphtitle,graphstate,thumbimg){
if(parenthash==undefined){parenthash="";}
if(graphtitle==undefined){graphtitle="Untitled Graph";}
fetch("https://www.desmos.com/api/v1/calculator/save", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"92\", \"Opera GX\";v=\"78\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://www.desmos.com/calculator/"+parenthash,
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "parent_hash="+parenthash+"&recovery_parent_hash="+parenthash+"&thumb_data="+thumbimg+"&graph_hash="+graphhash+"&my_graphs=false&is_update=false&title="+graphtitle+"&calc_state="+graphstate+"&lang=en",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
}"""
  dAhAsH=(randomcharlen(10) if dAhAsH is None else dAhAsH)+'0desmython'
  saveg2=saveg+"""\nlet parenthash0 = Calc._calc.globalHotkeys.mygraphsController.graphsController.currentGraph.hash ;
let graphhash0 = '"""+dAhAsH+"""';
let graphtitle0 = """+('Calc._calc.globalHotkeys.mygraphsController.graphsController.currentGraph.title' if Title=='undefined' else Title)
  saveg3=saveg2 + """;
let graphstate0 = encodeURIComponent(JSON.stringify(Calc.getState()));
let thumbimg0 = encodeURIComponent(Calc.screenshot({width:200, height:200 , targetPixelRatio: 2}));
SaveGraph(parenthash0,graphhash0,graphtitle0,graphstate0,thumbimg0);"""
  await asyncio.sleep(1)
  driver.execute_script(saveg3)
  await asyncio.sleep(1)
  return dAhAsH
  
def desmythonexpr(line):
  string=line
  if string.startswith('table '):
    string=desmotable2(string[6:])
  return(string)

async def compiledesmython(string,message):
  #
  daGmsg = await message.reply(embed=await getready(message))
  RecMsg = await record(message)
  #
  pattern=re.compile(r'!create *(?:"([A-Za-z0-9 \[\]]+)"(\?[a-z0-9]{10})?)?(?:\n\[!(.*)\])?\n+```.*\n([\s\S]*)\n?```')
  title=[ii.group(1) for ii in pattern.finditer(string)][0]
  hash=[ii.group(2) for ii in pattern.finditer(string)][0]
  hash=hash[1:] if hash is not None else hash
  settings=[ii.group(3) for ii in pattern.finditer(string)][0]
  graphcontent=[ii.group(4) for ii in pattern.finditer(string)][0]
  graphcontent=variablerep(graphcontent).split('\n')
  graphkeys=''
  patternfolder=re.compile(r'folder(?:\s*"(.+)")?')
  graphsettings=[]
  patternexprsettings=re.compile(r'\[!(.*)\] (.*)')
  for line in graphcontent:
    if line=='':
      graphkeys=graphkeys+'\ue015'
      graphsettings.append('')
    elif line[0]=='"' and line[-1]=='"':
      graphkeys=graphkeys+line[0:-1]+'\n'
      graphsettings.append('')
    elif line.startswith('/folder')==True:
      graphkeys=graphkeys+'\ue003'
    elif len(list(patternfolder.finditer(line)))==1:
      foldername=[ii.group(1) for ii in patternfolder.finditer(line)][0]
      foldername=''if foldername is None else foldername
      graphkeys=graphkeys+'folder'+foldername+'\n'
      graphsettings.append('')
    elif len(list(patternexprsettings.finditer(line)))==1 and line[:2]=='[!':
      graphsettings.append('{'+[ii.group(1) for ii in patternexprsettings.finditer(line)][0]+'}')
      graphkeys=graphkeys+desmythonexpr([ii.group(2) for ii in patternexprsettings.finditer(line)][0])+'\n'
    else:
      graphsettings.append('')
      graphkeys=graphkeys+desmythonexpr(line)+'\n'
  GraphCreated=await screenshotdes(graphkeys,graphsettings,settings,'"'+title+'"' if title is not None else 'undefined',hash)
  dGembed = nextcord.Embed(color=0x12793e, title='Graph creating using Desmython',description='https://www.desmos.com/calculator/'+GraphCreated)
  dGembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
  dGembed.set_image(url='https://saved-work.desmos.com/calc_thumbs/production/{}.png'.format(GraphCreated))
  daGmsg=await daGmsg.edit(embed=dGembed)
  RecMsg = await record(daGmsg,RecMsg)

'''asyncio.run(compiledesmython("""!create
[!xAxisArrowMode=Desmos.AxisArrowModes.BOTH,bounds=-20|10|-10|10]
```css
folder
a=0
a->a+sqrt(2^(sqrt(a+5))+2)+2
/folder
[!id=3,color=Desmos.Colors.GREEN,lineStyle='DOTTED'] cos(x)```"""))'''