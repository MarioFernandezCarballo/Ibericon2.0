# This code handles user authentication and registration in a Flask web application.
# It provides functions for user registration, BCP credentials verification, user login,
# setting authentication cookies, and user logout.

import requests
import json
from datetime import timedelta

from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_login import login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from database import User, City


# Function to register a user
def userSignup(database, form):
    # Verify the user's credentials in an external service (BCP)
    status, data = checkBCPUser(form)
    if status == 200:
        # Hash the user's password
        hashed_password = generate_password_hash(form.password, method='scrypt')
        user = User.query.filter_by(bcpId=data['id']).first()
        city = City.query.filter_by(name=form.city).first()
        if user:
            if not user.registered:
                # Update user data if the user already exists but is not registered
                user.bcpMail = data['email']
                user.password = hashed_password
                user.registered = True
                user.conference = city.conference.id
                user.city = city.id
                database.session.commit()
                # Create a response with user information and set cookies
                response = jsonify({
                    "status": 200,
                    "message": "Registration successful",
                    "data": {
                        "id": user.bcpId,
                        "name": user.bcpName,
                        "mail": user.bcpMail,
                        "conference": city.conference.name,
                        "city": city.name
                    }
                })
                return setUserInfo(response, user)
            return jsonify({
                "status": 401,
                "message": "User already registered",
                "data": {}
            })
        bcpId = data['id']
        new_user = User(
            bcpId=bcpId,
            bcpMail=data['email'],
            password=hashed_password,
            bcpName=data['firstName'] + " " + data['lastName'],
            permissions=0,
            city=city.id,
            conference=city.conference.id,
            registered=True
        )
        database.session.add(new_user)
        database.session.commit()
        # Create a response with user information and set cookies
        response = jsonify({
            "status": 200,
            "message": "Registration successful",
            "data": {
                "id": new_user.bcpId,
                "name": new_user.bcpName,
                "mail": new_user.bcpMail,
                "conference": city.conference.name,
                "city": city.name
            }
        })
        return setUserInfo(response, new_user)
    return jsonify({
        "status": 401,
        "message": "Your BCP credentials are incorrect",
        "data": {}
    })


# Function to verify the user's credentials in an external service (BCP)
def checkBCPUser(form):
    headers = current_app.config['BCP_API_HEADERS']
    r = requests.post('https://prod-api.bestcoastpairings.com/users/signin',
                      json={"username": form.mail, "password": form.password},
                      headers=headers)
    if r.status_code == 200:
        tokens = json.loads(r.text)
        headers['Identity'] = tokens['idToken']
        headers['Authorization'] = 'Bearer ' + tokens['accessToken']
        r = requests.get('https://prod-api.bestcoastpairings.com/users/' + form.mail,
                         headers=headers)
        if r.status_code == 200:
            userData = json.loads(r.text)
            return r.status_code, userData
    return r.status_code, {}


# Function for a user to log in
def userLogin(form):
    user = User.query.filter_by(bcpMail=form.mail).first()
    if user:
        if check_password_hash(user.password, form.password):
            city = City.query.filter_by(id=user.city).first()
            # Create a response with user information and set cookies
            response = jsonify({
                "status": 200,
                "message": "Login successful",
                "data": {
                    "id": user.bcpId,
                    "name": user.bcpName,
                    "mail": user.bcpMail,
                    "conference": city.conference.name if city else None,
                    "city": city.name if city else None
                }
            })
            return setUserInfo(response, user)
    return jsonify({
        "status": 401,
        "message": "Could not verify",
        "data": {}
    })


# Function to set user information and cookies after login
def setUserInfo(response, user):
    set_access_cookies(response, create_access_token(identity=user.bcpId, expires_delta=timedelta(days=365)))
    response.set_cookie("preferred_update", "1")
    response.set_cookie("preferred_gameType", "1")
    response.set_cookie("preferred_language", "en")
    login_user(user)
    return response


# Function to get user information by their ID
def getUserOnly(pl):
    return User.query.filter_by(id=pl).first()


# Function to log out a user
def resetUserInfo():
    response = jsonify({
        "status": 200,
        "message": "Logout successful",
        "data": {}
    })
    logout_user()
    unset_jwt_cookies(response)
    return response
