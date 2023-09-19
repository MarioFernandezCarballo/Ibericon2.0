from flask import current_app, jsonify
from sqlalchemy import desc

from database import Tournament, UserTournament


def getTournaments(query):
    result = Tournament.query.filter_by(conference=query.conference)
    result = result.order_by(desc(Tournament.date)).all() if query.conference else result.all()
    return jsonify({
        "status": 200,
        "message": "Ok",
        "data": [{
            "id": tor.bcpId,
            "uri": tor.bcpUri,
            "name": tor.name,
            "city": tor.city,
            "conference": tor.conference,
            "date": tor.date,
            "finished": tor.isFinished,
            "isTeam": tor.isTeam,
            "rounds": tor.rounds,
            "totalPlayers": tor.totalPlayers
        } for tor in result]
    })


def getTournament(query):
    tor = Tournament.query.filter_by(bcpId=query.id).first()
    result = current_app.config['database'].session.query(Tournament, UserTournament)\
        .join(UserTournament, Tournament.id == UserTournament.tournamentId)\
        .filter(UserTournament.tournamentId == tor.bcpId).all()
    return result
