from replit import db
import copy

ParentGraphsList=copy.deepcopy(db['ParentGraphsList'].value)
thetitles=copy.deepcopy(db['thetitles'].value)
GraphsList=copy.deepcopy(db['GraphsList'].value)
objowner=copy.deepcopy(db['objowner'].value)
bump={}
noofresults=5
def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    listOfElems=list(filter((None).__ne__, listOfElems))
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True