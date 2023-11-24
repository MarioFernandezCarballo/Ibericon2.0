import requests
import json

from flask import current_app

from database import Tournament, UserTournament
from utils.user import getUserByBcpId
from utils.admin import updateStats


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

        updateStats()
    return 200
