# -*- coding:utf-8 -*-
from flask import request

from api.resource import APIView
from api.models.ssl import SSL, SSLSetting, Acme, AcmeType

class SSLSettingView(APIView):
    '''
        证书配置视图
    '''
    url_prefix = '/setting'

    def get(self):
        print(request.values)
    
    def post(self):
        print(request.values)

class AcmeSettingView(APIView):
    url_prefix = '/setting/acme'

    def get(self):
        data = {}
        for d in AcmeType.query.all():
            res = Acme.get_by(acme_type_id=d.id, to_dict=True)
            data={d.name: res}
        
        return self.jsonify(data)
    
    def post(self):
        print(request.values)