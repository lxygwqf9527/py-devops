# -*- coding: utf-8 -*-

from flask import g
from flask_login import current_user
from api.app import create_app

app = create_app()

print(current_user,'wdnmd==============================================qiezi')

@app.after_request
def reg_user():
    g.user = current_user
