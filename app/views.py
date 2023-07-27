from app import app
from .service.common import status
from datetime import datetime
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
import requests
from authlib.integrations.flask_client import OAuth

import json
from urllib.parse import quote_plus, urlencode

# TODO: add token expiration checks
# TODO: handle errors on UI
# TODO: move out to separate client network calls
# TODO: move out refresh token to secure session
# TODO: investigate ciba


appConf = {
    "OAUTH2_CLIENT_ID": "test_web_app",
    "OAUTH2_CLIENT_SECRET": "BbyZrpYjSf6JRxOEs1tVBFUcYVcfAYIQ",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myorg",
    "OAUTH2_ISSUER_HOST": "http://localhost:8080",
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

        accessToken = _retrieveAdminAccessToken()

        if(accessToken == ""):
            abort(404)
        else:
            isSuccesfullySubmited = _submitNewUser(email, password, accessToken)
            if (isSuccesfullySubmited):
                isSuccesfullyAuthenticateed = _authenticateUser(email, password)

                if(isSuccesfullyAuthenticateed):
                    return redirect(url_for("dashboard"))


        return render_template("public/signup.html")
    else:
        abort(404)


def _authenticateUser(email, password):
    post_body = f"client_id={ appConf.get('OAUTH2_CLIENT_ID') }&client_secret={ appConf.get('OAUTH2_CLIENT_SECRET') }&grant_type=password&scope=email roles profile&username={email.split('@')[0]}&password={password}"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = appConf.get("OAUTH2_ISSUER") + "/protocol/openid-connect/token"

    accessTokenResp = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    accessTokenRespJson = accessTokenResp.json()
    print(f"${accessTokenRespJson}")

    if not "access_token" in accessTokenRespJson:
        abort(401)
    else:
        session["user"] = accessTokenRespJson
        print(session)
        session["access_token"] = accessTokenRespJson["access_token"]
        session["refresh_token"] = accessTokenRespJson["refresh_token"]


    return accessTokenResp.ok


def _submitNewUser(email, password, accessToken):
    post_body = {
        "username": email.split("@")[0],
        "email": email,
        "enabled": True,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }],
        "groups": []
    }
    headers = {
        'Authorization': "Bearer " + accessToken,
        'Content-Type': "application/json; charset=utf-8",
    }
    url = appConf.get("OAUTH2_ISSUER_HOST") + "/admin/realms/myorg/users"

    accessTokenResp = requests.post(
        url,
        json=post_body,
        headers=headers
    )
    return accessTokenResp.ok


def _retrieveAdminAccessToken():
    post_body = {
        "grant_type": "client_credentials",
        "client_id": appConf.get("OAUTH2_CLIENT_ID"),
        "client_secret": appConf.get("OAUTH2_CLIENT_SECRET"),
        "scope": ["test_api_access"]
    }
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = appConf.get("OAUTH2_ISSUER") + "/protocol/openid-connect/token"

    accessTokenResp = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    
    if not accessTokenResp.ok:
        return ""
    else:
        accessTokenRespJson = accessTokenResp.json()
        if not "access_token" in accessTokenRespJson:
            return ""
        return accessTokenRespJson["access_token"]


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if "user" in session:
        return redirect(url_for("dashboard"))
    if request.method == 'GET':
        return render_template("public/signin.html")
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        isSuccesfullyAuthenticateed = _authenticateUser(email, password)
        if(isSuccesfullyAuthenticateed):
            return redirect(url_for("dashboard"))
        # if "user" in session:
        #     abort(404)
        # return oauth.notesApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))
    else: 
        abort(404)


@app.route("/callback", methods=["POST"])
def callback():
    token = oauth.notesApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["POST"])
def logout():
    # id_token = session["user"]["id_token"]
    # session.clear()
    # return redirect(
    #     appConf.get("OAUTH2_ISSUER")
    #     + "/protocol/openid-connect/logout?"
    #     + urlencode(
    #         {
    #             "post_logout_redirect_uri": url_for("loggedOut", _external=True),
    #             "id_token_hint": id_token
    #         },
    #         quote_via=quote_plus,
    #     )
    # )
    post_body = f"client_id={ appConf.get('OAUTH2_CLIENT_ID') }&client_secret={ appConf.get('OAUTH2_CLIENT_SECRET') }&refresh_token={ session['user']['refresh_token'] }"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + session["user"]["access_token"],
    }
    url = appConf.get("OAUTH2_ISSUER") + "/protocol/openid-connect/logout"

    accessTokenResp = requests.post(
        url,
        data=post_body,
        headers=headers
    )

    if(accessTokenResp.ok):
        session.clear()

    return redirect(url_for("index"))


    


@app.route("/loggedout")
def loggedOut():
    if "user" in session:
        abort(404)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    print("dashboard")
    if "user" in session:
        return render_template(
            "public/index.html",
            data='',
            data_expiration=session["user"]["access_token"],
            details=json.dumps(session.get("user"), indent=4),
            time=datetime.utcnow().strftime('%H:%M:%S'),
        )
    # if "user" in session:
    #     if "access_token" in session["user"]:
    #         return render_template(
    #             "public/index.html",
    #             data='',
    #             # data_expiration=session["user"]["id_token"],
    #             data_expiration=session["user"]["access_token"],
    #             details=json.dumps(session.get("user"), indent=4),
    #             time=datetime.utcnow().strftime('%H:%M:%S'),
    #         )
    
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
