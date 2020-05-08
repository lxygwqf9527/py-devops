# -*- coding:utf-8 -*-

import datetime

import jwt
import uuid
import time
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user, logout_user

from api.models.account import User, Role
from api.resource import APIView
from api.libs import human_datetime, args_required
from api.libs.cache import UserCache
from api.libs.perm import auth_abandoned
from api.libs.perm.crud import UserCRUD




class LoginView(APIView):
    url_prefix = "/login"
    
    # 装饰器，查看request.value是否有某个值
    @args_required("username")
    @args_required("password")
    @auth_abandoned
    def post(self):
        username = request.values.get("username") or request.values.get("email")
        password = request.values.get("password")
        user, authenticated = User.query.authenticate(username, password)
        log_type = request.values.get('type')
        x_real_ip = request.headers.get('x-real-ip', '')
        if user and not user.is_active:
            return abort(403,"账户已被系统禁用")
        if not user:
            return abort(403, "User <{0}> does not exist".format(username))
        if not authenticated:
            return abort(403, "invalid username or password")
        
        if log_type == 'ldap':
            pass
            # ldap未完成
        else:
            if user and user.deleted_by is None:
                return handle_user_info(user, x_real_ip)
        value = UserCache.get_count_error(username)
        if value >= 3:
            if user and user.is_active:
                user.is_active = False
                user.save()
            return abort(403,"账户已被禁用")
        login_user(user)

        role = Role.get_by(id=user.id, first=True, to_dict=False)
        if role:
            pass

def handle_user_info(user, x_real_ip):
    UserCache.del_count_error(user.username)
    token_isvalid = user.access_token and len(user.access_token) == 32 and user.token_expired >= time.time()
    user.access_token = user.access_token if token_isvalid else uuid.uuid4().hex
    user.token_expired = time.time() + 8 * 60 * 60
    user.last_login = human_datetime()
    user.last_ip = x_real_ip
    UserCRUD.update(**user.to_dict(),user.id)
    return jsonify(
        access_token= user.access_token,
        nickname=user.nickname,
        is_supper=user.is_supper,
        has_real_ip=True if x_real_ip else False,
        permissions=[] if user.is_supper else user.page_perms
    )

class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)



