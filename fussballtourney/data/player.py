from fussballtourney.data import *

class Player(BaseModel):
    tournament  = ndb.KeyProperty(kind=Tournament, required=True, repeated=False)
    nickname    = ndb.StringProperty(required=True, indexed=True)
