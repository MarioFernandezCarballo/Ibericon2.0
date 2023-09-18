from flask import Blueprint, render_template
from flask_login import current_user
from flask_openapi3 import APIBlueprint

from utils.club import getClubs, getClub, getClubOnly


clubBP = APIBlueprint('clubBluePrint', __name__)


@clubBP.route("/clubs", methods={"GET", "POST"})
def clubsEndPoint():
    clb = getClubs()
    return render_template(
        'clubs.html',
        title="Clubes",
        clubs=clb,
        user=current_user if not current_user.is_anonymous else None
    )


@clubBP.route("/club/<cl>", methods={"GET", "POST"})
def clubEndPoint(cl):
    club = getClubOnly(cl)
    clTor = getClub(cl)
    return render_template(
        'club.html',
        title=club.name,
        club=club,
        clTor=clTor,
        user=current_user if not current_user.is_anonymous else None
    )
