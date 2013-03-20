from fussballtourney.data import *

class Tournament(BaseModel):
    label       = ndb.StringProperty(required=True)
    dateStart   = ndb.StringProperty(required=False)
    type        = ndb.StringProperty(default=TournamentTypeEnum.ROUND_ROBIN)
    status      = ndb.StringProperty(default=TournamentStatusEnum.NEW)