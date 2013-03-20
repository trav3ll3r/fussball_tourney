from flask import Flask
from util.ProduceJson import ProduceJson
import settings

app = Flask('fussballtourney')
app.config.from_object('fussballtourney.settings')

import views

#app.add_url_rule('/', view_func=views.index)
#@ProduceJson
#app.add_url_rule('/tournaments', view_func=views.tournaments)