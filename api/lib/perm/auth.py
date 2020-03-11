# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from functools import wraps
from flask import request
from flask import current_app

def auth_abandoned(func):
    setattr(func, "authenticated", False)
    print(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args,kwargs)
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

        if _auth_with_session() or _auth_with_key() or _auth_with_token() or _auth_with_ip_white_list():
            return func(*args, **kwargs)

        abort(401)

    return wrapper