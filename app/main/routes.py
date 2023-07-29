from app import app

from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import jsonify
from app.auth.token_validator import ClientTokenValidator

require_auth = ResourceProtector()
validator = ClientTokenValidator("http://localhost:8080/realms/myorg")
require_auth.register_token_validator(validator)


@app.route("/api/public")
def public():
    response = "Everything fine! Authorization is not required here!" 
    return jsonify(message=response)


@app.route("/api/private")
@require_auth(None)
def private():
    response = "Everything fine! You are authorized!"
    return jsonify(message=response)


@app.route("/api/notes")
@require_auth(None)
def notes():
    response = "Everything fine! Notes here"
    return jsonify(message=response)


@app.route("/api/scoped")
@require_auth("test_api_access")
def private_scoped():
    response = "Everything fine! You are authorized with test_api_access scope!"
    return jsonify(message=response)