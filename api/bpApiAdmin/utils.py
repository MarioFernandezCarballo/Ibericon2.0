import requests
import json

from flask import current_app, jsonify
from sqlalchemy import desc

from database import User, Conference, Tournament, UserTournament, Faction, Team, Club, UserFaction, UserClub, City
from utils.admin import setPlayerPermission, algorithm, newTournament, updateStats, updateAlgorithm, deleteTournament, setTeamLeader

def setPlayerPermissionApi(database, userId, level):
    return setPlayerPermission(database, userId, level, fromApi=True)


def setTeamLeaderApi(database, userId, teamId):
    return setTeamLeader(database, userId, teamId, fromApi=True)


def newTournamentApi(uri):
    if "https://www.bestcoastpairings.com/event/" in uri:
        eventId = uri.split("/")[-1].split("?")[0]
        uri = current_app.config["BCP_API_EVENT"].replace("####event####", eventId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        info = json.loads(response.text)
        #if not info['ended']:
        #    return jsonify({
        #        "status": 401,
        #        "message": "Tournament is not ended",
        #        "data": {}
        #    })
        tor = Tournament.query.filter_by(bcpId=info['id']).first()
        if tor:
            if not tor.isFinished and info['ended']:
                _ = deleteTournament(tor)
            else:
                return jsonify({
                    "status": 401,
                    "message": "Tournament already exists",
                    "data": {}
                })
        tor, result = newTournament(info)
        if result == 200:
            return jsonify({
                "status": 200,
                "message": "Ok",
                "data": {
                    "id": tor.bcpId,
                    "name": tor.name,
                    "uri": tor.bcpUri,
                    "city": tor.city,
                    "conference": Conference.query.filter_by(id=tor.conference).first().name,
                    "date": tor.date,
                    "isTeam": tor.isTeam,
                    "rounds": tor.rounds,
                    "users": [{
                        "id": user.bcpId,
                        "name": user.bcpName,
                        "conference": city.conference.name,
                        "city": city.name,
                        "score": userTournament.ibericonScore,
                        "profilePic": user.profilePic,
                        "faction": {
                            "id": faction.bcpId,
                            "name": faction.name
                        },
                        "club": {
                            "id": club.bcpId,
                            "name": club.name
                        }
                    } for user, userTournament, faction, club, city in current_app.config['database']
                        .session.query(User, UserTournament, Faction, Club, City)
                        .join(UserTournament, User.id == UserTournament.userId)
                        .join(Faction, Faction.id == UserTournament.factionId)
                        .join(Club, Club.id == UserTournament.clubId)
                        .join(City, City.id == User.city)
                        .filter(UserTournament.tournamentId == tor.id).all()]
                }
            })
        else:
            return jsonify({
                "status": 500,
                "message": "Something went wrong",
                "data": {}
            })
    return jsonify({
                "status": 404,
                "message": "Bad link",
                "data": {}
            })


def updateStatsApi():
    return updateStats()


def updateAlgorithmApi():
    return  updateAlgorithm()


def deleteTournamentApi(query):
    tor = Tournament.query.filter_by(bcpId=query.id).first()
    return deleteTournament(tor)
