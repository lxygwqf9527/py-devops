# -*- coding:utf-8 -*-

from flask import g
from flask import request

from api.resource import APIView
from api.libs.perm.crud import UserCRUD
from api.models import Notify
from api.models.account import User


class GetUserInfoView(APIView):
    url_prefix = "/user/info"

    def get(self):
        # 返回个人信息
        access_token = request.headers.get('x-token')
        user = User.query.get_by_access_token(access_token)
        return self.jsonify({'username': user.username,
                            'is_supper': user.is_supper,
                            'host_perms': [] if user.is_supper else user.host_perms,
                            'routers': [] if user.is_supper else user.routers_perms
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