from pydantic import BaseModel, Field


class Queries:
    class Ranking(BaseModel):
        conference: str = Field([], description="Conference of Ibericon")
    class Detail(BaseModel):
        bcpId: str = Field(None, description="BCP Id")

    class Modify(BaseModel):
        name: str = Field(None, description="Team name")
        conference: str = Field(None, description="New conference (Norte, Sur, Este, Noreste, Centro")
        profilePic: str = Field(None, description="ProfilePic")
