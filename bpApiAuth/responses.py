from pydantic import BaseModel, Field


# Define data models for the API responses
class Models:
    # Define a Pydantic BaseModel for sign-up response data
    class SignUp(BaseModel):
        id: str = Field(None, description="BCP Id")
        name: str = Field(None, description="BCP Name")
        mail: str = Field(None, description="BCP Mail")
        conference: int = Field(None, description="Your Ibericon conference Id")


# Define response models for the API endpoints
class Responses:
    class BaseResponse(BaseModel):
        status: int = Field(None, description="Status code")
        message: str = Field(None, description="Exception information")

    class Auth(BaseResponse):
        data: Models.SignUp = Field({}, description="User")
