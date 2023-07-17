"""
Test Client.
"""
import requests

tokenUrl = "http://localhost:8080/realms/myorg/protocol/openid-connect/token"

client_id = "test_api_client"
client_secret = "tkEvkjOGBG4JIpWYTdxoWndb4SbauS0Q"
requiredScopes = " ".join(["test_api_access"])

# request access token
post_body = {"grant_type": "client_credentials",
             "client_id": client_id,
             "client_secret": client_secret,
             "scope": requiredScopes}
headers = {'content-type': "application/x-www-form-urlencoded"}

accessTokenResp = requests.post(tokenUrl,
                    data=post_body,
                    headers=headers)

if not accessTokenResp.ok:
    print("response status not ok")
    quit()

accessTokenRespJson = accessTokenResp.json()

if not "access_token" in accessTokenRespJson:
    print("access_token not found")
    quit()

accessToken = accessTokenRespJson["access_token"]
print(accessToken)

# test request
apiReqHeaders = {
    'content-type': "application/json",
    'authorization': f"Bearer {accessToken}"
}
apiResp = requests.get("http://localhost:5000/api/scoped", headers=apiReqHeaders)

# parse the response
if not apiResp.ok:
    print("ok response not received")
    quit()

print(apiResp.json())
