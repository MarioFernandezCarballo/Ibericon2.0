from flask import current_app
from sqlalchemy import desc

from database import Team, Tournament, UserTournament, User


def getTeam(te):
    return current_app.config["database"].session.query(UserTournament, Tournament, User
                                                        ).filter(UserTournament.teamId == te
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(User,
                                                                               User.id == UserTournament.userId).all()


def getTeamOnly(te):
    return Team.query.filter_by(id=te).first()


def getTeams(qty=0):
    if qty > 0:
        result = Team.query.order_by(desc(Team.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return Team.query.order_by(desc(Team.ibericonScore)).all()


def getTeamUsers(team, allUsers):
    teamUsersId = [pl['objectId'] for pl in team['players']]
    return [user for user in allUsers['data'] if user['objectId'] in teamUsersId]


def addTeam(db, te):
    teId = te['name'].replace(" ", "-").lower()
    if not Team.query.filter_by(bcpId=teId).first():
        db.session.add(Team(
            bcpId=teId,
            name=te['name'].strip(),
            shortName=te['name'].replace(" ", "").lower()
        ))
    db.session.commit()
    return Team.query.filter_by(bcpId=teId).first()
