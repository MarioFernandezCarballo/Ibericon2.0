from pydantic import BaseModel, Field
from typing import List


class Factions:
    class Faction(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")


class Clubs:
    class Club(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")


class Teams:
    class Team(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")


class Users:
    class User(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: str = Field(None, description="Your Ibericon conference")
        score: float = Field(None, description="Tournament Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        faction: Factions.Faction = Field(None, description="Faction Information")
        club: Clubs.Club = Field(None, description="Club Information")


class Models:
    class Permission(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        permission: int = Field(None, description="Ibericon Permissions")
        oldPermission: int = Field(None, description="Ibericon Old Permissions")

    class Tournament(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        uri: str = Field(None, description="BCP Uri")
        city: str = Field(None, description="City")
        conference: str = Field(None, description="Conference")
        date: str = Field(None, description="Date of the tournament")
        isTeam: bool = Field(None, description="Is team tournament?")
        rounds: int = Field(None, description="Tournament rounds")
        users: List[Users.User] = Field([], description="Tournament Users")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Permission(BaseResponse):
        data: Models.Permission

    class AddTournament(BaseResponse):
        data: Models.Tournament


