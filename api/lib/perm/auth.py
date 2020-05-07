# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from functools import wraps

import jwt
from flask import request
from flask import current_app
from flask import session
from flask_login import login_user
from flask import g

from api.models.account import User


def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

def auth_required(func):
    if request.json is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    current_app.logger.debug(request.values)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        abort(401)

    return wrapper