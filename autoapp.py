# -*- coding: utf-8 -*-

from flask import g
from flask_login import current_user
from api.app import create_app
from api.extensions import celery

app = create_app()
# app.app_context().push()
@app.before_request
def after_request():
    g.user = current_user