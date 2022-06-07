from replit import db
import copy
import requests

#https://stackoverflow.com/questions/38491722/reading-a-github-file-using-python-returns-html-tags
def getDataURL(url0):
  req = requests.get(url0)
  if req.status_code == requests.codes.ok:
      req = req.json()
      print(len(req))
      return req
  else:
      print('Content was not found.')


ParentGraphsList=copy.deepcopy(getDataURL('https://raw.githubusercontent.com/DesmoSearch/Desmobot/main/DATA/ParentGraphsList'))
thetitles=copy.deepcopy(getDataURL('https://raw.githubusercontent.com/DesmoSearch/Desmobot/main/DATA/thetitles'))
GraphsList=copy.deepcopy(getDataURL('https://raw.githubusercontent.com/DesmoSearch/Desmobot/main/DATA/GraphsList'))
objowner=copy.deepcopy(getDataURL('https://raw.githubusercontent.com/DesmoSearch/Desmobot/main/DATA/objowner'))
bump={}
noofresults=5
GRAPHSCHANNEL=983620015246962688
def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    listOfElems=list(filter((None).__ne__, listOfElems))
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

