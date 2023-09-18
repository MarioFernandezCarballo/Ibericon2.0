from pydantic import BaseModel, Field
from typing import Optional


class Queries:
    class Ranking(BaseModel):
        region: str = Field([], description="Ragion of Ibericon")

    class Detail(BaseModel):
        bcpId: str = Field(None, description="BCP Id")
