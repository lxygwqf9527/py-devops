# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from functools import wraps

import jwt
from flask import request, abort
from flask import current_app
from flask import session
from flask_login import login_user
from flask import g

from api.models.account import User
from api.libs.cache import UserCache

def _auth_with_session():
    print(g.user,'==============')
    print(login_user(g.user),'----------')
    print(session,'=++++++++++')
    # print(login_user(UserCache.get(session["user"]["userName"])),'---------')
    if isinstance(getattr(g, 'user', None), User):
        login_user(g.user)
        return True
    if "user" in session and "userName" in (session["user"] or {}):
        login_user(UserCache.get(session["user"]["userName"]))
        return True
    return False



def auth_required(func):
    if request.json is not None:
        setattr(request, 'values', request.json)
    else:
        setattr(request, 'values', request.values.to_dict())

    current_app.logger.debug(request.values)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            # 先判断有没有authenticated这个属性是否为True，是的话表示通过认证
            return func(*args, **kwargs)
        if _auth_with_session():
            return func(*args, **kwargs)
        # 再判断session or key or token or ip_white_list，满足一样即可
        abort(401)

    return wrapper

def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper