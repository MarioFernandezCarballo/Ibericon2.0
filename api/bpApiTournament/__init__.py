from flask_openapi3 import APIBlueprint

from .queries import Queries
from .responses import Responses
from .utils import getTournament, getTournaments


tournamentApiBP = APIBlueprint('tournamentApiBluePrint', __name__, url_prefix='/api/tournament')

@tournamentApiBP.get("/",
                     summary="Tournaments list",
                     description='Get tournament list',
                     responses={
                         200: Responses.List,
                     })
def getTournamentsApiEndPoint(query: Queries.List):
    response = getTournaments(query)
    return response


@tournamentApiBP.get("/detail",
                     summary="Tournaments detail",
                     description='Get tournament detail',
                     responses={
                         200: Responses.Detail,
                     })
def getTournamentApiEndPoint(query: Queries.Detail):
    response = getTournament(query)
    return response
