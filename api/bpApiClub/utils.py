import tokenize

from flask import current_app, jsonify

from sqlalchemy import desc
from database import Club, UserClub, Conference

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
    result = Club.query.filter_by(bcpId=query.bcpId).first()
    return jsonify({
        "status": 200,
        "message": "Ok",
        "data": {
            "id": result.bcpId,
            "name": result.name,
            "conference": result.conference,
            "score": result.ibericonScore,
            "users": [{
                "id": us.bcpId,
                "name": us.bcpName,
                "score": UserClub.query.filter_by(userId=us.id).filter_by(clubId=result.id).first().ibericonScore,
                "profilePid": us.profilePic,  # TODO volcar imagen
                "isClassified": us.isClassified
            } for us in result.users],
            "tournaments": [{
                "id": to.bcpId,
                "name": to.name,
                "uri": to.bcpUri,
                "conference": Conference.query.filter_by(id=to.conference).first().name,
                "date": to.date
            } for to in result.tournaments]
        }
    })

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