from flask import current_app
from sqlalchemy import desc

from database import Club, Tournament, UserTournament


def getClub(te):
    return current_app.config["database"].session.query(UserTournament, Tournament, Club
                                                        ).filter(UserTournament.clubId == te
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(Club,
                                                                               Club.id == UserTournament.clubId).all()


def getClubOnly(te):
    return Club.query.filter_by(id=te).first()


def getClubs(qty=0):
    if qty > 0:
        result = Club.query.order_by(desc(Club.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return Club.query.order_by(desc(Club.ibericonScore)).all()


def addClub(db, te):
    if te['team']:
        if not Club.query.filter_by(bcpId=te['teamId']).first():
            db.session.add(Club(
                bcpId=te['teamId'],
                name=te['team']['name'].strip(),
                shortName=te['team']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Club.query.filter_by(bcpId=te['teamId']).first() if te['team'] else None
