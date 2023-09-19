from pydantic import BaseModel, Field
from typing import Optional


class Queries:
    class Ranking(BaseModel):
        conference: str = Field([], description="Conference of Ibericon")

    class Detail(BaseModel):
        bcpId: str = Field(None, description="BCP Id")
