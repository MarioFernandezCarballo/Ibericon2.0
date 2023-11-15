from pydantic import BaseModel, Field


class Queries:
    # Define a Pydantic BaseModel for sign-up requests
    class SignUp(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
        city: str = Field(None, description="Your city")

    # Define a Pydantic BaseModel for login requests
    class Login(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
