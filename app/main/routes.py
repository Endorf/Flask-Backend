import json
from app import app

from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import jsonify
from app.auth.token_validator import ClientTokenValidator
from app.service.common.status import HTTP_200_OK

require_auth = ResourceProtector()
validator = ClientTokenValidator(app.config.get('OAUTH2_ISSUER'))
require_auth.register_token_validator(validator)

class Note:
    def __init__(self, username, email, tag_index, title, details):
        self.username = username
        self.email = email
        self.tag_index = tag_index
        self.title = title
        self.details = details

# 0: General
# 1: Metaphor
# 2: Quote
_notes = [
    Note("Skylinn", "skylinn@email.com", 1, "Why did Atlas shrug?", None),
    Note("Francisco d'Anconia", "franco@email.com", 0, "What do you think about contradictions?", "Contradictions do not exist. Whenever you think that you are facing a contradiction, check your premises. You will find that one of them is wrong."),
    Note("Quintus Horatius Flaccus", "flaccus@email.com", 0, "Carpe diem, quam minimum credula postero", None),
    Note("John Connor", "connor@email.com", 2, "The future is not set. There is no fate but what we make for oursalves.", "My father told it to my mom"),
    Note("John Galt", "galt@email.com", 0, "Existence is identity, consciousness is identification.", None),
    Note("user 747", "user747@email.com", 2, "Try to be a rainbow in someone's clouds.", None),
]


def _note_to_dict(person):
    return {
        'username': person.username, 
        'email': person.email, 
        'tag_index': person.tag_index, 
        'title': person.title, 
        'details': person.details
    }



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
    return (
        json.dumps(_notes, default=_note_to_dict, indent=4),
        HTTP_200_OK, 
        {'ContentType':'application/json'}
    )


@app.route("/api/scoped")
@require_auth("test_api_access")
def private_scoped():
    response = "Everything fine! You are authorized with test_api_access scope!"
    return jsonify(message=response)