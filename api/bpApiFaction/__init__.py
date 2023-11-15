from flask_openapi3 import APIBlueprint

from .queries import Queries
from .responses import Responses
from .utils import getFactions, getFaction

factionApiBP = APIBlueprint('factionApiBluePrint', __name__, url_prefix='/api/faction')


@factionApiBP.get("/",
                  summary="Faction list",
                  description="List of faction",
                  responses={
                      200: Responses.Ranking,
                  })
def factionRankingApiEndPoint(query: Queries.Ranking):
    result = getFactions(query)
    return result


@factionApiBP.get("/detail",
                  summary="Faction detail",
                  description="Faction detail",
                  responses={
                      200: Responses.Detail,
                  })
def factionDetailApiEndPoint(query: Queries.Detail):
    result = getFaction(query)
    return result
