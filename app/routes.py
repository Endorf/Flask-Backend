from app import app

import json
from urllib.request import urlopen
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from flask import Flask, jsonify

from .authDecorator import requireAuthFactory


class ClientTokenValidator(JWTBearerTokenValidator):
    def __init__(self, issuer):
        jsonurl = urlopen(f"{issuer}/protocol/openid-connect/certs")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(ClientTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "iss": {"essential": True, "value": issuer}
        }


require_auth = requireAuthFactory("http://127.0.0.1:8080/realms/myorg")
# require_auth = ResourceProtector()
# validator = ClientTokenValidator("http://localhost:8080/realms/myorg")
# require_auth.register_token_validator(validator)


@app.route("/api/public")
def public():
    response = "Authorization is not required." 
    return jsonify(message=response)


@app.route("/api/private")
@require_auth(None)
def private():
    response = "Authorization is required!"
    return jsonify(message=response)


@app.route("/api/scoped")
@require_auth("test_api_access")
def private_scoped():
    response = "Authorization is required test_api_access scope"
    return jsonify(message=response)
