from flask import current_app, jsonify
from sqlalchemy import desc

from database import Faction, UserFaction, User


def getFactions(query):
    factions = current_app.config['database'].session.query(Faction).order_by(Faction.name).all()
    result = jsonify({
        "status": 200,
        "message": "Ok",
        "data": [{
            "id": faction.bcpId,
            "name": faction.name,
            "winRate": faction.winRate,
            "pickRate": faction.pickRate,
            "users": [{
                "id": user.bcpId,
                "name": user.bcpName,
                "conference": user.conference,
                "score": score,
                "profilePic": user.profilePic,
                "isClassified": user.isClassified,
            } for user, score in (current_app.config['database'].session.query(User, UserFaction.ibericonScore)
                                  .join(UserFaction, User.id == UserFaction.userId)
                                  .filter(UserFaction.factionId == faction.id)
                                  .order_by(desc(UserFaction.ibericonScore))
                                  .all())]
        } for faction in factions]
    })
    return result


def getFaction(query):
    faction = current_app.config['database'].session.query(Faction).filter(Faction.bcpId == query.bcpId).first()
    result = jsonify({
        "status": 200,
        "message": "Ok",
        "data": {
            "id": faction.bcpId,
            "name": faction.name,
            "winRate": faction.winRate,
            "pickRate": faction.pickRate,
            "users": [{
                "id": user.bcpId,
                "name": user.bcpName,
                "conference": user.conference,
                "score": score,
                "profilePic": user.profilePic,
                "isClassified": user.isClassified,
            } for user, score in (current_app.config['database'].session.query(User, UserFaction.ibericonScore)
                                  .join(UserFaction, User.id == UserFaction.userId)
                                  .filter(UserFaction.factionId == faction.id)
                                  .order_by(desc(UserFaction.ibericonScore))
                                  .all())],
            "tournaments": [{
                "id": tour.bcpId,
                "name": tour.name,
                "conference": tour.conference,
                "date": tour.date
            } for tour in faction.tournaments],
        }
    })
    return result
