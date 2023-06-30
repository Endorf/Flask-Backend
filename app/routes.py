from app import app

from functools import wraps
from .service.common import status

from flask import jsonify


def authorized(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        refresh_token()
        return f(*args, **kwargs)

    return decorated_function


def refresh_token():
    print("not authorized")


@app.route("/api/public")
def public():
    response = "Authorization is not required." 
    return jsonify(message=response)


@app.route("/api/private")
@authorized
def private():
    response = "Authorization is required!"
    return jsonify(message=response)
