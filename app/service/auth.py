from app import app
from flask import session
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

    if "access_token" in accessTokenRespJson:
        session["user"] = accessTokenRespJson
        session["email"] = email
        session["access_token"] = accessTokenRespJson["access_token"]
        session["refresh_token"] = accessTokenRespJson["refresh_token"]

    return accessTokenResp