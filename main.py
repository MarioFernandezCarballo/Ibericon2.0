from pydantic import BaseModel

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from utils import createApp, createDatabase

from bpGeneric import genericBP
from bpAuth import authBP
from bpAdmin import adminBP
from bpTeam import teamBP
from bpClub import clubBP
from bpUser import userBP
from bpFaction import factionBP
from bpTournament import tournamentBP

# API
from bpApiAdmin import adminApiBP
from bpApiAuth import authApiBP
from bpApiUser import userApiBP
from bpApiClub import clubApiBP
from bpApiFaction import factionApiBP
from bpApiTeam import teamApiBP
from bpApiTournament import tournamentApiBP

info = Info(title="Ibericon API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Ibericon 1.0
app.register_blueprint(genericBP)
app.register_blueprint(authBP)
app.register_blueprint(adminBP)
app.register_blueprint(teamBP)
app.register_blueprint(clubBP)
app.register_blueprint(userBP)
app.register_blueprint(factionBP)
app.register_blueprint(tournamentBP)

# API
app.register_api(adminApiBP)
app.register_api(authApiBP)
app.register_api(userApiBP)
app.register_api(clubApiBP)
app.register_api(factionApiBP)
app.register_api(teamApiBP)
app.register_api(tournamentApiBP)

app = createApp(app)
createDatabase(app)

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])


# TODO que pasa si alguien se cambia el mail de bcp? no se puede logar con el viejo pero guarda el bcpid...
# TODO gestionar el posible cambio de ciudad/conferencia de los jugadores con un many to many
