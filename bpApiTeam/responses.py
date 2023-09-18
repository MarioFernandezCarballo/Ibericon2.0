from pydantic import BaseModel, Field
from typing import List


class Users:
    class User(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        region: int = Field(None, description="Your Ibericon Region Id")
        score: int = Field(None, description="Ibericon global Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        isClassified: bool = Field(None, description="Is this user classified?")


class Tournament:
    class Tournament(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        region: int = Field(None, description="Your Ibericon Region Id")
        date: int = Field(None, description="Ibericon global Score")


class Models:
    class TeamRanking(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        region: int = Field(None, description="Ibericon Region Id")
        score: int = Field(None, description="Ibericon global Score")

    class TeamDetail(TeamRanking):
        users: List[Users.User] = Field([], description="Team users")
        tournaments: List[Tournament.Tournament] = Field([], description="Team tournaments")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Ranking(BaseResponse):
        data: List[Models.TeamRanking] = Field([], description="Teams for the ranking")

    class Detail(BaseResponse):
        data: Models.TeamDetail = Field({}, description="Team details")
