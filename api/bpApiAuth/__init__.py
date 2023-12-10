
from flask import make_response, redirect, url_for, current_app
from flask_openapi3 import APIBlueprint
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from flask_login import LoginManager, login_required

from .queries import Queries
from .responses import Responses
from .utils import userSignupApi, userLoginApi, getUserOnlyApi, resetUserInfoApi


authApiBP = APIBlueprint('authApiBluePrint', __name__, url_prefix='/api/auth')


loginManager = LoginManager()
jwt = JWTManager()

@loginManager.user_loader
def loadUser(user_id):
    return getUserOnlyApi(user_id)


@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('authBluePrint.login')))
    unset_jwt_cookies(response)
    return response


@authApiBP.post('/signup',
                summary="Sign Up",
                description="Register into the system",
                responses={
                    200: Responses.Auth,
                })
def signupApiEndPoint(query: Queries.SignUp):
    response = userSignupApi(current_app.config['database'], query)
    return response


@authApiBP.post('/login',
                summary="Login",
                description="Log in into the system. You must be registered",
                responses={
                    200: Responses.Auth
                })
def loginApiEndPoint(query: Queries.Login):
    response = userLoginApi(query)
    return response


@authApiBP.get('/logout',
                summary="Sign Up",
                description="Register into the system. You must be logged in",
                responses={
                    200: Responses.BaseResponse
                })
@login_required
def logoutApiEndPoint():
    response = resetUserInfoApi()
    return response
