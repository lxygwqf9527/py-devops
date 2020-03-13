# -*- coding: utf-8 -*-

print('1-----')
from flask import g
print('2------')
from flask_login import current_user
print('3------',current_user)
from api.app import create_app
print('4----')

app = create_app()



@app.before_request
def before_request():
    g.user = current_user
