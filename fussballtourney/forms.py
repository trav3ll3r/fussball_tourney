from flaskext import wtf
from flaskext.wtf import validators

class TournamentForm(wtf.Form):
    label     = wtf.TextField('Label'     , validators=[validators.Required()])
    dateStart = wtf.TextField('Date Start', validators=[])

class PlayerForm(wtf.Form):
    nickname   = wtf.TextField('Player nickname', validators=[validators.Required()])

class TeamForm(wtf.Form):
    teamName    = wtf.TextField('Team name', validators=[])
    playerAttId = wtf.TextField('Attacker' , validators=[validators.Required()])
    playerDefId = wtf.TextField('Defender' , validators=[validators.Required()])

class GameForm(wtf.Form):
    playerBlueAttId = wtf.TextField('Blue Attacker', validators=[validators.Required()])
    playerBlueDefId = wtf.TextField('Blue Defender', validators=[validators.Required()])
    playerRedAttId  = wtf.TextField('Red Attacker' , validators=[validators.Required()])
    playerRedDefId  = wtf.TextField('Red Defender' , validators=[validators.Required()])

class ScoreForm(wtf.Form):
    ownGoal = wtf.BooleanField('Own Goal?', validators=[])