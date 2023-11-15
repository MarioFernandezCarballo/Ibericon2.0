from pydantic import BaseModel, Field
from typing import Optional


class Queries:
    class Ranking(BaseModel):
        conference: str = Field([], description="Conference of Ibericon")
    class Detail(BaseModel):
        bcpId: str = Field(None, description="BCP Id")

    class Modify(BaseModel):
        name: str = Field(None, description="Team name")
        conference: str = Field(None, description="New conference (Norte, Sur, Este, Noreste, Centro")
        profilePic: str = Field(None, description="ProfilePic")  # TODO FRONT conviertelo a mapa de bits o lo que sea
        # ...
