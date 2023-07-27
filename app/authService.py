from app import app
from flask import make_response, redirect, abort, request, session, url_for
import requests

def authenticateUser(email, password):
    post_body = f"client_id={ app.config['OAUTH2_CLIENT_ID'] }&client_secret={ app.config['OAUTH2_CLIENT_SECRET'] }&grant_type=password&scope=email roles profile&username={email.split('@')[0]}&password={password}"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/token"

    accessTokenResp = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    accessTokenRespJson = accessTokenResp.json()
    print(f"${accessTokenRespJson}")

    if not "access_token" in accessTokenRespJson:
        return False
    else:
        session["user"] = accessTokenRespJson
        session["email"] = email
        session["access_token"] = accessTokenRespJson["access_token"]
        session["refresh_token"] = accessTokenRespJson["refresh_token"]

    return accessTokenResp.ok


def registerUser(email, password):
    accessToken = _retrieveAdminAccessToken()
    if(accessToken == ""):
        return False

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
    url = app.config['OAUTH2_ISSUER_HOST'] + "/admin/realms/myorg/users"

    accessTokenResp = requests.post(
        url,
        json=post_body,
        headers=headers
    )

    if (accessTokenResp.ok):
        return authenticateUser(email, password)
    else:    
        return accessTokenResp.ok


def _retrieveAdminAccessToken():
    post_body = {
        "grant_type": "client_credentials",
        "client_id": app.config['OAUTH2_CLIENT_ID'],
        "client_secret": app.config['OAUTH2_CLIENT_SECRET'],
        "scope": ["test_api_access"]
    }
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/token"

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
