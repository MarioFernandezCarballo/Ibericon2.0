import os

from flask import current_app, jsonify
from flask_openapi3 import APIBlueprint
from flask_login import login_required
from flask_limiter import Limiter, RateLimitExceeded

from utils.decorators import only_left_hand, only_collaborator

from .queries import Queries
from .responses import Responses
from .utils import setPlayerPermission, updateAlgorithm, updateStats, addNewTournament, deleteTournament


adminApiBP = APIBlueprint('adminApiBluePrint', __name__, url_prefix='/api/admin')
limiter = Limiter(key_func=lambda: 'global')


@adminApiBP.patch("/user/permission",
                  summary="Change permissions",
                  description='Change permissions. You must be at least "Left Hand": '
                              '1-plasteel, '
                              '2-ceramite, '
                              '3-diamantite, '
                              '4-adamantium, '
                              '10-team leader, '
                              '11-tournament organizer, '
                              '12-collaborator, '
                              '13-left hand, '
                              '14-right hand, '
                              '15-admin',
                  responses={
                      200: Responses.Permission,
                  })
@login_required
@only_left_hand
def changePlayerPermissionsApiEndPoint(query: Queries.Permission):
    response = setPlayerPermission(current_app.config["database"], query.bcpId, query.newPermission)
    return response


@adminApiBP.post("tournament/add",
                  summary="Add new tournament manually",
                  description='Add New tournament. This function will soon be deprecated',
                  responses={
                      200: Responses.AddTournament,
                  })
@login_required
@only_collaborator
def addNewTournamentApiEndPoint(query: Queries.AddTournament):
    response = addNewTournament(current_app.config['database'], query)
    return response


@adminApiBP.delete("tournament/delete",
                   summary="Delete tournament manually",
                   description='Delete tournament',
                   responses={
                       200: Responses.BaseResponse,
                   })
@login_required
@only_collaborator
def deleteTournamentApiEndPoint(query: Queries.DeleteTournament):
    result = deleteTournament(query)
    updateStats()
    return result


@adminApiBP.post('/update/server',
                 summary="Delete tournament manually",
                 description='Delete tournament',
                 responses={
                     200: Responses.BaseResponse,
                 },
                 doc_ui=False)  # TODO cambiar esto en github que apunte a donde tiene que hacerlo
def webhookApi():
    os.system('bash command-pull-event.sh')  # TODO limitar esto a una vez por hora
    return jsonify({
        "status": 200,
        "message": "Ok"
    })


@adminApiBP.patch('/update/algorithm',
                  summary="Delete tournament manually",
                  description='Delete tournament',
                  responses={
                      200: Responses.BaseResponse,
                  },
                  doc_ui=False)
@login_required
@only_left_hand
def updateAlgorithmApiEndPoint():
    try:
        with limiter.limit("1/hour"):
            result = updateAlgorithm()
            return result
    except RateLimitExceeded:
        return jsonify({
            "status": 400,
            "message": "Limit of this endpoint exceeded"
        })


@adminApiBP.patch('/update/stats',
                   summary="Update stats manually",
                   description='Update stats',
                   responses={
                       200: Responses.BaseResponse,
                   })
@login_required
@only_left_hand
def updateStatsApiEndPoint():
    try:
        with limiter.limit("1/hour"):
            result = updateStats()
            return result
    except RateLimitExceeded:
        return jsonify({
            "status": 400,
            "message": "Limit of this endpoint exceeded"
        })
