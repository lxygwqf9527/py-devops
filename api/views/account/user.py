# -*- coding:utf-8 -*-

from flask import g
from flask import request, abort, session
from flask_login import current_user

from api.resource import APIView
from api.libs.perm.crud import UserCRUD
from api.models import Notify


class GetUserInfoView(APIView):
    url_prefix = "/user/info"

    def get(self):
        # 返回个人信息
        # print(current_user)
        # name = session.get("CAS_USERNAME") or current_user.nickname
        # role = dict(roles=session.get("acl", {}).get("parentRoles", []))
        # avatar = current_user.avatar
        
        # return 
        # return self.jsonify(result=dict(name=name,
        #                                 role=role,
        #                                 avatar=avatar))
        return self.jsonify({'username': current_user.username,
                            'is_supper': current_user.is_supper,
                            'host_perms': [] if current_user.is_supper else current_user.host_perms,
                            'permissions': [] if current_user.is_supper else user.page_perms
                            })

class SelfView(APIView):
    url_prefix = "/user/self"
    
    def patch(self):
        new_password = request.values.get('new_password', None)
        old_password = request.values.get('old_password', None)
        uid = g.user.id
        if  new_password and old_password:

            if len(new_password) < 6:
                return self.jsonify(error='请设置至少6位的新密码')
            if g.user.check_password(old_password):
                UserCRUD.update(uid,_password=new_password) 
            else:
                return self.jsonify(error='原密码错误，请重新输入')
        if request.values.get('nickname', None):
            UserCRUD.update(uid, nickname=request.values.get('nickname'))
        
        return self.jsonify(error='')
        
class NotifyView(APIView):
    """
        notify视图
    """
    url_prefix = "/user/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        for notify in Notify.get_by_in_id(ids=request.values['ids'],to_dict=False):
            notify.update(unread=False)
            
        return self.jsonify(error='')