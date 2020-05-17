# -*- coding: utf-8 -*-

from flask import g
from flask_login import current_user
from api.app import create_app

app = create_app()



@app.before_request
def before_request():
    g.user = current_user

@app.after_request
def after_request(response):
    g.user = current_user

    return response