import requests
import json
from datetime import timedelta

from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_login import login_user, logout_user
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from database import User, Region, Tournament, UserTournament, Faction, Team, Club, UserFaction, UserClub


def getTournaments(query):
    result = Tournament.query.filter_by(region=query.region)  # TODO
    result = result.order_by(desc(Tournament.date)).all() if query.region else result.all()
    return jsonify({
        "status": 200,
        "message": "Ok",
        "data": [{
            "id": tor.bcpId,
            "uri": tor.bcpUri,
            "name": tor.name,
            "city": tor.city,
            "region": tor.region,  # TODO
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
