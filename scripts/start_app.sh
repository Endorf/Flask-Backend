#!/bin/bash
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn