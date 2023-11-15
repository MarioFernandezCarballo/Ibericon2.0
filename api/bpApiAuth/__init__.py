# This handles user authentication and provides endpoints for
# user registration, login, and logout.

# Import necessary modules and libraries
from flask import make_response, redirect, url_for, current_app
from flask_openapi3 import APIBlueprint
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from flask_login import LoginManager, login_required

# Import custom modules
from .queries import Queries
from .responses import Responses
from .utils import userSignupApi, userLoginApi, getUserOnlyApi, resetUserInfoApi


# Create an APIBlueprint object for authentication-related routes
authApiBP = APIBlueprint('authApiBluePrint', __name__, url_prefix='/api/auth')


# Create instances of LoginManager and JWTManager
loginManager = LoginManager()
jwt = JWTManager()


# Function to load a user based on their ID (used by LoginManager)
@loginManager.user_loader
def loadUser(user_id):
    return getUserOnlyApi(user_id)


# Function to handle expired JWT tokens and redirect the user to the login page
@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('authBluePrint.login')))
    unset_jwt_cookies(response)
    return response


# Define a route for user registration
@authApiBP.post('/signup',
                summary="Sign Up",
                description="Register into the system",
                responses={
                    200: Responses.Auth,
                })
def signupApiEndPoint(query: Queries.SignUp):
    # Process the user registration request
    response = userSignupApi(current_app.config['database'], query)
    return response


# Define a route for user login
@authApiBP.post('/login',
                summary="Login",
                description="Log in into the system. You must be registered",
                responses={
                    200: Responses.Auth
                })
def loginApiEndPoint(query: Queries.Login):
    # Process the user login request
    response = userLoginApi(query)
    return response


# Define a route for user logout
@authApiBP.get('/logout',
                summary="Sign Up",
                description="Register into the system. You must be logged in",
                responses={
                    200: Responses.BaseResponse
                })
@login_required
def logoutApiEndPoint():
    # Process the logout request
    response = resetUserInfoApi()
    return response
