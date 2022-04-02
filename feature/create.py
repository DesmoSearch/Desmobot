from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import asyncio
import re
from setup import getready, record
import nextcord
from replit import db

from random import choice
def randomcharlen(leng):
  return(''.join(map(choice,["bcdfghjklmnpqrstvwxz7","aeiouyaeiouy0"]*int(leng/2))))

def variablerep(string):
  string=re.sub('(\) *[\^\/] *\(.*\))','\\1\ue014',string)
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

async def screenshotdes(graphkeys,settings,Settings,Title,dAhAsH,importasfolder,URL='https://www.desmos.com/calculator'):
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options=chrome_options)
  
  driver.get(URL)
  await asyncio.sleep(3)
  selectfirst=driver.find_element(By.CLASS_NAME, "dcg-mq-root-block")
  action =  ActionChains(driver);
  action.click(on_element = selectfirst)
  
  graphkeyssplit=graphkeys.split('\n')
  if graphkeyssplit[-1]=='':
    graphkeyssplit.pop()
  for gks in graphkeyssplit:
    action.send_keys(gks)
    action.key_down(Keys.CONTROL)
    action.key_down(Keys.ALT)
    action.key_down('x')
    action.key_up(Keys.CONTROL)
    action.key_up(Keys.ALT)
    action.key_up('x')
  action.key_down(Keys.ALT)
  action.key_down(Keys.SHIFT)
  action.key_down(Keys.UP)
  action.key_up(Keys.ALT)
  action.key_up(Keys.SHIFT)
  action.key_up(Keys.UP)
  action.perform()
  
  #
  importthem="""importdata=eval(\""""+str(importasfolder)+"""\")
function computeContext(state) {
  const calculator = new Desmos.GraphingCalculator();
  calculator.setState(state);
  // Emulate what happens in the web worker
  const Context = require("core/math/context").Context;
  const context = new Context();
  const changeSet = {
    isCompleteState: true,
    statements: {},
  };
  for (let stmt of calculator.controller.getAllItemModels()) {
    if (stmt.type !== "expression") continue;
    changeSet.statements[stmt.id] = stmt;
  }
  const ticker = Calc.controller.listModel.ticker.cachedParsableState;
  if (ticker.handlerLatex) {
    changeSet.statements[ticker] = ticker;
  }
  context.processChangeSet(changeSet);
  context.updateAnalysis();
  return context;
}
state=Calc.getState()
for(gi=0;gi<importdata.length;gi++){
    state.expressions.list.push({id:importdata[gi][2],type:'folder',collapsed: true,title:'imported '+importdata[gi][0]+'\\n('+importdata[gi][1]+')\\nhttps://www.desmos.com/calculator/'+importdata[gi][2]})
    try {
        json0 = await (
            await fetch(`https://www.desmos.com/calculator/`+importdata[gi][2], {
                headers: {
                    Accept: "application/json",
                },
            })
        ).json()
        ctx=computeContext(json0.state);
        fandvtobeimported=importdata[gi][4]
        for (const vard0 of fandvtobeimported){
            vard=ctx.frame[vard0]
            if(vard){
            if (vard.userData){
                Depend=vard._dependencies.filter((e) => !vard._dummyDependencies.includes(e)&&(e.includes('_')||(e.length==1&&e!='e')))
                fandvtobeimported.push.apply(fandvtobeimported,Depend)
            }}
        }
        
        fandvtobeimported=fandvtobeimported.filter((x, i, a) => a.indexOf(x) == i)
        //console.log(fandvtobeimported)
        xyz=fandvtobeimported.map(function(y){
                x=json0.state.expressions.list[ctx.frame[y].userData.index]
                x.folderId=importdata[gi][2];
                if (x.type=='expression'){
                    if(x.latex!=undefined){
                        x.latex = x.latex.replace(/(.)_{([A-Za-z0-9]*)}/g, '$1_{$2'+importdata[gi][3]+'}')
                    }
                }
                return(x)
        })
        state.expressions.list.push.apply(state.expressions.list,xyz)
        
    } catch (err) {}
}
state.expressions.list.push({id:'credit',type:'text',text:'Graph created using https://github.com/DesmoSearch/Desmobot discord bot | MathEnthusiast314'})
Calc.setState(state);"""
  
  driver.execute_script(importthem)
  #
  
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
  saveg=db['saveg']
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
  pattern=re.compile(r'!create *(?:"([A-Za-z0-9 \[\]]+)"(\?[a-z0-9]{10})?)?(?:\n\[!(.*)\])?\n+```.*\n(?:import +([A-Za-z0-9\.\,! ]+) +as +([A-Za-z0-9\, ]+)\n)?([\s\S]*?)\n?```')
  title=[ii.group(1) for ii in pattern.finditer(string)][0]
  hash=[ii.group(2) for ii in pattern.finditer(string)][0]
  hash=hash[1:] if hash is not None else hash
  settings=[ii.group(3) for ii in pattern.finditer(string)][0]
  graphcontent=[ii.group(6) for ii in pattern.finditer(string)][0]
  
  modulesl=[ii.group(4) for ii in pattern.finditer(string)][0]
  moduleas=[ii.group(5) for ii in pattern.finditer(string)][0]
  #
  importasfolder=[]
  if modulesl is not None and moduleas is not None:
    moduleslL=re.split(' *, *',modulesl)
    moduleasL=re.split(' *, *',moduleas)
    if len(moduleslL)==len(moduleasL):
      from setup import dmodulelist
      for modname, modas in zip(moduleslL,moduleasL):
        thetup=[ele for ele in dmodulelist if ele[2]==modname or ele[3]==modname]
        if len(thetup)>0:
          varorfunc=[ii.group(2)+'_'+ii.group(3) for ii in re.finditer('('+str(modas)+')'+'\.([A-Za-z0-9])([A-Za-z0-9]*)',graphcontent)]
          graphcontent=re.sub('('+str(modas)+')'+'\.([A-Za-z0-9])([A-Za-z0-9]*)','\\2_\\3\\1',graphcontent)
          importasfolder.append([thetup[0][3],thetup[0][2],thetup[0][1].fields[0].value.replace('https://www.desmos.com/calculator/',''),modas,varorfunc])
  graphcontent=variablerep(graphcontent).split('\n')
  #
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
  GraphCreated=await screenshotdes(graphkeys,graphsettings,settings,'"'+title+'"' if title is not None else 'undefined',hash,importasfolder)
  dGembed = nextcord.Embed(color=0x12793e, title='Graph created using Desmython',description='https://www.desmos.com/calculator/'+GraphCreated)
  dGembed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
  dGembed.set_image(url='https://saved-work.desmos.com/calc_thumbs/production/{}.png'.format(GraphCreated))
  daGmsg=await daGmsg.edit(embed=dGembed)
  RecMsg = await record(daGmsg,RecMsg)

'''asyncio.run(compiledesmython("""!create
[!xAxisArrowMode=Desmos.AxisArrowModes.BOTH,bounds=-20|10|-10|10]
```css
import me314.complex as 2d
folder
a=0
a->a+sqrt(2^(sqrt(a+5))+2)+2
/folder
distance((2,0),2d.Power((x,y),(2,1)))=2
[!id=3,color=Desmos.Colors.GREEN,lineStyle='DOTTED'] cos(x)```"""))'''