from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from flask_login import login_required
from utils import createApp, createDatabase, decorators

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
        amountGolden=app.config['MONEY'],
        amountTrips=app.config['PERCENTAGE'],
        user=current_user if not current_user.is_anonymous else None
    )
@app.route("/ranking", methods={"GET", "POST"})
def ranking():
    from flask import render_template
    from flask_login import current_user
    from utils import getUsers, getClubs
    usr = getUsers()
    cls = getClubs()
    usr = [{"id": u.id, "conference": u.conference, "profilePic": u.profilePic, "bcpName": u.bcpName, "ibericonScore": u.ibericonScore} for u in usr]
    cls = [{"id": c.id, "conference": "caca","profilePic": c.profilePic, "bcpName": c.name, "ibericonScore": c.ibericonScore} for c in cls]
    return render_template(
        'ranking.html',
        title="Jugadores",
        users=usr,
        norte=[u for u in usr if u['conference']=='Norte'],
        noreste=[u for u in usr if u['conference']=='Noreste'],
        este=[u for u in usr if u['conference']=='Este'],
        centro=[u for u in usr if u['conference']=='Centro'],
        sur=[u for u in usr if u['conference']=='Sur'],
        teams=cls,
        user=current_user if not current_user.is_anonymous else None
    )
@app.route("/winrates", methods={"GET", "POST"})
def winRatesEndPoint():
    from flask import render_template
    from flask_login import current_user
    from utils import getUsersWinRate, getFactions
    usr = getUsersWinRate()
    fct, _ = getFactions()
    usr = [{"id": u.id, "profilePic": u.profilePic, "bcpName": u.bcpName, "winRate": u.winRate} for u in usr if u.winRate]
    fct = [{"id": f.id, "bcpName": f.name, "winRate": f.winRate, "pickRate": f.pickRate} for f in sorted(fct, key=lambda d: d.winRate, reverse=True) if f.winRate]
    return render_template(
        'winrates.html',
        title="Winrates",
        users=usr,
        factions=fct,
        user=current_user if not current_user.is_anonymous else None
    )
# User
@app.route("/user/<us>", methods={"GET", "POST"})
def userEndPoint(us):
    from flask import render_template, redirect, url_for
    from flask_login import current_user
    from utils import getUserConferencePosition, getUserFactions, getUserGlobalPosition, getUserOnly, getUserConference, \
        getUserMostPlayedFaction, getUserMostPlayedClub, getUserLastFaction, getPastTournamentsByUser, \
        getFutureTournamentsByUser
    if not current_user.is_anonymous:
        if int(us) == current_user.id:
            return redirect(url_for('position'))
    usr = getUserOnly(us)
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
            'user.html',
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
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from flask import render_template, request, redirect, url_for
    from flask_login import current_user
    from utils import getUserOnly, getUserConference, updateProfile, getUserMostPlayedFaction, getUserMostPlayedClub, getUserLastFaction, getConferences
    if request.method == 'POST':
        updateProfile(current_user, request.form)
        return redirect(url_for('profile'))
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
@app.route('/new-image', methods=['POST'])
@login_required
def newImage():
    from flask import make_response, request
    from flask_login import current_user
    from utils import updatePicture
    if request.method == 'POST':
        return make_response("result", updatePicture(current_user, request.files))
    return make_response("Not ok", 400)
@app.route('/position', methods=['GET', 'POST'])
@login_required
def position():
    from flask import render_template, redirect, url_for
    from flask_login import current_user
    from utils import getUserConferencePosition, getUserFactions, getUserGlobalPosition, getUserOnly, getUserConference, getUserMostPlayedFaction, getUserMostPlayedClub, getUserLastFaction, getPastTournamentsByUser, getFutureTournamentsByUser
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
# Faction
@app.route("/faction/<fact>", methods={"GET"})
def factionEndPoint(fact):
    from flask import render_template
    from flask_login import current_user
    from utils import getFactionOnly, getFaction
    faction = getFactionOnly(fact)
    fct = getFaction(fact)
    return render_template(
        'faction.html',
        title=faction.name,
        user=current_user if not current_user.is_anonymous else None,
        faction=fct,
        fctOnly=faction
    )
# Club
@app.route("/club/<cl>", methods={"GET"})
def clubEndPoint(cl):
    from flask import render_template
    from flask_login import current_user
    from utils import getClubOnly, getClub
    club = getClubOnly(cl)
    clTor = getClub(cl)
    return render_template(
        'club.html',
        title=club.name,
        club=club,
        clTor=clTor,
        user=current_user if not current_user.is_anonymous else None
    )
#Auth
@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import request, render_template
    from flask_login import current_user
    from utils.auth import userLogin
    from utils.city import getCities
    cities = getCities()
    if request.method == 'POST':
        response, _ = userLogin(request.form)
        return response
    return render_template('landing.html', title="Login", cities=cities, user=current_user if not current_user.is_anonymous else None)
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
@app.route("/add/tournament", methods={"GET", "POST"})
@login_required
@decorators.only_collaborator
def addNewTournamentAdmin():
    from flask import request, flash, render_template, redirect, url_for
    from flask_login import current_user
    from utils.admin import updateStats
    from api.bpApiAdmin.utils import newTournamentApi
    if request.method == 'POST':
        response = newTournamentApi(request.form['uri'])
        if response.status == 200:
            if updateStats().status == 200:
                flash("OK")
            else:
                flash("No OK")
        else:
            flash("No OK")
        return redirect(url_for('dashboard'))
    return render_template(
        'add.html',
        title="Añadir Torneo",
        user=current_user if not current_user.is_anonymous else None
    )
@app.route("/collaborator", methods={"GET", "POST"})
@login_required
@decorators.only_collaborator
def collaboratorAdmin():
    from flask import request, flash, render_template, redirect, url_for
    from flask_login import current_user
    from utils.admin import updateThings
    if request.method == 'POST':
        response = updateThings(request.form)
        if response.status == 200:
            flash("OK")
        else:
            flash("No OK")
        return redirect(url_for('dashboard'))
    return render_template(
        'collaborator.html',
        title="Espacio de colaborador",
        user=current_user if not current_user.is_anonymous else None
    )

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

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
