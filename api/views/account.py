# -*- coding:utf-8 -*-

import datetime

import jwt
from flask import abort
from flask import current_app
from flask import request
from flask import session
from flask_login import login_user, logout_user

from api.lib.decorator import args_required
from api.lib.perm.auth import auth_abandoned
from api.models.acl import User, Role
from api.resource import APIView
from api.lib.perm.acl.role import RoleRelationCRUD
from api.lib.perm.acl.cache import RoleCache

class LoginView(APIView):
    url_prefix = "/login"

    @args_required("username")
    @args_required("password")
    @auth_abandoned
    def post(self):

        username = request.values.get("username") or request.values.get("email")
        password = request.values.get("password")
        user, authenticated = User.query.authenticate(username, password)
        if not user:
            return self.jsonify(msg="User <{0}> does not exist".format(username),status=403)
        if not authenticated:
            return self.jsonify(msg="invalid username or password",status=403)
        login_user(user)

        token = jwt.encode({
            'sub': user.email,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=24 * 60 * 7)},
            current_app.config['SECRET_KEY'])
        role = Role.get_by(id=user.rid, first=True, to_dict=False)
        print(role)
        if role:
            parent_ids = RoleRelationCRUD.recursive_parent_ids(role.id)
            parent_roles = [RoleCache.get(i).name for i in parent_ids]
        else:
            parent_roles = []
        session["acl"] = dict(uid=user.uid,
                              avatar=user.avatar,
                              userName=user.username,
                              nickName=user.nickname,
                              parentRoles=parent_roles)

        return self.jsonify(token=token.decode(),status=200)
    
class LogoutView(APIView):
    url_prefix = "/logout"

    @auth_abandoned
    def post(self):
        logout_user()
        self.jsonify(code=200)



