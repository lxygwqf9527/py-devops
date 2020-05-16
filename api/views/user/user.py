# -*- coding:utf-8 -*-

from flask import request, abort, session
from flask_login import current_user
from api.resource import APIView

class GetUserInfoView(APIView):
    url_prefix = "/info"

    def get(self):
        # name = session.get("CAS_USERNAME") or current_user.nickname
        # role = dict(roles=session.get("acl", {}).get("parentRoles", []))
        # avatar = current_user.avatar
        
        # return self.jsonify(result=dict(name=name,
        #                                 role=role,
        #                                 avatar=avatar))
        return abort(404,'呵呵')

class SelfView(APIView):
    url_prefix = "/self"
    pass
