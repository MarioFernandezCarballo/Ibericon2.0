from flask import jsonify
from flask_openapi3 import APIBlueprint
from flask_login import login_required

from database import Region

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
    usr = getUsers(query.region)  # TODO hacer aquí el join de region y otras cosas
    users = []
    for u in usr:
        region = Region.query.filter_by(id=u.region).first()
        users.append({
            'id': u.bcpId,
            'name': u.bcpName,
            'region': region.name,
            'scoreGlobal': u.ibericonScore,
            'scoreRegion': u.ibericonScore  # TODO
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
    region = Region.query.filter_by(id=user.region).first()
    return jsonify({
        "status": 200,
        "message": "Successful",
        "data": {
            'id': user.bcpId,
            'name': user.bcpName,
            'region': region.name,
            'scoreGlobal': user.ibericonScore,
            'scoreRegion': user.ibericonScore  # TODO
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
    region = Region.query.filter_by(id=user.region).first()
    return jsonify({
        "status": 200,
        "message": "Successful",
        "data": {
            'id': user.bcpId,
            'name': user.bcpName,
            'region': region.name,
            'scoreGlobal': user.ibericonScore,
        }
    })