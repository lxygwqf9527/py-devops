# -*- coding: utf-8 -*-

from flask import g
from flask_login import current_user
from api.app import create_app

app = create_app()

@app.before_request
def after_request():
    g.user = current_user._get_current_object()
