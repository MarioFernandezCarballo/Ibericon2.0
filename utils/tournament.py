from sqlalchemy import func

from flask import current_app

from database import Tournament, Conference, UserTournament, Faction


def getAllTournaments():
    return current_app.config['database'].session.query(Tournament, Conference).outerjoin(Conference, Tournament.conference == Conference.id).order_by(func.cast(Tournament.date, current_app.config['database'].Date)).all()


def getFutureTournamentsByUser(usr):
    return [t for t in usr.tournaments if not t.isFinished]


def getPastTournamentsByUser(usr):
    result = []
    for t in usr.tournaments:
        if t.isFinished:
            usT = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=t.id).first()
            fct = Faction.query.filter_by(id=usT.factionId).first()
            result.append({
                "tournament": t,
                "userTournament": usT,
                "faction": fct
            })
    return result