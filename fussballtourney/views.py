from fussballtourney import app
from flask import render_template, redirect, flash, url_for
from fussballtourney.data.models import *
from fussballtourney.forms import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournaments')
def tournaments():
    data = Tournament.gql('WHERE status = :pStatus', pStatus=TournamentStatusEnum.NEW).fetch(50)
    return render_template('tournaments.html', tournaments=data)

@app.route('/tournaments/new', methods = ['GET', 'POST'])
def new_tournament():
    form = TournamentForm()
    if form.validate_on_submit():
        tournament = Tournament(
            label = form.label.data,
            dateStart = form.dateStart.data
        )
        tournament.put()
#        flash('Tournament saved on database.')
        return redirect(url_for('tournaments'))

    return render_template('new_tournament.html', form=form)

@app.route('/tournaments/<tournamentId>')
def tournament(tournamentId):
    _tournament = Tournament.get_by_id(int(tournamentId))
    _players = getTournamentPlayers(_tournament.key).fetch(50)
    _teams = Team.gql("WHERE tournament = :pTournament", pTournament=_tournament.key).order(+Team.name).fetch(50)
    _games = Game.gql("WHERE tournament = :pTournament", pTournament=_tournament.key).order(+Game.created).fetch(50)

    return render_template('tournament.html', tournament=_tournament, players=_players, teams=_teams, games=_games)

@app.route('/tournaments/<tournamentId>/players/new', methods = ['GET', 'POST'])
def new_player(tournamentId):
    _tournament = Tournament.get_by_id(int(tournamentId))

    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(
            #parent = _tournament.key,
            tournament = _tournament.key,
            nickname = form.nickname.data
        )
        player.put()
#        flash('Player saved on database.')
        return redirect('/tournaments/' + tournamentId)

    form.tournament = _tournament
    return render_template('new_player.html', form=form)

@app.route('/tournaments/<tournamentId>/teams/new', methods = ['GET', 'POST'])
def new_team(tournamentId):
    _tournament = Tournament.get_by_id(int(tournamentId))

    form = TeamForm()
    if form.validate_on_submit():
        _playerAttId = int(form.playerAttId.data)
        _playerDefId = int(form.playerDefId.data)
        _teamName    = form.teamName.data

        _playerAtt = Player.get_by_id(_playerAttId)
        _playerDef = Player.get_by_id(_playerDefId)

        team = Team(
            tournament = _tournament.key,
            playerAtt = _playerAtt.key,
            playerDef = _playerDef.key,
            name = _teamName
        )
        team.put()
        #        flash('Player saved on database.')
        return redirect('/tournaments/' + tournamentId)

    _players = getTournamentPlayers(_tournament.key).fetch(50)

    form.tournament = _tournament
    form.players    = _players

    return render_template('new_team.html', form=form)

@app.route('/tournaments/<tournamentId>/games/new', methods = ['GET', 'POST'])
def new_game(tournamentId):
    _tournament = Tournament.get_by_id(int(tournamentId))

    form = GameForm()
    if form.validate_on_submit():
        _playerBlueAttId = int(form.playerBlueAttId.data)
        _playerBlueDefId = int(form.playerBlueDefId.data)
        _playerRedAttId  = int(form.playerRedAttId.data)
        _playerRedDefId  = int(form.playerRedDefId.data)

        _teamBlue = getTournamentTeamByPlayers(_tournament.key, _playerBlueAttId, _playerBlueDefId)
        _teamRed  = getTournamentTeamByPlayers(_tournament.key, _playerRedAttId , _playerRedDefId )

        game = Game(
            tournament = _tournament.key,
            teamBlue   = _teamBlue.key,
            teamRed    = _teamRed.key
        )
        game.put()

#        flash('Player saved on database.')
        return redirect('/tournaments/' + tournamentId)

    _players = getTournamentPlayers(_tournament.key).fetch(50)

    form.tournament = _tournament
    form.players    = _players
    return render_template('new_game.html', form=form)

@app.route('/tournaments/<tournamentId>/games/<gameId>', methods = ['GET', 'POST'])
def game(tournamentId, gameId):
    _tournament = Tournament.get_by_id(int(tournamentId))
    _game       = Game.get_by_id(int(gameId))
    _scores     = getGameScores(_game.key)

    return render_template('game.html', tournament=_tournament, game=_game, scores=_scores)

@app.route('/tournaments/<tournamentId>/games/<gameId>/scores/new/player/<playerId>', methods = ['GET', 'POST'])
def new_score(tournamentId, gameId, playerId):
    _tournament = Tournament.get_by_id(int(tournamentId))
    _game       = Game.get_by_id(int(gameId))
    _player     = Player.get_by_id(int(playerId))

    form = ScoreForm()
    if form.validate_on_submit():
        _team = None

        isOwnGoal = bool(form.ownGoal.data)

        # check if player belongs to BLUE team
        if _player.key == _game.teamBlue.get().playerDef or _player.key == _game.teamBlue.get().playerAtt:
            if isOwnGoal:
                _team = _game.teamRed
            else:
                _team = _game.teamBlue

        # check if player belongs to RED team
        if _player.key == _game.teamRed.get().playerDef or _player.key == _game.teamRed.get().playerAtt:
            if isOwnGoal:
                _team = _game.teamBlue
            else:
                _team = _game.teamRed

        if _team is not None:
            score = Score(
                game    = _game.key,
                player  = _player.key,
                team    = _team,
                ownGoal = isOwnGoal
            )
            score.put()
            return redirect('tournaments/' + tournamentId + '/games/' + gameId)

    form.tournament   = _tournament
    form.game         = _game
    form.player       = _player
    form.ownGoal.data = False
    return render_template('new_score.html', form=form)

def getTournamentPlayers(tournamentKey):
    result = Player.gql("WHERE tournament = :pTournament", pTournament=tournamentKey).order(+Player.nickname)
    return result

def getTournamentTeamByPlayers(tournamentKey, playerAttId, playerDefId):
    _playerAtt = Player.get_by_id(playerAttId)
    _playerDef = Player.get_by_id(playerDefId)

    result = Team.gql("WHERE tournament = :pTournament AND playerAtt = :pPlayerAtt AND playerDef = :pPlayerDef",
        pTournament = tournamentKey,
        pPlayerAtt  = _playerAtt.key,
        pPlayerDef  = _playerDef.key
    ).get()

    if result is None:
        #create team and return it
        team = Team(
            tournament = tournamentKey,
            playerAtt  = _playerAtt.key,
            playerDef  = _playerDef.key,
            name       = _playerAtt.nickname + " / " + _playerDef.nickname
        )
        team.put()

        result = team

    return result

def getGameScores(gameKey):
    result = Score.gql("WHERE game = :pGame", pGame=gameKey).order(+Score.created)
    return result