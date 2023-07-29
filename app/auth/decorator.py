import json
from functools import wraps
import jwt
import requests
from flask import abort, request


def requireAuthFactory(issuer=None):
    def require_creds(scopes=None):
        def __getRequiredScopes():
            if isinstance(scopes, str):
                return scopes.split(" ")
            elif isinstance(scopes, list):
                return scopes


        def __readPubKey(kid):
            pubKeysUrl = f"{issuer}/protocol/openid-connect/certs"
            allPubKeys = requests.get(pubKeysUrl).json()["keys"]
            reqPubKeyJwk = [x for x in allPubKeys if x["kid"] == kid][0]
            reqPubKey = jwt.algorithms.RSAAlgorithm.from_jwk(
            json.dumps(reqPubKeyJwk))
            return reqPubKey
        

        def __parseUserScopes(accessToken):
            jwtHeader = jwt.get_unverified_header(accessToken)
            alg = jwtHeader['alg']
            kid = jwtHeader['kid']

            pubKey = __readPubKey(kid)
            
            payload = jwt.decode(
                accessToken,
                key=pubKey,
                algorithms=[alg],
                options={"verify_aud": False}
            )

            return payload["scope"].split(" ")
        

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                accessToken = (
                    request.headers.get('Authorization', "")
                    .replace("Bearer ", "")
                )
                required_scopes = __getRequiredScopes()

                if accessToken == "":
                    abort(401)
                if required_scopes is None:
                    return f(*args, **kwargs)
                else:
                    userScopes = __parseUserScopes(accessToken)

                    print(userScopes)
                    print(scopes)

                    isAnyReqScopeAbsent = len([x for x in required_scopes if x not in userScopes]) > 0
                    if isAnyReqScopeAbsent:
                        abort(401)
                    else:
                        return f(*args, **kwargs)
                
            return decorated_function
        return decorator
    return require_creds
