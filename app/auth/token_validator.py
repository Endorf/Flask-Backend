from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
import json
from urllib.request import urlopen

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