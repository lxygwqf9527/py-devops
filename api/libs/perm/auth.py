# -*- coding:utf-8 -*- 


from __future__ import unicode_literals

from functools import wraps

from flask import request, abort
from flask import current_app
from flask import session
from flask_login import login_user, current_user
from flask import g
import time

import settings
from api.models.account import User
from api.libs.cache import UserCache


def _auth_with_session():
    # session 判断函数
    if isinstance(getattr(g, 'user', None), User):
        login_user(g.user)
        return True
    if "user" in session and "username" in (session["user"] or {}):
        login_user(UserCache.get(session["user"]["username"]))
        return True
    return False

def _auth_with_key():
    key = request.values.get('_key')
    secret = request.values.get('_secret')
    path = request.path
    keys = sorted(request.values.keys())
    req_args = [request.values[k] for k in keys if k not in ("_key", "_secret")]
    user, authenticated = User.query.authenticate_with_key(key, secret, req_args, path)
    if user and authenticated:
        login_user(user)
        return True
    return False

def _auth_with_token():
    if request.path in settings.AUTHENTICATION_EXCLUDES:
            return None
    access_token = request.headers.get('x-token')
    if access_token and len(access_token) == 32:
        x_real_ip = request.headers.get('x-real-ip', '')
        user = User.get_by(first=True,to_dict=False,access_token=access_token)
        # if user and x_real_ip == user.last_ip and user.token_expired >= time.time() and user.is_active:
        if user and user.token_expired >= time.time() and user.is_active:
            request.user = user
            user.token_expired = time.time() + 8 * 60 * 60
            user.save()
            login_user(user)
            g.user = user
            return True

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
        if _auth_with_session() or _auth_with_token():
            return func(*args, **kwargs)
        # 再判断session or key or token or ip_white_list，满足一样即可
        abort(401,'认证未通过')

    return wrapper

def auth_abandoned(func):
    setattr(func, "authenticated", False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper