from flask_openapi3 import APIBlueprint
from flask_login import login_required

from utils import only_team_leader

from .utils import getClubs, getClub, modifyClub
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
def clubApiEndPoint(query: Queries.Detail):
    response = getClub(query)
    return response


@clubApiBP.patch("/change",
                summary="Change club conference",
                description="Change club conference (Norte, Noroeste, Este, Sur, Centro)",
                responses={
                    200: Responses.Modify,
                })
@login_required
@only_team_leader
def modifyClubApiEndPoint(query: Queries.Modify):
    response = modifyClub(query)
    return response