#!/bin/bash
mkdir -p /var/www/flask-app || cd /var/www/flask-app

yum install python3-pip -y

python3 -m venv .venv
source /var/www/flask-app/.venv/bin/activate

pip3 install --upgrade pip
pip3 install Flask gunicorn
pip3 install -r requirements.txt

deactivate