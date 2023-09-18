from flask import Blueprint, render_template
from flask_login import current_user

from utils.user import setPlayerPermission, getUser
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import getAllTournaments

tournamentBP = Blueprint('tournamentBluePrint', __name__)


@tournamentBP.route("/tournaments", methods={"GET", "POST"})
def tournamentsEndPoint():
    tors = getAllTournaments()
    return render_template(
        'tournaments.html',
        title="Torneos",
        user=current_user if not current_user.is_anonymous else None,
        tors=tors
    )
