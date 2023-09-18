from pydantic import BaseModel, Field
from typing import Optional


class Queries:
    class List(BaseModel):
        region: Optional[str] = Field(None, description="Tournament region")

    class Detail(BaseModel):
        id: str = Field(None, description="Tournament BCP Id")
