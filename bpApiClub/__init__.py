from flask_openapi3 import APIBlueprint

from .utils import getClubs, getClub
from .responses import Responses
from .queries import Queries


clubApiBP = APIBlueprint('clubApiBluePrint', __name__, url_prefix='/api/club')


@clubApiBP.get("/",
                summary="Club ranking",
                description="Show clubs ranking",
                responses={
                    200: Responses.Ranking,
                })
def clubsApiEndPoint(query: Queries.Ranking):
    response = getClubs(query)
    return response


@clubApiBP.get("/detail",
                summary="Club detail",
                description="Show club detail",
                responses={
                    200: Responses.Detail,
                })
def clubEndPoint(query: Queries.Detail):
    response = getClub(query)
    return response
