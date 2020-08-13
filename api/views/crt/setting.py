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
        acme_type = []
        acmes = []
        for d in AcmeType.query.all():
            acme_type.append(d.name)
            res = Acme.get_by(acme_type_id=d.id, to_dict=True)
            for acme in res:
                acme['type'] = d.name
                acmes.append(acme)

        return self.jsonify({'acme_type': acme_type, 'acmes': acmes})
    
    def post(self):
        print(request.values)