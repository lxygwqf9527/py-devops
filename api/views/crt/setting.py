# -*- coding:utf-8 -*-
from flask import request
import json
import CloudFlare

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

def acme_cloudflare_test(user,key):
    cf = CloudFlare.CloudFlare(email=user,token=key)
    try:
        zones = cf.zones.get(params={'per_page':1})
        return True
    except:
        return False

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

        return self.jsonify({'acme_types': acme_type, 'acmes': acmes})
    
    def post(self):
        id = request.values.get('id', None)
        user = request.values.get('user', None)
        key = request.values.get('key', None)
        acme_type = request.values.get('acme_type', None)
        if request.values.get('id'):
            Acme.get_by(id=request.values['id'], first=True, to_dict=False).update(**request.values)
        elif Acme.query.filter(db.exists().where(and_(Acme.user==user,Acme.deleted_by.is_(None),Acme.acme_type.name==acme_type))).scalar():
            return self.jsonify(error='%s已存在的用户【%s】' % (acme_type,user))
        else:
            request.values['created_by'] = g.user.id
            acme = Acme.create(**request.values)
            if g.user.role:
                g.user.role.add_acme_perm(acme.id)
        return self.jsonify(error='')
    
    def patch(self):
        '''
            更新
        '''
        
        return self.jsonify(error='')