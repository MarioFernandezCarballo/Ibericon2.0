from pydantic import BaseModel, Field


class Queries:
    class Permission(BaseModel):
        bcpId: str = Field(None, description="BCP Id")
        newPermission: int = Field(None, description="New Permission")

    class AddTournament(BaseModel):
        uri: str = Field(None, description="Tournament Uri")

    class DeleteTournament(BaseModel):
        id: str = Field(None, description="Tournament BCP Id")
