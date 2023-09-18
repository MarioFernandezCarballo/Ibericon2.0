from pydantic import BaseModel, Field


class Queries:
    # Define a Pydantic BaseModel for sign-up requests
    class SignUp(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
        region: str = Field(None, description="Your Ibericon Region")

    # Define a Pydantic BaseModel for login requests
    class Login(BaseModel):
        mail: str = Field(None, description="BCP Mail")
        password: str = Field(None, description="BCP Password")
