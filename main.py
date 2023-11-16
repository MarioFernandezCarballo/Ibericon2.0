from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from flask_login import login_required
from utils import createApp, createDatabase, decorators

from bpGeneric import genericBP
from bpAuth import authBP
from bpTeam import teamBP
from bpClub import clubBP
from bpUser import userBP
from bpFaction import factionBP
from bpTournament import tournamentBP

# API
from api.bpApiAdmin import adminApiBP
from api.bpApiAuth import authApiBP
from api.bpApiUser import userApiBP
from api.bpApiClub import clubApiBP
from api.bpApiFaction import factionApiBP
from api.bpApiTeam import teamApiBP
from api.bpApiTournament import tournamentApiBP

info = Info(title="Ibericon API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Ibericon 1.0
#app.register_blueprint(genericBP)
#app.register_blueprint(authBP)
#app.register_blueprint(adminBP)
#app.register_blueprint(teamBP)
#app.register_blueprint(clubBP)
#app.register_blueprint(userBP)
#app.register_blueprint(factionBP)
#app.register_blueprint(tournamentBP)

# API
app.register_api(adminApiBP)
app.register_api(authApiBP)
app.register_api(userApiBP)
app.register_api(clubApiBP)
app.register_api(factionApiBP)
app.register_api(teamApiBP)
app.register_api(tournamentApiBP)

app = createApp(app)
createDatabase(app)


# Ibericon 2.0
# Generic
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    from flask import render_template
    from flask_login import current_user
    from utils import getUsers, getClubs, getAllTournaments
    usr = getUsers()
    clb = getClubs()
    tour = getAllTournaments()
    tours = [{
        "bcpUri": u.Tournament.bcpUri,
        "name": u.Tournament.name,
        "date": u.Tournament.date,
        "rounds": u.Tournament.rounds,
        "players": len(u.Tournament.users),
        "conference": u.Conference.name,
        "imgUri": u.Tournament.imgUri
    } for u in tour if not u.Tournament.isFinished]
    return render_template(
        'general.html',
        title="General",
        users=usr,
        clubs=clb,
        tournaments=tours,
        numUsers=len(usr),
        numTour=len(tour),
        amountGolden=50,  # TODO gestionar esto
        amountTrips=60,
        user=current_user if not current_user.is_anonymous else None
    )


@app.route('/about', methods=['GET', 'POST'])
def about():
    from flask import render_template
    from flask_login import current_user
    from utils import getAllTournaments
    tors = getAllTournaments()
    tors = [{
        "bcpUri": u.Tournament.bcpUri,
        "name": u.Tournament.name,
        "date": u.Tournament.date,
        "rounds": u.Tournament.rounds,
        "players": len(u.Tournament.users),
        "conference": u.Conference.name,
        "imgUri": u.Tournament.imgUri
    } for u in tors if not u.Tournament.isFinished]
    return render_template(
        'about.html',
        title="About",
        tournaments=tors,
        user=current_user if not current_user.is_anonymous else None
    )


# Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from flask import render_template, request, redirect, url_for
    from flask_login import current_user
    from utils import getUserOnly, getUserConference, updateProfile, getUserMostPlayedFaction, getUserMostPlayedClub, getUserLastFaction, getConferences
    if request.method == 'POST':
        return updateProfile(current_user, request.form)
    usr = getUserOnly(current_user.id)
    if usr:
        conference = getUserConference(usr.conference)
        mostCommon = getUserMostPlayedFaction(usr)
        lastFaction = getUserLastFaction(usr)
        club = getUserMostPlayedClub(usr)
        conferences = getConferences()
        return render_template(
            'profile.html',
            title=usr.bcpName,
            conference=conference,
            last=lastFaction,
            common=mostCommon,
            club=club,
            usr=usr,
            conferences=conferences,
            user=current_user if not current_user.is_anonymous else None
        )
    return redirect(url_for('dashboard'))


@app.route('/position', methods=['GET', 'POST'])
@login_required
def position():
    from flask import render_template, request, redirect, url_for
    from flask_login import current_user
    from utils import getUserConferencePosition, getUserFactions, getUserGlobalPosition, getUserOnly, getUserConference, updateProfile, getUserMostPlayedFaction, getUserMostPlayedClub, getUserLastFaction, getPastTournamentsByUser, getFutureTournamentsByUser
    if request.method == 'POST':
        return updateProfile(current_user, request.form)
    usr = getUserOnly(current_user.id)
    if usr:
        conference = getUserConference(usr.conference)
        mostCommon = getUserMostPlayedFaction(usr)
        lastFaction = getUserLastFaction(usr)
        ratesFactions = getUserFactions(usr)
        club = getUserMostPlayedClub(usr)
        future = getFutureTournamentsByUser(usr)
        past = getPastTournamentsByUser(usr)
        globalClass = getUserGlobalPosition(usr)
        conferenceClass = getUserConferencePosition(usr)
        return render_template(
            'position.html',
            title=usr.bcpName,
            conference=conference,
            last=lastFaction,
            common=mostCommon,
            club=club,
            usr=usr,
            future=future,
            past=past,
            globalClass=globalClass,
            conferenceClass=conferenceClass,
            ratesFactions=ratesFactions,
            user=current_user if not current_user.is_anonymous else None
        )
    return redirect(url_for('dashboard'))

#Auth
@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import request, render_template
    from flask_login import current_user
    from utils.auth import userLogin
    if request.method == 'POST':
        response, _ = userLogin(request.form)
        return response
    return render_template('login.html', title="Login", user=current_user if not current_user.is_anonymous else None)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    from flask import request, render_template
    from flask_login import current_user
    from utils.auth import userSignup
    from utils.city import getCities
    cities = getCities()
    if request.method == 'POST':
        response, _ = userSignup(request.form)
        return response
    return render_template('signup.html', title="Registro", cities=cities, user=current_user if not current_user.is_anonymous else None)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    from utils.auth import resetUserInfo
    response, _ = resetUserInfo()
    return response


#Admin
@app.route('/get-tournaments', methods=['GET'])
@decorators.only_collaborator
def getTournaments():
    from flask import redirect, url_for
    from utils.admin import getFutureTournaments
    getFutureTournaments()
    return redirect(url_for('dashboard'))


@app.route('/check-tournaments', methods=['GET'])
@decorators.only_collaborator
def checkTournamentsAdmin():
    from flask import redirect, url_for
    from utils.admin import checkTournaments
    checkTournaments()
    return redirect(url_for('dashboard'))


@app.route('/update-stats', methods=['GET'])
@decorators.only_collaborator
def updateStatsAdmin():
    from flask import redirect, url_for
    from utils.admin import updateStats
    updateStats()
    return redirect(url_for('dashboard'))


# Tournaments
@app.route("/tournaments", methods={"GET", "POST"})
def tournamentsEndPoint():
    from flask import render_template
    from flask_login import current_user
    from utils import getAllTournaments
    tors = getAllTournaments()
    tors = [{
        "bcpUri": u.Tournament.bcpUri,
        "name": u.Tournament.name,
        "date": u.Tournament.date,
        "rounds": u.Tournament.rounds,
        "players": len(u.Tournament.users),
        "conference": u.Conference.name,
        "imgUri": u.Tournament.imgUri
    } for u in tors if not u.Tournament.isFinished]
    return render_template(
        'tournaments.html',
        title="Torneos",
        user=current_user if not current_user.is_anonymous else None,
        tournaments=tors
    )


# Ranking
@app.route("/ranking", methods={"GET", "POST"})
def ranking():
    from flask import render_template
    from flask_login import current_user
    from utils import getUsers, getClubs
    usr = getUsers()
    cls = getClubs()
    usr = [{"id": u.id, "profilePic": u.profilePic, "bcpName": u.bcpName, "ibericonScore": u.ibericonScore} for u in usr]
    cls = [{"id": c.id, "profilePic": c.profilePic, "bcpName": c.name, "ibericonScore": c.ibericonScore} for c in cls]
    return render_template(
        'ranking.html',
        title="Jugadores",
        users=usr,
        teams=cls,
        user=current_user if not current_user.is_anonymous else None
    )


# Winrates
@app.route("/winrates", methods={"GET", "POST"})
def winRatesEndPoint():
    from flask import render_template
    from flask_login import current_user
    from utils import getUsersWinRate
    usr = getUsersWinRate()
    usr = [{"id": u.id, "profilePic": u.profilePic, "bcpName": u.bcpName, "winRate": u.winRate} for u in usr if u.winRate]
    return render_template(
        'winrates.html',
        title="Winrates",
        users=usr,
        user=current_user if not current_user.is_anonymous else None
    )

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])



# TODO que pasa si alguien se cambia el mail de bcp? no se puede logar con el viejo pero guarda el bcpid...
# TODO gestionar el posible cambio de ciudad/conferencia de los jugadores con un many to many
#  Imagen default cuando se registran.

# TODO ver torneos una vez al dia
# TODO check torneos una vez al domingo
