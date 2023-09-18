import requests
import json
from datetime import timedelta

from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_login import login_user, logout_user
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from database import User, Region, Tournament, UserTournament, Faction, Team, Club, UserFaction, UserClub


def setPlayerPermission(database, userId, level):
    lvl = level
    usr = User.query.filter_by(bcpId=userId).first()
    usr.permissions = int(lvl)
    database.session.commit()
    return jsonify({
        "status": 200,
        "message": "Ok",
        "data": {
            "id": usr.bcpId,
            "name": usr.bcpName,
            "permission": usr.permissions,
        }
    })


def algorithm(tor, user):
    performance = [0, 0, 0]
    playerModifier = 1 + len(tor.users) / 100
    for game in user['total_games']:
        performance[game['gameResult']] += 1
    points = ((performance[2] * 3) + performance[1])
    finalPoints = points
    return finalPoints * playerModifier


def addNewTournament(db, form):
    if "https://www.bestcoastpairings.com/event/" in form.uri:
        eventId = form.uri.split("/")[-1].split("?")[0]
        uri = current_app.config["BCP_API_EVENT"].replace("####event####", eventId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        info = json.loads(response.text)
        if not info['ended']:
            return jsonify({
                "status": 401,
                "message": "Tournament is not ended",
                "data": {}
            })
        if Tournament.query.filter_by(bcpId=info['id']).first():
            return jsonify({
                "status": 401,
                "message": "Tournament already exists",
                "data": {}
            })
        tor = manageTournament(db, info)
        if tor.isTeam:
            manageTeams(db, tor)
        else:
            manageUsers(db, tor)
        result = updateStats(tor)
        if result.json['status'] == 200:
            return jsonify({
                "status": 200,
                "message": "Ok",
                "data": {
                    "id": tor.bcpId,
                    "name": tor.name,
                    "uri": tor.bcpUri,
                    "city": tor.city,
                    # "region": Region.query.filter_by(id=tor.city).first().name,  # TODO
                    "date": tor.date,
                    "isTeam": tor.isTeam,
                    "rounds": tor.rounds,
                    "users": [{
                        "id": user.bcpId,
                        "name": user.bcpName,
                        # "region": Region.query.filter_by(id=user.region).first().name,  # TODO
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
                    } for user, userTournament, faction, club in current_app.config['database'].session.query(User, UserTournament, Faction, Club)
                        .join(UserTournament, User.id == UserTournament.userId)
                        .join(Faction, Faction.id == UserTournament.factionId)
                        .join(Club, Club.id == UserTournament.clubId)
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


def manageTournament(db, info):
    isTeamTournament = info['teamEvent']
    location = current_app.config["CITIES"][info['zip'][0:2]]
    db.session.add(Tournament(
        bcpId=info['id'],
        bcpUri="https://www.bestcoastpairings.com/event/" + info['id'],
        name=info['name'].strip(),
        shortName=info['name'].replace(" ", "").lower(),
        city=location,
        isTeam=isTeamTournament,
        date=info['eventDate'].split("T")[0],
        totalPlayers=info['totalPlayers'] - info['droppedPlayers'],
        rounds=info['numberOfRounds']
    ))
    db.session.commit()
    return Tournament.query.filter_by(bcpId=info['id']).first()


def manageUsers(db, tor):
    uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    info = json.loads(response.text)
    for user in info['data']:
        usr = addUserFromTournament(db, user, tor)
        fct = addFactionFromTournament(db, user)
        cl = addClubFromTournament(db, user)
        tor.users.append(usr)
        usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
        usrTor.position = user['placing']
        usrTor.performance = json.dumps(user['total_games'])
        usrTor.innerId = user['playerId']
        usrTor.ibericonScore = algorithm(tor, user)

        if fct:
            if fct not in usr.factions:
                usr.factions.append(fct)
            usrTor.factionId = fct.id
        if cl:
            if cl not in usr.clubs:
                usr.clubs.append(cl)
            usrTor.clubId = cl.id
        db.session.commit()


def manageTeams(db, tor):  # TODO test this all
    uri = current_app.config["BCP_API_TEAM"].replace("####event####", tor.bcpId)
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    infoTeams = json.loads(response.text)
    uri = current_app.config["BCP_API_TEAM_PLACINGS"].replace("####event####", tor.bcpId)
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    infoTeamPlacings = json.loads(response.text)
    uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    infoUsers = json.loads(response.text)
    for teamPlacing in infoTeamPlacings['data']:
        team = [tpl for tpl in infoTeams['data'] if tpl['id'] == teamPlacing['id']][0]
        uss = [u for u in infoUsers['data'] if u['objectId'] in [pl['objectId'] for pl in team['players']]]
        tm = addTeamFromTournament(db, team)
        if tm:
            tor.teams.append(tm)

        for us in uss:
            usr = addUserFromTournament(db, us, tor)
            fct = addFactionFromTournament(db, us)
            cl = addClubFromTournament(db, us)

            tor.users.append(usr)
            tm.users.append(usr)

            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = us['placing']
            usrTor.performance = json.dumps('total_games')
            usrTor.innerId = us['playerId']

            usrTor.teamPosition = teamPlacing['placing']

            performance = [0, 0, 0]
            maxPoints = len(teamPlacing['games']) * 3
            maxIbericon = 3
            playerModifier = 1 + tor.totalPlayers / 100
            for game in teamPlacing['games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points * maxIbericon / maxPoints
            usrTor.ibericonTeamScore = finalPoints * playerModifier * 10
            usrTor.teamId = tm.id

            performance = [0, 0, 0]
            maxPoints = len(us['games']) * 3
            maxIbericon = 3
            playerModifier = 1 + tor.totalPlayers / 100
            for game in us['games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points * maxIbericon / maxPoints
            usrTor.ibericonScore = finalPoints * playerModifier * 10

            if fct:
                if fct not in usr.factions:
                    usr.factions.append(fct)
                usrTor.factionId = fct.id
            if cl:
                if cl not in usr.clubs:
                    usr.clubs.append(cl)
                usrTor.clubId = cl.id
            db.session.commit()


def addUserFromTournament(db, usr, tor):
    if not User.query.filter_by(bcpId=usr['userId']).first():
        region = Region.query.filter_by(name=tor.city).first()  # TODO cambiar a region cuando funcione
        db.session.add(User(
            bcpId=usr['userId'],
            bcpName=usr['user']['firstName'].strip() + " " + usr['user']['lastName'].strip(),
            region=region.id if region else None,  # TODO test
            permissions=0,
            registered=False
        ))
    db.session.commit()
    return User.query.filter_by(bcpId=usr['userId']).first()


def addFactionFromTournament(db, fct):
    if fct['army']:
        if not Faction.query.filter_by(bcpId=fct['armyId']).first():
            db.session.add(Faction(
                bcpId=fct['armyId'],
                name=fct['army']['name'].strip(),
                shortName=fct['army']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Faction.query.filter_by(bcpId=fct['armyId']).first() if fct['army'] else None


def addClubFromTournament(db, te):
    if te['team']:
        if not Club.query.filter_by(bcpId=te['teamId']).first():
            db.session.add(Club(
                bcpId=te['teamId'],
                name=te['team']['name'].strip(),
                shortName=te['team']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Club.query.filter_by(bcpId=te['teamId']).first() if te['team'] else None


def addTeamFromTournament(db, te):
    teId = te['name'].replace(" ", "-").lower()
    if not Team.query.filter_by(bcpId=teId).first():
        db.session.add(Team(
            bcpId=teId,
            name=te['name'].strip(),
            shortName=te['name'].replace(" ", "").lower()
        ))
    db.session.commit()
    return Team.query.filter_by(bcpId=teId).first()


def updateStats(tor=None):
    if tor:
        for usr in tor.users:
            best = current_app.config['database'].session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            cities = {}
            score = 0
            counter = 0
            for to in best:
                if not to.Tournament.isTeam:
                    to.UserTournament.countingScore = False
                    try:
                        cities[to.Tournament.city] += 1
                    except KeyError:
                        cities[to.Tournament.city] = 1

                    if cities[to.Tournament.city] <= 3:
                        score += to.UserTournament.ibericonScore
                        to.UserTournament.countingScore = True
                        counter += 1
                    if counter == 4:
                        break
            usr.ibericonScore = score
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrFct.ibericonScore = score
            for usrCl in UserClub.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.clubId == usrCl.clubId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrCl.ibericonScore = score
        for tm in tor.teams:
            best = current_app.config['database'].session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            clubScore = []
            for player in UserClub.query.filter_by(clubId=cl.id).all():
                for best in current_app.config['database'].session.query(UserTournament).order_by(desc(UserTournament.ibericonScore)).filter(UserTournament.userId == player.userId).limit(3).all():
                    clubScore.append(best.ibericonScore)
            clubScore.sort(reverse=True)
            cl.ibericonScore = sum(clubScore[:10])
    else:
        for usr in User.query.all():
            best = current_app.config['database'].session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            cities = {}
            score = 0
            counter = 0
            for to in best:
                if not to.Tournament.isTeam:
                    to.UserTournament.countingScore = False
                    try:
                        cities[to.Tournament.city] += 1
                    except KeyError:
                        cities[to.Tournament.city] = 1

                    if cities[to.Tournament.city] <= 3:
                        score += to.UserTournament.ibericonScore
                        to.UserTournament.countingScore = True
                        counter += 1
                    if counter == 4:
                        break
            usr.ibericonScore = score
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrFct.ibericonScore = score
            for usrCl in UserClub.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.clubId == usrCl.clubId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 3:
                        break
                usrCl.ibericonScore = score
        for tm in Team.query.all():
            best = current_app.config['database'].session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonTeamScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            clubScore = []
            for player in UserClub.query.filter_by(clubId=cl.id).all():
                for best in current_app.config['database'].session.query(UserTournament).order_by(desc(UserTournament.ibericonScore)).filter(
                        UserTournament.userId == player.userId).limit(3).all():
                    clubScore.append(best.ibericonScore)
            clubScore.sort(reverse=True)
            cl.ibericonScore = sum(clubScore[:10])
    current_app.config['database'].session.commit()
    return jsonify({
        "status": 200,
        "message": "Ok"
    })


def updateAlgorithm():
    for tor in Tournament.query.all():
        uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        info = json.loads(response.text)
        for user in info['data']:
            usr = User.query.filter_by(bcpId=user['userId']).first()
            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = user['placing']
            usrTor.performance = json.dumps(user['total_games'])
            usrTor.ibericonScore = algorithm(tor, user)
            current_app.config['database'].session.commit()
        _ = updateStats(tor)
    return jsonify({
        "status": 200,
        "message": "Ok"
    })


def deleteTournament(to):
    UserTournament.query.filter_by(tournamentId=to).delete()
    current_app.config['database'].session.delete(Tournament.query.filter_by(id=to).first())
    current_app.config['database'].session.commit()
    return jsonify({
        "status": 200,
        "message": "Ok"
    })
