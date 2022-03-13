from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import difflib
import pylatexenc
from pylatexenc.latex2text import LatexNodes2Text
def getinfo(hashurl):
  if "*" in hashurl or '$' in hashurl:
    return {}
  html = urlopen(hashurl).read()
  soup = BeautifulSoup(html, features="html.parser")
  finaldict={}
  if 'graph' in json.loads(soup.body['data-load-data']).keys():
    for key in [x for x in ['hash','parent_hash','thumbUrl','stateUrl','title','access','created'] if x in json.loads(soup.body['data-load-data'])['graph'].keys()]:
      finaldict[key]=json.loads(soup.body['data-load-data'])['graph'][key]
    finaldict['version']='null'
    dastate=json.loads(soup.body['data-load-data'])['graph']['state']
    if 'version' in dastate.keys():
      finaldict['version']=dastate['version']
    if 'expressions' in dastate.keys():
      expr=dastate['expressions']['list']
      finaldict['expressions'] = expr
      finaldict['notes'], finaldict['folders']=[],[]
      finaldict['notes']=[expr[i] for i in range(len(expr)) if expr[i]['type' if 'type' in expr[i] else 'id']=='text']
      finaldict['folders']=[expr[i] for i in range(len(expr)) if expr[i]['type' if 'type' in expr[i] else 'id']=='folder']
      patternvar = re.compile(r"([A-Za-z](?:_{?\w*}?)?)=")
      finaldict['variables']=list(set([ii.group(1) for ii in patternvar.finditer(str(expr))]))
  return (finaldict)


def difference (graph1,graph2):
  getinfo1=getinfo('https://www.desmos.com/calculator/'+graph1)
  getinfo2=getinfo('https://www.desmos.com/calculator/'+graph2)
  Expressions = lambda getinf: [f"[#{exp['id']}] {exp['latex' if 'latex' in exp.keys() else ('text' if 'text' in exp.keys() else 'title')]}" for exp in getinf['expressions'] if ('latex' in exp.keys() or 'text' in exp.keys() or 'title' in exp.keys())]
  Type = lambda getinf: ['expression' if 'latex' in exp.keys() else ('note' if 'text' in exp.keys() else 'folder') for exp in getinf['expressions'] if ('latex' in exp.keys() or 'text' in exp.keys() or 'title' in exp.keys())]

  Expressions01 = [convert0(exp) for exp in Expressions(getinfo1)]
  Expressions02 = [convert0(exp) for exp in Expressions(getinfo2)]

  diffx = difflib.ndiff(Expressions01,Expressions02)
  diff2x=[]
  getidx=-1
  for changex in diffx:

    if changex[0] in ["-","+","?"]:
      getid0x = re.match('[+-\?] (\[.*?\])',changex)
      if (getid0x is None):
        diff2x[-1]=diff2x[-1]+'\n'+changex
      else:
        if getidx==getid0x.group(1):
          diff2x[-1]=diff2x[-1]+'\n'+changex
        else:
          diff2x.append(changex)
          getidx=getid0x.group(1)
    else:
      if graph1==graph2:   
        diff2x.append(changex)
  diff2x = ['```diff\n'+dif+'```' for dif in diff2x]
  
  Expressions1 = [exp for exp in Expressions(getinfo1)]
  Expressions2 = [exp for exp in Expressions(getinfo2)]
  Type1 = Type(getinfo1)

  text1_lines, text2_lines = Expressions1, Expressions2
  diff = difflib.ndiff(text1_lines, text2_lines)
  sm = difflib.SequenceMatcher(a=text1_lines, b=text2_lines)
  diff2=[]
  getid=-1
  for change in diff:
    if change[0] in ["-","+","?"]:
      getid0 = re.match('[+-\?] (\[.*?\])',change)
      if (getid0 is None):
        diff2[-1]=diff2[-1]+'\n'+change
      else:
        if getid==getid0.group(1):
          diff2[-1]=diff2[-1]+'\n'+change
        else:
          diff2.append(change)
          getid=getid0.group(1)
    else:
      if graph1==graph2:   
        diff2.append(change)
  diff2 = ['```diff\n'+dif+'```' for dif in diff2]
  
  return([sm.ratio(),diff2,getinfo1['parent_hash'],Type1,diff2x])

from pylatexenc import macrospec, latexwalker, latex2text
#https://github.com/phfaist/pylatexenc/issues/36
def convert0(latex_text):
  lwc = latexwalker.get_default_latex_context_db()
  lwc.add_context_category('powers', specials=[
      macrospec.SpecialsSpec('^', args_parser=macrospec.MacroStandardArgsParser('{')),
      macrospec.SpecialsSpec('_', args_parser=macrospec.MacroStandardArgsParser('{')),
  ])
  
  # define the replacement string for ^
  l2tc = latex2text.get_default_latex_context_db()
  l2tc.add_context_category('powers', specials=[
      latex2text.SpecialsTextSpec('^', simplify_repl='^(%s)'),
      latex2text.SpecialsTextSpec('_', simplify_repl='_(%s)'),
  ])
  
  latex_text = r'{}'.format(latex_text)
  
  lw = latexwalker.LatexWalker(latex_text, latex_context=lwc)
  l2t = latex2text.LatexNodes2Text(latex_context=l2tc)
  
  return(l2t.nodelist_to_text(lw.get_latex_nodes()[0]))