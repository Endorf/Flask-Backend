from app import app
from .service.common import status
from datetime import datetime
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
from authlib.integrations.flask_client import OAuth

import json
from urllib.parse import quote_plus, urlencode


appConf = {
    "OAUTH2_CLIENT_ID": "test_web_app",
    "OAUTH2_CLIENT_SECRET": "BbyZrpYjSf6JRxOEs1tVBFUcYVcfAYIQ",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myorg",
    "FLASK_SECRET": "somelongrandomstring",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "notesApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)


# View

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    else: 
        return render_template(
            "public/auth.html",
            session=session.get("user"),
        )
 

@app.route("/signin", methods=["POST"])
def signin():
    if "user" in session:
        abort(404)
    return oauth.notesApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/callback", methods=["POST"])
def callback():
    token = oauth.notesApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["POST"])
def logout():
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("loggedOut", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )


@app.route("/loggedout")
def loggedOut():
    if "user" in session:
        abort(404)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template(
            "public/index.html",
            data='',
            data_expiration=session["user"]["id_token"],
            details=json.dumps(session.get("user"), indent=4),
            time=datetime.utcnow().strftime('%H:%M:%S'),
        )
    else:
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
