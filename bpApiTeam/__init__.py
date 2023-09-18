from flask_openapi3 import APIBlueprint

from .utils import getTeams, getTeam
from .responses import Responses
from .queries import Queries


teamApiBP = APIBlueprint('teamApiBluePrint', __name__, url_prefix='/api/team')


@teamApiBP.get("/",
                summary="Team ranking",
                description="Show team ranking",
                responses={
                    200: Responses.Ranking,
                })
def clubsApiEndPoint(query: Queries.Ranking):
    response = getTeams(query)
    return response


@teamApiBP.get("/detail",
                summary="Team detail",
                description="Show club detail",
                responses={
                    200: Responses.Detail,
                })
def clubEndPoint(query: Queries.Detail):
    response = getTeam(query)
    return response
