from app import app

from .service.common import status

from flask import jsonify
from flask import render_template
from flask import make_response, redirect, request, url_for
from datetime import datetime

# Storage

usersData = {
    "user@user.com": {
        "username": "Alice",
        "tag": "Fun Facts",
        "bio": "Alice bio"
    },
    "user1@gmail.com": {
        "username": "Andy",
        "tag": "General",
        "bio": "some bio of Andy"
    },
    "user2@gmail.com": {
        "username": "John",
        "tag": "Smart Quotes",
        "bio": "John bio"
    }
}


# View

@app.route("/")
def index():
    return render_template("public/auth.html")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "public/index.html",
        data='',
        data_expiration=' No data ',
        details='Server time:',
        time=datetime.utcnow().strftime('%H:%M:%S'),
    )


@app.route("/login")
def login():
    return render_template("public/auth.html")


@app.route("/logout", methods=["POST"])
def logout():
    return redirect(url_for('login'))


@app.route('/auth/register', methods=["GET", "POST"])
def get_data():
    email = request.form.get('email')
    print(email)
    password = request.form.get('password')

    if (password) and (email in usersData):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


# API

@app.route("/users", methods=["GET", "POST"])
def users():
    response = make_response(jsonify(usersData))
    response.set_cookie('test', "user-config", expires=0)
    return response


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK
