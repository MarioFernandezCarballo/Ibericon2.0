from flask import current_app

from sqlalchemy import desc
from database import User, UserTournament, Tournament


def getUsers(region, qty=0):  # TODO region thingy
    if qty > 0:
        result = User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()


def getUser(pl):
    usr = User.query.filter_by(bcpId=pl).first()
    return current_app.config["database"].session.query(UserTournament, User, Tournament
                                                        ).order_by(desc(UserTournament.ibericonScore)).filter(UserTournament.userId == usr.id
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(User,
                                                                               User.id == UserTournament.userId).all()


def getUserOnly(pl):
    return User.query.filter_by(bcpId=pl).first()
