from flask import current_app, jsonify

from sqlalchemy import desc
from database import Club, Tournament, UserTournament, Conference


def getClubs(query, qty=0):
    result = Club.query
    if query.conference:
        conference = Conference.query.filter_by(name=query.conference).first()
        if conference:
            result = result.filter_by(conference=conference.id).order_by(desc(Club.ibericonScore)).all()
        else:
            return jsonify({
                "status": 404,
                "message": "Region not found",
                "data": []
            })
    else:
        result = Club.query.order_by(desc(Club.ibericonScore)).all()
    return jsonify({
            "status": 200,
            "message": "Ok",
            "data": [{
                "id": cl.bcpId,
                "name": cl.name,
                "conference": cl.conference,
                "score": cl.ibericonScore
            } for cl in result[0:qty-1]]
        })


def getClub(query):
    # TODO terminar esto cuando esté definido user y tournament
    cl = Club.query.filter_by(id=query.bcpId).first()
    if cl:
        res = current_app.config["database"].session.query(UserTournament, Tournament, Club
                                                           ).filter(UserTournament.clubId == query.bcpId
                                                                    ).join(Tournament, Tournament.id == UserTournament.tournamentId
                                                                           ).join(Club, Club.id == UserTournament.clubId).all()
