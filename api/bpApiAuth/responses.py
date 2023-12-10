from pydantic import BaseModel, Field


class Models:
    class SignUp(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        mail: str = Field(None, description="BCP Mail")
        conference: int = Field(None, description="Your Ibericon conference Id")


class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="Status code")
        message: str = Field(None, description="Exception information")

    class Auth(BaseResponse):
        data: Models.SignUp = Field({}, description="User")
