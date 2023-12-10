from flask import current_app, jsonify
from sqlalchemy import desc

from database import Team, Tournament, UserTournament, Conference

def getTeams(query, qty=0):
    result = Team.query
    if query.conference != "España":
        conference = Conference.query.filter_by(name=query.conference).first()
        if conference:
            result = result.filter_by(conference=conference.id).order_by(desc(Team.ibericonScore)).all()
        else:
            return jsonify({
                "status": 404,
                "message": "Conference not found",
                "data": []
            })
    else:
        result = Team.query.order_by(desc(Team.ibericonScore)).all()
    return jsonify({
            "status": 200,
            "message": "Ok",
            "data": [{
                "id": te.bcpId,
                "name": te.name,
                "conference": te.conference,
                "score": te.ibericonScore
            } for te in result[0:qty-1]]
        })


def getTeam(query):
    cl = Team.query.filter_by(id=query.bcpId).first()
    if cl:
        res = current_app.config["database"].session.query(UserTournament, Tournament, Team
                                                           ).filter(UserTournament.teamId == query.bcpId
                                                                    ).join(Tournament, Tournament.id == UserTournament.tournamentId
                                                                           ).join(Team, Team.id == UserTournament.teamId).all()
