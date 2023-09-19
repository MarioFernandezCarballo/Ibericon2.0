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


class Tournaments:
    class Tournament(BaseModel):
        id: str = Field(None, description="BCP Id")
        uri: str = Field(None, description="BCP tournament Url")
        name: str = Field(None, description="BCP Name")
        city: Cities.City = Field(None, description="Tournament City")
        conference: Conferences.Conference = Field(None, description="Conference region")
        date: str = Field(None, description="Tournament Date")
        isFinished: bool = Field(None, description="Is tournament done?")
        isTeam: bool = Field(None, description="Is tournament team?")
        rounds: int = Field(None, description="Tournament rounds")
        score: float = Field(None, description="Tournament score")
        isCounting: bool = Field(None, description="Does this tournament counts for score?")
        totalPlayers: int = Field(None, description="Tournament players")
        innerId: str = Field(None, description="Tournament internal ID")
        position: int = Field(None, description="Tournament position")
        faction: Factions.Faction = Field(None, description="Tournament Faction")
        club: Clubs.Club = Field(None, description="Tournament Club")
        performance: str = Field(None, description="Tournament performance")
        # TODO ... performance


class Models:
    class UserRanking(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: Conferences.Conference = Field(None, description="Your Ibericon conference")
        city: Cities.City = Field(None, description="Your Ibericon city")
        score: float = Field(None, description="Ibericon global Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        isClassified: bool = Field(None, description="Is this user classified?")

    class UserDetail(UserRanking):
        factions: List[Factions.Faction] = Field([], description="User's factions")
        teams: List[Teams.Team] = Field([], description="User's teams")
        clubs: List[Clubs.Club] = Field([], description="User's clubs")
        tournaments: List[Tournaments.Tournament] = Field([], description="User's tournaments")
        # TODO ... rates


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Ranking(BaseResponse):
        data: List[Models.UserRanking] = Field([], description="Users for the ranking")

    class Detail(BaseResponse):
        data: Models.UserDetail = Field({}, description="User details")
