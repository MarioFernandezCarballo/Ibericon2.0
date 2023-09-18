import requests
import json

from sqlalchemy import desc
from flask import current_app

from database import User, Team, Tournament, UserTournament, UserFaction, UserClub, Club
from utils.user import getUserByBcpId


def updateStats(db, tor=None):
    if tor:
        for usr in tor.users:
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
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
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            clubScore = []
            for player in UserClub.query.filter_by(clubId=cl.id).all():
                for best in db.session.query(UserTournament).order_by(desc(UserTournament.ibericonScore)).filter(UserTournament.userId == player.userId).limit(3).all():
                    clubScore.append(best.ibericonScore)
            clubScore.sort(reverse=True)
            cl.ibericonScore = sum(clubScore[:10])
    else:
        for usr in User.query.all():
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonScore)).filter(
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
            best = db.session.query(UserTournament, Tournament).order_by(desc(UserTournament.ibericonTeamScore)).filter(
                UserTournament.teamId == tm.id).join(Tournament, Tournament.id == UserTournament.tournamentId).all()
            tm.ibericonScore = sum([t.UserTournament.ibericonTeamScore for t in best[:4]]) / 3  # Team Players
        for cl in Club.query.all():
            clubScore = []
            for player in UserClub.query.filter_by(clubId=cl.id).all():
                for best in db.session.query(UserTournament).order_by(desc(UserTournament.ibericonScore)).filter(
                        UserTournament.userId == player.userId).limit(3).all():
                    clubScore.append(best.ibericonScore)
            clubScore.sort(reverse=True)
            cl.ibericonScore = sum(clubScore[:10])
    db.session.commit()
    return 200


def updateAlgorythm(app):
    for tor in Tournament.query.all():
        uri = app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
        response = requests.get(uri, headers=current_app.config["BCP_API_HEADERS"])
        info = json.loads(response.text)
        for user in info['data']:
            usr = getUserByBcpId(user)

            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = user['placing']
            usrTor.performance = json.dumps(user['total_games'])

            performance = [0, 0, 0]
            playerModifier = 1 + len(tor.users) / 100
            for game in user['total_games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points
            usrTor.ibericonScore = finalPoints * playerModifier
            app.config['database'].session.commit()

        updateStats(app.config['database'], tor)
    return 200
