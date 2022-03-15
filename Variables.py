from replit import db
import copy

ParentGraphsList=copy.deepcopy(db['ParentGraphsList'].value)
thetitles=copy.deepcopy(db['thetitles'].value)
GraphsList=copy.deepcopy(db['GraphsList'].value)
objowner=copy.deepcopy(db['objowner'].value)