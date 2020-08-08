# -*- coding:utf-8 -*-
from flask import request, g

from api.resource import APIView
from api.models.ssl import SSL, SSLType

class SSLView(APIView):
    '''
        证书视图
    '''

    def get(self):
        '''
            获取所有的ssl type和ssls 后面调整为根据用户权限来返回具体证书
        '''
        # ssl_id = request.values.get('id')
        # if ssl_id:
        #     if not g.user.has_ssl_perm(ssl_id):
        #         return self.jsonify(error='无权访问该ssl证书')
        ssls = SSL.query.filter(SSL.deleted_at.is_(None)).all()
        ssl_types = [i.ssl_type.key for i in ssls if i.ssl_type ]
        perms = [x.id for x in ssls] if g.user.is_supper else g.user.ssl_perms
        # 这里证书字符串和证书私钥也一起提交给了前端，证书太多可能会导致前端数据加载太慢，卡顿的现象出现,后面再优化
        ssl_list = []
        for x in ssls:
            if x.ssl_type_id:
                type_name = x.ssl_type.key
            x = x.to_dict()
            x['ssl_type'] = type_name
            ssl_list.append(x)
        return self.jsonify({'ssl_types': ssl_types, 'ssls': ssl_list, 'perms': perms})

    # def post(self):
    #     '''

    def patch(self):
        '''
        证书类别
        '''
        if request.values.get("id") and request.values.get("ssl_type"):
            ssl = SSL.get_by(id=request.values.get('id'), to_dict=False, first=True)
            if not ssl:
                return self.jsonify(error="未找到指定证书")
            SSLType.get_by(id=ssl.ssl_type_id, to_dict=False, first=True).update(key=request.values.get("ssl_type"))
            return self.jsonify(SSL.query.filter(ssl_type=request.values.get("ssl_type"), deleted_at=None).count())
        else:
            return self.jsonify(error="不能跟原来的名字一样")
