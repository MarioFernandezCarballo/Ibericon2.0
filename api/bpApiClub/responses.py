from pydantic import BaseModel, Field
from typing import List

class Users:
    class User(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        score: int = Field(None, description="Ibericon global Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        isClassified: bool = Field(None, description="Is this user classified?")


class Tournament:
    class Tournament(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: int = Field(None, description="Your Ibericon conference Id")
        date: int = Field(None, description="Ibericon global Score")


class Models:
    class ClubRanking(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: int = Field(None, description="Ibericon conference Id")
        score: int = Field(None, description="Ibericon global Score")

    class ClubDetail(ClubRanking):
        users: List[Users.User] = Field([], description="Club users")
        tournaments: List[Tournament.Tournament] = Field([], description="Club tournaments")

    class ChangeClubConference(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: str = Field(None, description="Ibericon conference Id")
        oldConference: str = Field(None, description="Ibericon old conference")
        newPic: str = Field(None, description="New Club image")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Ranking(BaseResponse):
        data: List[Models.ClubRanking] = Field([], description="Clubs for the ranking")

    class Detail(BaseResponse):
        data: Models.ClubDetail = Field({}, description="Club details")

    class Modify(BaseResponse):
        data: Models.ChangeClubConference = Field({}, description="Club conference modified")