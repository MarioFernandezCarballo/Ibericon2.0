from pydantic import BaseModel, Field
from typing import List

class Users:
    class User(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: int = Field(None, description="Your Ibericon conference Id")
        score: int = Field(None, description="Ibericon global Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        isClassified: bool = Field(None, description="Is this user classified?")


class Tournament:
    class User(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: int = Field(None, description="Your Ibericon conference Id")
        date: int = Field(None, description="Ibericon global Score")


class Models:
    class FactionRanking(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        users: List[Users.User] = Field(None, description="Ibericon global Score")

    class FactionDetail(FactionRanking):
        tournaments: List[Users.User] = Field(None, description="Ibericon global Score")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Ranking(BaseResponse):
        data: List[Models.FactionRanking] = Field([], description="Factions for the list")

    class Detail(BaseResponse):
        data: Models.FactionDetail = Field({}, description="Faction details")
