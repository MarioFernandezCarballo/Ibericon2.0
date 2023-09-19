import json
import secrets
import os

from werkzeug.security import generate_password_hash

from database import db, User, Conference, City
from bpApiAuth import loginManager, jwt
from bpApiAdmin import limiter


def createApp(app):
    with open("secret/config.json") as conf:
        config = json.load(conf)
        conf.close()
    app.config["SECRET_KEY"] = handleSecretKey(config)
    app.config['PORT'] = config['port']
    app.config['HOST'] = config['host']

    app.config["JWT_SECRET_KEY"] = handleSecretKey(config)
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = config['db-uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["BCP_API_EVENT"] = config['api-event-uri']
    app.config["BCP_API_USER"] = config['api-user-uri']
    app.config["BCP_API_USERS"] = config['api-users-uri']
    app.config["BCP_API_TEAM"] = config['api-team-uri']
    app.config["BCP_API_TEAM_PLACINGS"] = config['api-team-placings-uri']
    app.config["BCP_API_HEADERS"] = config['api-headers']

    app.config["CITIES"] = config["cities"]
    app.config["CONFERENCES"] = config["conferences"]

    app.config["ADMIN_USERNAME"] = config['admin-name']
    app.config["ADMIN_PASSWORD"] = config['admin-password']
    app.config["ADMIN_MAIL"] = config['admin-mail']

    app.config["COLLABORATOR_USERNAME"] = config['collab-name']
    app.config["COLLABORATOR_PASSWORD"] = config['collab-password']

    loginManager.init_app(app)
    app.config["loginManager"] = loginManager
    jwt.init_app(app)
    app.config["jwt"] = jwt
    db.init_app(app)
    app.config["database"] = db
    limiter.init_app(app)
    app.config["limiter"] = limiter

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(app.config['database'])
            createAdmin(app)
            createCollaborator(app)
            createRegions(app)
            file = open('database.txt', 'w')
            file.write("Database Created")
            file.close()


def handleSecretKey(keys):
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/config.json", 'w'), indent=4)
        return key


def createTables(database):
    database.create_all()
    database.session.commit()


def createAdmin(app):
    new_user = User(
        bcpId="0000000000",
        bcpMail=app.config["ADMIN_MAIL"],
        bcpName=app.config["ADMIN_USERNAME"],
        password=generate_password_hash(app.config["ADMIN_PASSWORD"], method='scrypt'),
        permissions=15
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()


def createCollaborator(app):
    new_user = User(
        bcpId="0000000000",
        bcpMail=app.config["ADMIN_MAIL"],
        bcpName=app.config["COLLABORATOR_USERNAME"],
        password=generate_password_hash(app.config["COLLABORATOR_PASSWORD"], method='scrypt'),
        permissions=13
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()


def createRegions(app):
    for key, value in app.config['CONFERENCES'].items():
        new_conference = Conference(name=key)
        app.config['database'].session.add(new_conference)
        for key1, value1 in app.config['CITIES'].items():
            if value1 in value:
                new_region = City(name=value1, code=int(key1), conference=new_conference)
                app.config['database'].session.add(new_region)
        app.config['database'].session.commit()
