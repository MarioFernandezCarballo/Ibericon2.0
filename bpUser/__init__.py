from flask import Blueprint, render_template
from flask_login import current_user

from utils.user import getUsers, getUser, getUserOnly, getUserBestTournaments

userBP = Blueprint('userBluePrint', __name__)


@userBP.route("/users", methods={"GET", "POST"})
def usersEndPoint():
    usr = getUsers()
    return render_template(
        'users.html',
        title="Jugadores",
        users=usr,
        user=current_user if not current_user.is_anonymous else None
    )


@userBP.route("/user/<us>", methods={"GET", "POST"})
def userEndPoint(us):
    user = getUserOnly(us)
    usr = getUser(us)
    return render_template(
        'user.html',
        title=user.bcpName,
        userOnly=user,
        usr=usr,
        user=current_user if not current_user.is_anonymous else None
    )
