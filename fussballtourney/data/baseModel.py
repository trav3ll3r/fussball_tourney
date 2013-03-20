from fussballtourney.data import *

# BASE ENTITY
class BaseModel(ndb.Expando):
    created     = ndb.DateTimeProperty(auto_now=False, auto_now_add=True)
    updated     = ndb.DateTimeProperty(auto_now=True, auto_now_add=False)
