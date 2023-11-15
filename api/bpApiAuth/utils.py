# This code handles user authentication and registration in a Flask web application.
# It provides functions for user registration, BCP credentials verification, user login,
# setting authentication cookies, and user logout.
from utils.auth import userSignup, userLogin, getUserOnly, resetUserInfo


# Function to register a user
def userSignupApi(database, form):
    _, apiResult = userSignup({"email": form.email, "password": form.password})
    return apiResult


# Function for a user to log in
def userLoginApi(form):
    _, apiResult = userLogin({"email": form.mail, "password": form.password})
    return apiResult



# Function to get user information by their ID
def getUserOnlyApi(pl):
    return getUserOnly(pl)


# Function to log out a user
def resetUserInfoApi():
    _, apiResult = resetUserInfo()
    return apiResult
