from app import app
from datetime import datetime
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
from authlib.integrations.flask_client import OAuth

import json
from urllib.parse import quote_plus, urlencode


oauth = OAuth(app)
oauth.register(
    "notesApp",
    client_id=app.config.get("OAUTH2_CLIENT_ID"),
    client_secret=app.config.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'{app.config.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)


# View

@app.route("/")
def index():
    return render_template(
        "public/auth.html",
        session=session.get("user"),
    )


@app.route("/login", methods=["POST"])
def login():
    if "user" in session:
        abort(404)
    return oauth.notesApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/callback")
def callback():
    token = oauth.notesApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["POST"])
def logout():
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        app.config.get("OAUTH2_ISSUER")
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


# test api

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for("index"))


@app.route("/signin")
def signin():
    return render_template("public/signin.html")
