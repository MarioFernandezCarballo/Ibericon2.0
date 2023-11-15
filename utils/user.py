import requests
import json
from statistics import mode
from flask import current_app
from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

from database import User, UserFaction, UserTournament, Tournament, Conference, Faction


def setPlayerPermission(database, userId, form):
    try:
        lvl = form['permission']
        usr = User.query.filter_by(id=userId).first()
        usr.permissions = int(lvl)
        database.session.commit()
    except:
        return False
    return True


def getUser(pl):
    return current_app.config["database"].session.query(UserTournament, User, Tournament
                                                        ).order_by(desc(UserTournament.ibericonScore)).filter(UserTournament.userId == pl
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(User,
                                                                               User.id == UserTournament.userId).all()


def getUserBestTournaments(pl):
    return UserTournament.query.filter_by(userId=int(pl)).order_by(desc(UserTournament.ibericonScore)).limit(4).all()


def getUserOnly(pl):
    return User.query.filter_by(id=pl).first()


def getUserConference(cn):
    return Conference.query.filter_by(id=cn).first()


def getUserMostPlayedFaction(usr):
    fct = usr.factions
    return mode(fct) if fct else None


def getUserMostPlayedClub(usr):
    cl = usr.clubs
    return mode(cl) if cl else None


def getUserLastFaction(usr):
    usT = current_app.config['database'].session.query(UserTournament).filter(UserTournament.userId == usr.id).order_by(desc(UserTournament.id)).limit(1).first()
    if usT:
        return Faction.query.filter_by(id=usT.factionId).first() if usT.factionId else None
    return None


def getUserByBcpId(user):
    return User.query.filter_by(bcpId=user['userId']).first()


def getUsers(qty=0):
    if qty > 0:
        result = User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()


def getUsersWinRate(qty=0):
    if qty > 0:
        result = User.query.filter(User.bcpId != "0000000000").order_by(desc(User.winRate)).all()
        return result[0:qty-1]
    else:
        return User.query.filter(User.bcpId != "0000000000").order_by(desc(User.winRate)).all()

def updateProfile(usr, form):
    usr = User.query.filter_by(id=usr.id)
    return usr  # TODO
