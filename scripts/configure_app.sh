#!/bin/bash
cd /var/www/flask-app
export FLASK_APP=run.py
export FLASK_ENV=production

ln -sf /var/www/flask-app/gunicorn.service /etc/systemd/system/gunicorn.service