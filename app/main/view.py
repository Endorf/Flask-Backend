from app import app
from datetime import datetime
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
from authlib.integrations.flask_client import OAuth
import json


# View

@app.route("/")
def index():
    return redirect(url_for("auth"))