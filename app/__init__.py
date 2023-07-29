import os
from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

app.secret_key = os.urandom(24)

from app.auth import view
from app.auth import routes
from app.dashboard import view
from app.main import view
from app.main import routes
