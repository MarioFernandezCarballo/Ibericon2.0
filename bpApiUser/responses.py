from pydantic import BaseModel, Field
from typing import List


class Models:
    class UserRanking(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        conference: int = Field(None, description="Your Ibericon conference Id")
        score: int = Field(None, description="Ibericon global Score")
        profilePic: str = Field(None, description="Profile pic (Base64 str)")
        isClassified: bool = Field(None, description="Is this user classified?")

    class UserDetail(UserRanking):
        pass
        # factions: List[factionResponses.Detail] = Field([], description="User's factions")
        # teams: List[teamResponses.Detail] = Field([], description="User's teams")
        # clubs: List[clubResponses.Detail] = Field([], description="User's clubs")
        # tournaments: List[tournamentResponses.Detail] = Field([], description="User's tournaments")
        # ... rates


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="status code")
        message: str = Field(None, description="exception information")

    class Ranking(BaseResponse):
        data: List[Models.UserRanking] = Field([], description="Users for the ranking")

    class Detail(BaseResponse):
        data: Models.UserDetail = Field({}, description="User details")
