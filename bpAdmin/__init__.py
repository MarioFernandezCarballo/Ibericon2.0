import os
from flask_openapi3 import APIBlueprint
from flask import Blueprint, redirect, url_for, current_app, request, flash, render_template
from flask_login import login_required, current_user

from utils.general import updateStats, updateAlgorythm
from utils.user import setPlayerPermission, getUserOnly
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import addNewTournament, deleteTournament

adminBP = APIBlueprint('adminBluePrint', __name__)


@adminBP.route("/user/<us>/permission", methods={"GET", "POST"})
@login_required
@only_left_hand
def changePlayerPermissionsEndPoint(us):
    if request.method == "POST":
        if setPlayerPermission(current_app.config["database"], us, request.form):
            flash("OK")
        else:
            flash("No OK")
        return redirect(url_for('userBluePrint.userEndPoint',
                                us=us))
    usr = getUserOnly(us)
    return render_template(
        'permissions.html',
        usr=usr,
        permissions=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])


@adminBP.route("/add/tournament", methods={"GET", "POST"})
@login_required
@only_collaborator
def addNewTournamentEndPoint():
    if request.method == 'POST':
        status, tor = addNewTournament(current_app.config['database'], request.form)
        if status == 200:
            if updateStats(current_app.config['database'], tor) == 200:
                flash("OK")
            else:
                flash("No OK")
        else:
            flash("No OK")
        return redirect(url_for('genericBluePrint.generalEndPoint'))
    return render_template(
        'add.html',
        title="Añadir Torneo",
        user=current_user if not current_user.is_anonymous else None
    )


@adminBP.route("/delete/tournament/<to>", methods={"GET", "POST"})
@login_required
@only_collaborator
def deleteTournamentEndPoint(to):
    if deleteTournament(current_app.config["database"], to) == 200:
        if updateStats(current_app.config['database']) == 200:
            flash("OK")
        else:
            flash("NOK")
    else:
        flash("NOK")
    return redirect(url_for('genericBluePrint.generalEndPoint'))


@adminBP.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system('bash command-pull-event.sh')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@adminBP.route('/update_algorythm', methods=['Get'])
@login_required
@only_left_hand
def updateAlgorythmEndPoint():
    if updateAlgorythm(current_app) == 200:
        return 'Updated successfully', 200
    else:
        return 'Wrong', 400


@adminBP.route('/update_stats', methods=['Get'])
@login_required
@only_left_hand
def updateStatsEndPoint():
    if updateStats(current_app.config['database']) == 200:
        flash("OK")
    else:
        flash("NOK")
    return redirect(url_for('genericBluePrint.generalEndPoint'))
