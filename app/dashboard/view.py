from app import app
from datetime import datetime
from flask import jsonify
from flask import render_template
from flask import make_response, redirect, abort, request, session, url_for
from authlib.integrations.flask_client import OAuth
import json


# View

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template(
            "public/index.html",
            data='',
            data_expiration=session["user"]["id_token"],
            details=json.dumps(session.get("user"), indent=4),
            time=datetime.utcnow().strftime('%H:%M:%S'),
        )
    else:
        return redirect(url_for("index"))