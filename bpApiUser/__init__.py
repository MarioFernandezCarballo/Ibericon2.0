from flask import jsonify
from flask_openapi3 import APIBlueprint
from flask_login import login_required

from database import Conference

from .queries import Queries
from .responses import Responses
from .utils import getUsers, getUser, getUserOnly

userApiBP = APIBlueprint('userApiBluePrint', __name__, url_prefix='/api/user')


@userApiBP.get("/",
                summary="User list",
                description="List of user",
                responses={
                    200: Responses.Ranking,
                })
def userRankingApiEndPoint(query: Queries.Ranking):
    usr = getUsers(query.conference)  # TODO hacer aquí el join de region y otras cosas
    users = []
    for u in usr:
        conference = Conference.query.filter_by(id=u.conference).first()
        users.append({
            'id': u.bcpId,
            'name': u.bcpName,
            'conference': conference.name,
            'scoreGlobal': u.ibericonScore,
        })
    return jsonify({
        "status": 200,
        "message": "Successful",
        "data": users
    })


@userApiBP.get("/detail",
                summary="User detail",
                description="User detail",
                responses={
                    200: Responses.Detail,
                })
def userDetailApiEndPoint(query: Queries.Detail):
    user = getUserOnly(query.bcpId)
    usr = getUser(query.bcpId)
    conference = Conference.query.filter_by(id=user.conference).first()
    return jsonify({
        "status": 200,
        "message": "Successful",
        "data": {
            'id': user.bcpId,
            'name': user.bcpName,
            'conference': conference.name,
            'scoreGlobal': user.ibericonScore,
        }
    })


@userApiBP.get("/profile",
                summary="User profile",
                description="User profile page",
                responses={
                    200: Responses.Detail,
                })
@login_required
def userProfileApiEndPoint(query: Queries.Detail):
    user = getUserOnly(query.bcpId)
    usr = getUser(query.bcpId)
    conference = Conference.query.filter_by(id=user.conference).first()
    return jsonify({
        "status": 200,
        "message": "Successful",
        "data": {
            'id': user.bcpId,
            'name': user.bcpName,
            'conference': conference.name,
            'scoreGlobal': user.ibericonScore,
        }
    })