from flask import current_app, jsonify

from sqlalchemy import desc
from database import Club, Tournament, UserTournament, Conference


def getClubs(query):
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
            } for cl in result]
        })


def getClub(query):
    # TODO terminar esto cuando esté definido user y tournament
    cl = Club.query.filter_by(id=query.bcpId).first()
    if cl:
        res = current_app.config["database"].session.query(UserTournament, Tournament, Club
                                                           ).filter(UserTournament.clubId == query.bcpId
                                                                    ).join(Tournament, Tournament.id == UserTournament.tournamentId
                                                                           ).join(Club, Club.id == UserTournament.clubId).all()

def modifyClub(query):
    club = Club.query.filter_by(name=query.name).first()
    if club:
        data = {
            "id": club.bcpId,
            "name": club.name,
            "conference": None,
            "oldConference": None,
            "newPic": False
        }
        if query.conference:
            oldConference = Conference.query.filter_by(id=club.conference).first()
            conference = Conference.query.filter_by(name=query.conference).first()
            if conference:
                club.conference = conference.id
                data['conference'] = conference.name
                data['oldConference'] = oldConference.name
            else:
                return jsonify({
                    "status": 404,
                    "message": "Conference not found",
                    "data": {}
                })
        if query.profilePic:
            club.profilePic = query.profilePic  # TODO ver cómo volcar imagen en base de datos
            data['newPic'] = True
        current_app.config['database'].session.commit()
        return jsonify({
            "status": 200,
            "message": "Ok",
            "data": data
        })
    return jsonify({
        "status": 404,
        "message": "Club not found",
        "data": {}
    })