# -*- coding:utf-8 -*-

from flask import g
from flask import request, abort, session
from flask_login import current_user

from api.resource import APIView
from api.libs.perm.crud import UserCRUD

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
    
    def patch(self):
        if request.values.get('new_password', None) and request.values.get('old_password', None):
            uid = g.user.id
            if len(new_password) < 6:
                return self.jsonify(error='请设置至少6位的新密码')
            if g.user.check_password(old_password):
                UserCRUD.update(uid,password=new_password) 
            else:
                return self.jsonify(error='原密码错误，请重新输入')
        if request.values.get('nickname', None):
            UserCRUD.update(uid, request.values.get('nickname'))
        
        
            

