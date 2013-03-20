class RoleEnum:
    PLAYER  = 'PLAYER'
    ADMIN   = 'ADMIN'

class TableSideEnum:
    RANDOM  = 'RANDOM'
    RED     = 'RED'
    BLUE    = 'BLUE'

class TournamentStatusEnum:
    NEW         = 'NEW'
    STARTED     = 'STARTED'
    COMPLETED   = 'COMPLETED'

class TournamentTypeEnum:
    #SOURCE: http://www.afterschoolpa.com/typesoftournaments_a.html

    ROUND_ROBIN         = 'ROUND_ROBIN'     #DEFAULT
    SINGLE_ELIMINATION  = 'SINGLE_ELIMINATION'
    DOUBLE_ELIMINATION  = 'DOUBLE_ELIMINATION'
    UP_AND_DOWN         = 'UP_AND_DOWN'
    CONSOLIDATION       = 'CONSOLIDATION'
    LADDER              = 'LADDER'