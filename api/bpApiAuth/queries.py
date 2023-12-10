from pydantic import BaseModel, Field


class Queries:
    class SignUp(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
        city: str = Field(None, description="Your city")

    class Login(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
