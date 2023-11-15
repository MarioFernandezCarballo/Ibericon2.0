from flask import current_app, jsonify
from sqlalchemy import desc

from database import Tournament, UserTournament, User, Faction, Club, City


def getTournaments(query):
    result = Tournament.query
    result = (result.filter_by(conference=query.conference)
              .order_by(desc(Tournament.date)).all()) if query.conference else result.all()
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
    city = City.query.filter_by(id=tor.city).first()
    result = (current_app.config['database'].session.query(Tournament, UserTournament, User, Faction, Club)
              .join(UserTournament, Tournament.id == UserTournament.tournamentId)
              .join(User, User.id == UserTournament.userId)
              .join(Faction, Faction.id == UserTournament.factionId)
              .join(Club, Club.id == UserTournament.clubId)
              .filter(UserTournament.tournamentId == tor.id).all())
    return jsonify({
        "status": 200,
        "message": "Ok",
        "data": {
            "id": tor.bcpId,
            "uri": tor.bcpUri,
            "name": tor.name,
            "city": {
                "id": city.id,
                "name": city.name
            },
            "conference": {
                "id": city.conference.id,
                "name": city.conference.name
            },
            "date": tor.date,
            "finished": tor.isFinished,
            "isTeam": tor.isTeam,
            "rounds": tor.rounds,
            "totalPlayers": tor.totalPlayers,
            "teams": [
                {
                    "id": team.bcpId,
                    "name": team.name
                }
            for team in tor.teams],
            "clubs": [
                {
                    "id": club.bcpId,
                    "name": club.name
                }
                for club in tor.clubs],
            "factions": [
                {
                    "id": faction.bcpId,
                    "name": faction.name
                }
                for faction in tor.factions],
            "users": [
                {
                    "id": user.id,
                    "name": user.bcpName,
                    "conference": user.conference,
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
                }
            for tournament, userTournament, user, faction, club in result]
        }
    })
