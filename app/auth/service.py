from app import app
import requests


def refresh(token):
    post_body = f"client_id={ app.config['OAUTH2_CLIENT_ID'] }&client_secret={ app.config['OAUTH2_CLIENT_SECRET'] }&grant_type=refresh_token&refresh_token={ token }"
    headers = {'Content-Type': "application/x-www-form-urlencoded",}
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/token"

    response = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    return response


def logout(refresh_token, authorization_header):
    post_body = f"client_id={ app.config['OAUTH2_CLIENT_ID'] }&client_secret={ app.config['OAUTH2_CLIENT_SECRET'] }&refresh_token={ refresh_token }"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': authorization_header,
    }
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/logout"

    response = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    return response


def authenticate(email, password):
    post_body = f"client_id={ app.config['OAUTH2_CLIENT_ID'] }&client_secret={ app.config['OAUTH2_CLIENT_SECRET'] }&grant_type=password&scope=email roles profile&username={email.split('@')[0]}&password={password}"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/token"

    response = requests.post(
        url,
        data=post_body,
        headers=headers
    )

    return response


def register(email, password):
    accessToken = _retrieveAdminAccessToken()
    # if(accessToken == ""):
        # return False  # TODO: return error

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

    response = requests.post(
        url,
        json=post_body,
        headers=headers
    )

    if (response.ok):
        return authenticate(email, password)
    else:    
        return response


def _retrieveAdminAccessToken():
    post_body = {
        "grant_type": "client_credentials",
        "client_id": app.config['OAUTH2_CLIENT_ID'],
        "client_secret": app.config['OAUTH2_CLIENT_SECRET'],
        "scope": ["test_api_access"]
    }
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = app.config['OAUTH2_ISSUER'] + "/protocol/openid-connect/token"

    response = requests.post(
        url,
        data=post_body,
        headers=headers
    )
    
    if not response.ok:
        return ""
    else:
        responseJson = response.json()
        if not "access_token" in responseJson:
            return ""
        return responseJson["access_token"]