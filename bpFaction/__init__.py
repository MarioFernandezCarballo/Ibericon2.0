from flask import Blueprint, render_template
from flask_login import current_user

from utils.faction import getFaction, getFactions, getFactionOnly


factionBP = Blueprint('factionBluePrint', __name__)


@factionBP.route("/faction/<fact>", methods={"GET", "POST"})
def factionEndPoint(fact):
    faction = getFactionOnly(fact)
    fct = getFaction(fact)
    return render_template(
        'faction.html',
        title=faction.name,
        user=current_user if not current_user.is_anonymous else None,
        faction=fct,
        fctOnly=faction
    )


@factionBP.route("/factions", methods={"GET", "POST"})
def factionsEndPoint():
    fct, usrFct = getFactions()
    return render_template(
        'factions.html',
        title="Facciones",
        user=current_user if not current_user.is_anonymous else None,
        factions=fct,
        usrFct=usrFct
    )
