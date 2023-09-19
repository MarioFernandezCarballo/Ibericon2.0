from pydantic import BaseModel, Field
from typing import List


class Cities:
    class City(BaseModel):
        id: str = Field(None, description="Id")
        name: str = Field(None, description="Name")

class Conferences:
    class Conference(BaseModel):
        id: str = Field(None, description="Id")
        name: str = Field(None, description="Name")


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
        conference: int = Field(None, description="Your Ibericon conference")
        city: int = Field(None, description="Your city")
        score: float = Field(None, description="Tournament Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        faction: Factions.Faction = Field(None, description="Faction Information")
        club: Clubs.Club = Field(None, description="Club Information")


class Models:
    class Simple(BaseModel):
        id: str = Field(None, description="BCP Id")
        uri: str = Field(None, description="BCP tournament Url")
        name: str = Field(None, description="BCP Name")
        city: Cities.City = Field(None, description="Tournament City")
        conference: Conferences.Conference = Field(None, description="Conference region")
        date: str = Field(None, description="Tournament Date")
        finished: bool = Field(None, description="Is tournament done?")
        isTeam: bool = Field(None, description="Is tournament team?")
        rounds: int = Field(None, description="Tournament rounds")
        totalPlayers: int = Field(None, description="Tournament players")

    class Detailed(Simple):
        users: List[Users.User] = Field([], description="Tournament Users")
        teams: List[Teams.Team] = Field([], description="Tournament Teams")
        clubs: List[Clubs.Club] = Field([], description="Tournament clubs")
        factions: List[Factions.Faction] = Field([], description="Tournament factions")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class List(BaseResponse):
        data: List[Models.Simple] = Field([], description="Tournaments")

    class Detail(BaseResponse):
        data: Models.Detailed = Field({}, description="Tournament detail")
