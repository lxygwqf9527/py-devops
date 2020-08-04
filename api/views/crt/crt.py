# -*- coding:utf-8 -*-
from flask import request, g

from api.resource import APIView
from api.models.ssl import SSL

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
        ssl_types = [i.ssl_type.name for i in ssls if i.ssl_type ]
        perms = [x.id for x in ssls] if g.user.is_supper else g.user.ssl_perms
        # 这里证书字符串和证书私钥也一起提交给了前端，证书太多可能会导致前端数据加载太慢，卡顿的现象出现,后面再优化
        print({'ssl_types': ssl_types, 'ssls': [x.to_dict() for x in ssls], 'perms': perms})
        return self.jsonify({'ssl_types': ssl_types, 'ssls': [x.to_dict() for x in ssls], 'perms': perms})

    # def post(self):
    #     '''

    #     '''