from fussballtourney.data import *

# SYSTEM ENTITY
class User(BaseModel):
    username    = ndb.StringProperty(required=True, indexed=True)
    nickname    = ndb.StringProperty(required=True)
    password    = ndb.StringProperty(required=True)
    role        = ndb.StringProperty(default=RoleEnum.PLAYER)

# BUSINESS ENTITIES
class Team(BaseModel):
    tournament  = ndb.KeyProperty(kind=Tournament, required=True, repeated=False, indexed=True)
    playerDef   = ndb.KeyProperty(kind=Player, required=True, repeated=False)
    playerAtt   = ndb.KeyProperty(kind=Player, required=True, repeated=False)
    name        = ndb.StringProperty(required=True, indexed=True)

class Game(BaseModel):
    tournament  = ndb.KeyProperty(kind=Tournament, required=True, indexed=True)
    teamRed     = ndb.KeyProperty(kind=Team, required=True)
    teamBlue    = ndb.KeyProperty(kind=Team, required=True)

class Score(BaseModel):
    game        = ndb.KeyProperty(kind=Game, required=True, indexed=True)
    player      = ndb.KeyProperty(kind=Player, required=True)
    team        = ndb.KeyProperty(kind=Team, required=True)
    ownGoal     = ndb.BooleanProperty(default=False)