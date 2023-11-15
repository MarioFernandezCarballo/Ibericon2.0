from flask import current_app, jsonify
from datetime import datetime, timedelta
import requests
import json
from sqlalchemy import desc
from database import *


def checkTournaments():
    for t in Tournament.query.filter_by(isFinished=False).all():
        uri = current_app.config["BCP_API_EVENT_CHECK"].replace("####eventId####", t.bcpId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        info = json.loads(response.text)
        if info['ended']:
            tor = Tournament.query.filter_by(bcpId=info['id']).first()
            if tor:
                _ = deleteTournament(tor)
            newTournament(info, finished=True)


def getFutureTournaments():
    current_datetime = datetime.utcnow()
    now = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    one_year_later = current_datetime + timedelta(days=365)  # Approximation, not accounting for leap years
    one_year_later_formatted = one_year_later.strftime("%Y-%m-%dT%H:%M:%SZ")

    uri = current_app.config["BCP_API_EVENT_SEARCH"].replace("####startDate####", now)
    uri = uri.replace("####endDate####", one_year_later_formatted)
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    info = json.loads(response.text)

    for t in info['data']:
        tor = Tournament.query.filter_by(bcpId=t['id']).first()
        if tor:
            _ = deleteTournament(tor)
        newTournament(t)


def setPlayerPermission(database, userId, level, fromApi=False):
    lvl = level
    usr = User.query.filter_by(bcpId=userId).first()
    oldPermission = usr.permissions
    usr.permissions = int(lvl)
    database.session.commit()
    if fromApi:
        return jsonify({
            "status": 200,
            "message": "Ok",
            "data": {
                "id": usr.bcpId,
                "name": usr.bcpName,
                "permission": usr.permissions,
                "oldPermissions": oldPermission
            }
        })
    return 200


def algorithm(tor, user):
    performance = [0, 0, 0]
    playerModifier = 1 + len(tor.users) / 100
    for game in user['total_games']:
        performance[game['gameResult']] += 1
    points = ((performance[2] * 3) + performance[1])
    finalPoints = points
    return finalPoints * playerModifier


def newTournament(tor, finished=False):
    if finished:
        uri = current_app.config["BCP_API_EVENT"].replace("####event####", tor['id'])
    else:
        uri = current_app.config["BCP_API_EVENT_NEW"].replace("####event####", tor['id'])
    response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
    users = json.loads(response.text)
    tor = manageTournament(tor)
    if tor.isTeam:
        # manageTeams(tor)
        manageUsers(tor, users)
    else:
        manageUsers(tor, users)
    if finished:
        result = updateStats(tor)
        return Tournament.query.filter_by(id=tor.id).first(), result.status_code
    return Tournament.query.filter_by(id=tor.id).first(), 200


def manageTournament(info):
    isTeamTournament = info['teamEvent']
    city = City.query.filter_by(name=current_app.config["CITIES"][info['zip'][0:2]]).first()
    current_app.config['database'].session.add(Tournament(
        bcpId=info['id'],
        bcpUri="https://www.bestcoastpairings.com/event/" + info['id'],
        imgUri=info['photoUrl'] if 'photoUrl' in info.keys() else current_app.config["IMAGE_DEFAULT"],
        name=info['name'].strip(),
        shortName=info['name'].replace(" ", "").lower(),
        city=city.id,
        conference=city.conference_id,
        isTeam=isTeamTournament,
        date=info['eventDate'].split("T")[0],
        totalPlayers=info['totalPlayers'] - info['droppedPlayers'],
        isFinished=info['ended'],
        rounds=info['numberOfRounds']
    ))
    current_app.config['database'].session.commit()
    return Tournament.query.filter_by(bcpId=info['id']).first()


def manageUsers(tor, users):
    if tor.isFinished:
        uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        users = json.loads(response.text)
    for user in users['data']:
        usr = addUserFromTournament(user, tor)
        fct = addFactionFromTournament(user)
        cl = addClubFromTournament(user, tor)
        tor.users.append(usr)
        usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
        if tor.isFinished:
            usrTor.position = user['placing']
            usrTor.opponents = user['opponentIds']
            usrTor.performance = json.dumps(user['total_games'])
            usrTor.won = len([gameRes['gameResult'] for gameRes in user['total_games'] if gameRes['gameResult'] == 2])
            usrTor.tied = len([gameRes['gameResult'] for gameRes in user['total_games'] if gameRes['gameResult'] == 1])
            usrTor.lost = len([gameRes['gameResult'] for gameRes in user['total_games'] if gameRes['gameResult'] == 0])
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
        current_app.config['database'].session.commit()


def addUserFromTournament(usr, tor):
    if not User.query.filter_by(bcpId=usr['userId']).first():
        uri = current_app.config["BCP_API_USER_DETAIL"].replace("####userId####", usr['userId'])
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        users = json.loads(response.text)
        imgUrl = current_app.config["IMAGE_DEFAULT"]
        if 'profileFileId' in users.keys():
            uri = current_app.config["BCP_API_USER_IMG"].replace("####img####", users['profileFileId'])
            response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
            img = json.loads(response.text)
            imgUrl = img['url']
        current_app.config['database'].session.add(User(
            bcpId=usr['userId'],
            bcpName=usr['user']['firstName'].strip() + " " + usr['user']['lastName'].strip(),
            conference=tor.conference,
            profilePic=imgUrl,
            city=tor.city,
            permissions=0,
            registered=False
        ))
    current_app.config['database'].session.commit()
    return User.query.filter_by(bcpId=usr['userId']).first()


def addFactionFromTournament(fct):
    if fct['army']:
        if not Faction.query.filter_by(bcpId=fct['armyId']).first():
            current_app.config['database'].session.add(Faction(
                bcpId=fct['armyId'],
                name=fct['army']['name'].strip(),
                shortName=fct['army']['name'].replace(" ", "").lower()
            ))
    current_app.config['database'].session.commit()
    return Faction.query.filter_by(bcpId=fct['armyId']).first() if fct['army'] else None


def addClubFromTournament(te, tor):
    if te['team']:
        uri = current_app.config["BCP_API_TEAMS_DETAIL"].replace("####teamId####", te['teamId'])
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        team = json.loads(response.text)
        imgUrl = current_app.config["IMAGE_DEFAULT"]
        if 'profileFileId' in team.keys():
            uri = current_app.config["BCP_API_USER_IMG"].replace("####img####", team['profileFileId'])
            response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
            img = json.loads(response.text)
            imgUrl = img['url']
        if not Club.query.filter_by(bcpId=te['teamId']).first():
            current_app.config['database'].session.add(Club(
                bcpId=te['teamId'],
                name=te['team']['name'].strip(),
                conference=tor.conference,
                profilePic=imgUrl,
                shortName=te['team']['name'].replace(" ", "").lower()
            ))
    current_app.config['database'].session.commit()
    return Club.query.filter_by(bcpId=te['teamId']).first() if te['team'] else None


def addTeamFromTournament(te, tor):
    teId = te['name'].replace(" ", "-").lower()
    if not Team.query.filter_by(bcpId=teId).first():
        current_app.config['database'].session.add(Team(
            bcpId=teId,
            name=te['name'].strip(),
            conference=tor.conference,
            shortName=te['name'].replace(" ", "").lower()
        ))
    current_app.config['database'].session.commit()
    return Team.query.filter_by(bcpId=teId).first()


def updateStats(tor=None):
    if tor:
        for usr in tor.users:
            best = current_app.config['database'].session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.userId == usr.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            score = 0
            counter = 0
            won = 0
            tied = 0
            lost = 0
            for to in best:
                to.UserTournament.countingScore = False
                if counter < 5:
                    score += to.UserTournament.ibericonScore
                    to.UserTournament.countingScore = True
                    counter += 1
                won += to.UserTournament.won
                tied += to.UserTournament.tied
                lost += to.UserTournament.lost
            usr.ibericonScore = score
            usr.winRate = 100 * won / (won + tied + lost)
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 4:
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
            score = 0
            counter = 0
            won = 0
            tied = 0
            lost = 0
            for to in best:
                to.UserTournament.countingScore = False
                if counter < 5:
                    score += to.UserTournament.ibericonScore
                    to.UserTournament.countingScore = True
                    counter += 1
                won += to.UserTournament.won
                tied += to.UserTournament.tied
                lost += to.UserTournament.lost
            usr.ibericonScore = score
            try:
                usr.winRate = won / (won + tied + lost)
            except ZeroDivisionError:
                usr.winRate = 0
            for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
                score = 0
                count = 0
                for t in best:
                    if t.UserTournament.factionId == usrFct.factionId:
                        count += 1
                        score += t.UserTournament.ibericonScore
                    if count == 4:
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


def deleteTournament(tor):
    UserTournament.query.filter_by(tournamentId=tor.id).delete()
    current_app.config['database'].session.delete(Tournament.query.filter_by(id=tor.id).first())
    current_app.config['database'].session.commit()
    _ = updateStats()
    return jsonify({
        "status": 200,
        "message": "Ok"
    })
