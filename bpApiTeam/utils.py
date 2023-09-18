from flask import current_app, jsonify

from sqlalchemy import desc
from database import Team, Tournament, UserTournament, Region


def getTeams(query, qty=0):
    result = Team.query
    if query.region != "España":
        reg = Region.query.filter_by(name=query.region).first()
        if reg:
            result = result.filter_by(region=reg.id).order_by(desc(Team.ibericonScore)).all()
        else:
            return jsonify({
                "status": 404,
                "message": "Region not found",
                "data": []
            })
    else:
        result = Team.query.order_by(desc(Team.ibericonScore)).all()
    return jsonify({
            "status": 200,
            "message": "Ok",
            "data": [{
                "id": te.bcpId,
                "name": te.bcpName,
                "region": te.region,
                "score": te.ibericonScore
            } for te in result[0:qty-1]]
        })


def getTeam(query):
    # TODO terminar esto cuando esté definido user y tournament
    cl = Team.query.filter_by(id=query.bcpId).first()
    if cl:
        res = current_app.config["database"].session.query(UserTournament, Tournament, Team
                                                           ).filter(UserTournament.teamId == query.bcpId
                                                                    ).join(Tournament, Tournament.id == UserTournament.tournamentId
                                                                           ).join(Team, Team.id == UserTournament.teamId).all()
