from pydantic import BaseModel, Field
from typing import Optional


class Queries:
    class Ranking(BaseModel):
        conference: Optional[str] = Field(None, description="Conference of Ibericon")

    class Detail(BaseModel):
        bcpId: str = Field(None, description="BCP Id")
