from app import app

from urllib.request import urlopen
from flask import jsonify, request, session

from .service import authenticateUser


@app.route("/api/auth", methods=["GET", "POST"])
def auth_client():
    user = request.args.get('user')
    password = request.args.get('password')

    print(f"{user} : {password}")

    data = authenticateUser(email=user, password=password)
    print(f"{data} ")

    response = session['user']
    
    return jsonify(message=response)


@app.route("/auth/signup", methods=["POST"])
def signup_client():
    pass


@app.route("/auth/signin", methods=["POST"])
def signin_client():
    pass


@app.route("/auth/refresh", methods=["POST"])
def refresh_client():
    pass


@app.route("/auth/logout", methods=["POST"])
def logout_client():
    pass