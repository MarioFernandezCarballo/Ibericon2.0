from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    bcpMail = db.Column(db.String(100))
    bcpId = db.Column(db.String(30), nullable=False)
    bcpName = db.Column(db.String(100))
    password = db.Column(db.String(200))
    permissions = db.Column(db.Integer)
    registered = db.Column(db.Boolean)
    ibericonScore = db.Column(db.Float, default=0.0)
    isClassified = db.Column(db.Boolean)
    profilePic = db.Column(db.LargeBinary)  # TODO b64encode(user.profilePic)
    region = db.Column(db.Integer, db.ForeignKey('region.id'))
    factions = db.relationship('Faction', secondary="userfaction", cascade='all,delete', back_populates='users')
    teams = db.relationship('Team', secondary="userteam", cascade='all,delete', back_populates='users')
    clubs = db.relationship('Club', secondary="userclub", cascade='all,delete', back_populates='users')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='users')


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.Integer, db.ForeignKey('region.id'))
    shortName = db.Column(db.String(50))
    ibericonScore = db.Column(db.Float, default=0.0)
    users = db.relationship('User', secondary="userteam", back_populates='teams')
    tournaments = db.relationship('Tournament', secondary='usertournament', back_populates='teams', overlaps="tournaments")


class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.Integer, db.ForeignKey('region.id'))
    shortName = db.Column(db.String(50))
    ibericonScore = db.Column(db.Float, default=0.0)
    users = db.relationship('User', secondary="userclub", back_populates='clubs')
    tournaments = db.relationship('Tournament', secondary='usertournament', back_populates='clubs', overlaps="tournaments")


class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    shortName = db.Column(db.String(30))
    users = db.relationship('User', secondary="userfaction", back_populates='factions')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='factions', overlaps="tournaments,tournaments")


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    bcpUri = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shortName = db.Column(db.String(50))
    city = db.Column(db.String(50))
    region = db.Column(db.Integer, db.ForeignKey('region.id'))
    date = db.Column(db.String(50))
    isFinished = db.Column(db.Boolean)
    isTeam = db.Column(db.Boolean)
    totalPlayers = db.Column(db.Integer)
    rounds = db.Column(db.Integer)
    users = db.relationship('User', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="tournaments,tournaments,tournaments")
    teams = db.relationship('Team', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="tournaments,tournaments,tournaments,users")  # TODO este dato es necesario?
    clubs = db.relationship('Club', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="teams,tournaments,tournaments,tournaments,users")  # TODO este dato es necesario?
    factions = db.relationship('Faction', secondary="usertournament", cascade='all,delete', back_populates='tournaments', overlaps="clubs,teams,tournaments,tournaments,tournaments,users")  # TODO este dato es necesario?


class UserTournament(db.Model):
    __tablename__ = 'usertournament'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    clubId = db.Column(db.Integer, db.ForeignKey('club.id'))
    tournamentId = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    innerId = db.Column(db.String(40))
    position = db.Column(db.Integer)
    teamPosition = db.Column(db.Integer)
    bcpScore = db.Column(db.Float, default=0.0)
    ibericonScore = db.Column(db.Float, default=0.0)
    ibericonTeamScore = db.Column(db.Float, default=0.0)
    countingScore = db.Column(db.Boolean, default=False)
    performance = db.Column(db.String(500))


class UserFaction(db.Model):
    __tablename__ = 'userfaction'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    ibericonScore = db.Column(db.Float, default=0.0)
    winRate = db.Column(db.Float, default=0.0)  # TODO


# TODO redefinir puntuaciones de equipo y club
class UserTeam(db.Model):
    __tablename__ = 'userteam'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    ibericonScore = db.Column(db.Float, default=0.0)


class UserClub(db.Model):
    __tablename__ = 'userclub'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    clubId = db.Column(db.Integer, db.ForeignKey('club.id'))
    ibericonScore = db.Column(db.Float, default=0.0)


class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('user.id'))


# ------- Rates ------- #
class UserUserRate:
    __tablename__ = 'useruserrate'
    id = db.Column(db.Integer, primary_key=True)
    user1Id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2Id = db.Column(db.Integer, db.ForeignKey('user.id'))
    games = db.Column(db.Integer, default=0)
    winRate = db.Column(db.Float, default=0.0)
    tieRate = db.Column(db.Float, default=0.0)
    loseRate = db.Column(db.Float, default=0.0)
