from flask import Blueprint, render_template
from flask_login import current_user, login_required

from utils.user import getUsers, getUser, getUserOnly, getUsersWinRate
from utils.club import getClubs

userBP = Blueprint('userBluePrint', __name__)


@userBP.route("/users", methods={"GET", "POST"})
def usersEndPoint():
    usr = getUsers()
    cls = getClubs()
    usr = [{"id": u.id, "profilePic": u.profilePic, "bcpName": u.bcpName, "ibericonScore": u.ibericonScore} for u in usr]
    cls = [{"id": c.id, "profilePic": c.profilePic, "bcpName": c.name, "ibericonScore": c.ibericonScore} for c in cls]
    return render_template(
        'users.html',
        title="Jugadores",
        users=usr,
        teams=cls,
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

@userBP.route("/profile/<us>", methods={"GET", "POST"})
@login_required
def profileEndPoint(us):
    user = getUserOnly(us)
    usr = getUser(us)
    return render_template(
        'profile.html',
        title="Mi perfil - " + user.bcpName,
        userOnly=user,
        usr=usr,
        user=current_user if not current_user.is_anonymous else None
    )


@userBP.route("/winrates", methods={"GET", "POST"})
def winRatesEndPoint():
    usr = getUsersWinRate()
    usr = [{"id": u.id, "profilePic": u.profilePic, "bcpName": u.bcpName, "winRate": u.winRate} for u in usr]
    return render_template(
        'winrates.html',
        title="Winrates",
        users=usr,
        user=current_user if not current_user.is_anonymous else None
    )