# -*- coding:utf-8 -*-
from flask import request, g

from api.resource import APIView
from api.models.ssl import SSL, SSLSetting

class SSLSettingView(APIView):
    '''
        证书配置视图
    '''
    url_prefix = '/setting'

    def get(self):
        data = []
        for i in SSLSetting.query.all():
            if i.ssl_type:
                i['ssl_type'] = i.ssl_type.key
            data.append(i)
        
        return self.jsonify(data)
