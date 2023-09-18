import requests
import json

from flask import current_app
from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

from database import User, UserFaction, UserTournament, Tournament, Region


def userSignup(database, form):
    if 'geography' in form.keys():
        status, data = checkBCPUser(form)
        if status == 200:
            hashed_password = generate_password_hash(form['password'], method='scrypt')
            user = User.query.filter_by(bcpId=data['id']).first()
            if user:
                if not user.registered:
                    user.bcpMail = data['email']
                    user.password = hashed_password
                    user.registered = True
                    database.session.commit()
                    return 200, user
                return 400, None
            bcpId = data['id']
            new_user = User(
                bcpId=bcpId,
                bcpMail=data['email'],
                password=hashed_password,
                bcpName=data['firstName'] + " " + data['lastName'],
                permissions=0,
                registered=True
            )
            database.session.add(new_user)
            database.session.commit()
            return 200, new_user
        return status, None
    return 401, None


def userLogin(form):
    user = User.query.filter_by(bcpName=form['mail']).first()
    if user:
        if check_password_hash(user.password, form['password']):
            return 200, user
    return 401, None


def setPlayerPermission(database, userId, form):
    try:
        lvl = form['permission']
        usr = User.query.filter_by(id=userId).first()
        usr.permissions = int(lvl)
        database.session.commit()
    except:
        return False
    return True


def getUser(pl):
    return current_app.config["database"].session.query(UserTournament, User, Tournament
                                                        ).order_by(desc(UserTournament.ibericonScore)).filter(UserTournament.userId == pl
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(User,
                                                                               User.id == UserTournament.userId).all()


def getUserBestTournaments(pl):
    return UserTournament.query.filter_by(userId=int(pl)).order_by(desc(UserTournament.ibericonScore)).limit(4).all()


def getUserOnly(pl):
    return User.query.filter_by(id=pl).first()


def getUserByBcpId(user):
    return User.query.filter_by(bcpId=user['userId']).first()


def getUsers(qty=0):
    if qty > 0:
        result = User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return User.query.filter(User.bcpId != "0000000000").order_by(desc(User.ibericonScore)).all()


def addUser(db, usr):
    if not User.query.filter_by(bcpId=usr['userId']).first():
        db.session.add(User(
            bcpId=usr['userId'],
            bcpMail="notamail@notamail.com",
            bcpName=usr['user']['firstName'].strip() + " " + usr['user']['lastName'].strip(),
            permissions=0,
            registered=False
        ))
    db.session.commit()
    return User.query.filter_by(bcpId=usr['userId']).first()


def checkBCPUser(form):
    headers = current_app.config['BCP_API_HEADERS']
    r = requests.post('https://prod-api.bestcoastpairings.com/users/signin',
                      json={"username": form['mail'], "password": form['password']},
                      headers=headers)
    if r.status_code == 200:
        tokens = json.loads(r.text)
        headers['Identity'] = tokens['idToken']
        headers['Authorization'] = 'Bearer ' + tokens['accessToken']
        r = requests.get('https://prod-api.bestcoastpairings.com/users/' + form['mail'],
                         headers=headers)
        if r.status_code == 200:
            userData = json.loads(r.text)
            return r.status_code, userData
    return r.status_code, {}
