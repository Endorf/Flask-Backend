"""
Sample of using password grant_type.
"""
from app import app
from datetime import datetime
from .service.common import status
import json
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
from .authService import authenticateUser, registerUser, logoutUser

# TODO: add token expiration checks
# TODO: handle errors on UI
# TODO: move out to separate client network calls
# TODO: move out refresh token to secure session
# TODO: investigate ciba

# View

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    else: 
        return render_template(
            "public/signin.html",
            session=session.get("user"),
        )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        print(session["user"])
        return redirect(url_for("dashboard"))

    if request.method == 'GET':
        return render_template("public/signup.html")
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        isSuccesfullyRegistered = registerUser(email, password)
        if isSuccesfullyRegistered:
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("signin"))


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == 'GET':
        return render_template("public/signin.html")
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        isSuccesfullyAuthenticateed = authenticateUser(email, password)
        if(isSuccesfullyAuthenticateed):
            return redirect(url_for("dashboard"))
    else: 
        abort(404)


@app.route("/logout", methods=["POST"])
def logout():
    logoutUser()
    session.clear()

    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template(
            "public/index.html",
            data='',
            data_expiration=session["user"]["access_token"],
            details=json.dumps(session.get("user"), indent=4),
            time=datetime.utcnow().strftime('%H:%M:%S'),
        )
    
    return redirect(url_for("index"))


# Storage

usersData = {
    "user@user.com": {
        "username": "Alice",
        "tag": "Fun Facts",
        "bio": "Alice bio"
    },
    "user1@gmail.com": {
        "username": "Andy",
        "tag": "General",
        "bio": "some bio of Andy"
    },
    "user2@gmail.com": {
        "username": "John",
        "tag": "Smart Quotes",
        "bio": "John bio"
    }
}


# test API

@app.route("/users", methods=["GET", "POST"])
def users():
    response = make_response(jsonify(usersData))
    response.set_cookie('test', "user-config", expires=0)
    return response


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK
