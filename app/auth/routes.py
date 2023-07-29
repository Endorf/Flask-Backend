from app import app

from flask import request, session
from authlib.integrations.flask_oauth2 import ResourceProtector

from .service import authenticate, register, logout, refresh
from app.auth.token_validator import ClientTokenValidator


require_auth = ResourceProtector()
validator = ClientTokenValidator("http://localhost:8080/realms/myorg")
require_auth.register_token_validator(validator)

 
@app.route("/auth/signup", methods=["POST"])
def signup_client():

    email = request.json['email']
    password = request.json['password']

    response = register(email, password)

    return (
        response.json(), 
        response.status_code, 
        {'ContentType':'application/json'}
    )


@app.route("/auth/signin", methods=["POST"])
def signin_client():
    email = request.json['email']
    password = request.json['password']

    response = authenticate(email, password)
    
    return (
        response.json(), 
        response.status_code, 
        {'ContentType':'application/json'}
    )


@app.route("/auth/refresh", methods=["POST"])
def refresh_client():
    token = request.json['token']

    response = refresh(token)

    return (
        response.json(), 
        response.status_code, 
        {'ContentType':'application/json'}
    )


@app.route("/auth/logout", methods=["POST"])
@require_auth(None)
def logout_client():
    refresh_token = request.json['refresh_token']

    response = logout(refresh_token, request.headers['Authorization'])
    session.clear()

    return (
        "", 
        response.status_code, 
        {'ContentType':'application/json'}
    )