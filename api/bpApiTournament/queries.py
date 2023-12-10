from pydantic import BaseModel, Field
from typing import Optional

class Queries:
    class List(BaseModel):
        conference: Optional[str] = Field(None, description="Tournament conference")

    class Detail(BaseModel):
        id: str = Field(None, description="Tournament BCP Id")
