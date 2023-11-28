from flask import current_app
from sqlalchemy import desc

import base64
import requests
import json

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


def updateTeamPicture(cl, form):
    file = form['file']
    img = base64.b64encode(file.read())
    response = requests.post(current_app.config['IMAGE_BB_UPLOAD'],
                             params={'key': current_app.config['IMAGE_BB_KEY']},
                             data={'image': img})
    u = Club.query.filter_by(id=cl).first()
    try:
        u.profilePic = json.loads(response.text)['data']['url']
    except KeyError:
        return 400
    current_app.config['database'].session.commit()
    return 200
