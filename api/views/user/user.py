# -*- coding:utf-8 -*-

from flask import request
from flask import session
from flask_login import current_user
from api.resource import APIView

class GetUserInfoView(APIView):
    url_prefix = "/users/info"

    def get(self):
        name = session.get("CAS_USERNAME") or current_user.nickname
        role = dict(roles=session.get("acl", {}).get("parentRoles", []))
        avatar = current_user.avatar
        
        return self.jsonify(result=dict(name=name,
                                        role=role,
                                        avatar=avatar))