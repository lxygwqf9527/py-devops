# -*- coding:utf-8 -*-
from flask import request, g
import json
import CloudFlare
from sqlalchemy import and_

from api.extensions import db
from api.resource import APIView
from api.models.ssl import SSL, SSLSetting, AcmeDns, AcmeDnsType


class SSLSettingView(APIView):
    '''
        证书配置视图
    '''
    url_prefix = '/setting'

    def get(self):
        print(request.values)
    
    def post(self):
        print(request.values)

def dns_cloudflare_test(user,key):
    cf = CloudFlare.CloudFlare(email=user,token=key)
    try:
        cf.zones.get(params={'per_page':1})
        return True
    except:
        return False

class DnsSettingView(APIView):
    url_prefix = '/setting/acme/dns'

    def get(self):
        acme_dns_types = []
        acme_dnss = []
        for d in AcmeDnsType.query.all():
            acme_dns_types.append(d.name)
            res = AcmeDns.get_by(acme_dns_type_id=d.id, to_dict=True)
            for dns in res:
                dns['type'] = d.name
                acme_dnss.append(dns)

        perms = [x['id'] for x in acme_dnss] if g.user.is_supper else g.user.dns_perms
        return self.jsonify({'acme_dns_types': acme_dns_types, 'acme_dnss': acme_dnss, 'perms': perms})
    
    def post(self):
        id = request.values.get('id', None)
        user = request.values.get('user', None)
        key = request.values.get('key', None)
        acme_dns_type = request.values.get('acme_dns_type', None)
        acme_dns_type_qy = AcmeDnsType.get_by(name=acme_dns_type,to_dict=False,first=True)
        if request.values.get('id'):
            AcmeDns.get_by(id=request.values['id'], first=True, to_dict=False).update(**request.values)
            return self.jsonify(error='')
        elif acme_dns_type_qy is not None and AcmeDns.query.all(db.exists().where(and_(AcmeDns.user==user,AcmeDns.deleted_by.is_(None),AcmeDns.acme_dns_type_id==acme_dns_type_qy.id))).scalar():
            return self.jsonify(error='%s已存在的用户【%s】' % (acme_dns_type,user))
        elif acme_dns_type_qy is None:
            kwargs = {"name": acme_dns_type}
            AcmeDnsType.create(**kwargs)

        request.values['acme_dns_type_id'] = AcmeDnsType.get_by(name=acme_dns_type,to_dict=False,first=True).id
        request.values['created_by'] = g.user.id
        request.values.pop('acme_dns_type')
        print(request.values,'===========')
        acmedns = AcmeDns.create(**request.values)
        if g.user.role:
            g.user.role.add_acme_dns_perm(acmedns.id)
        return self.jsonify(error='')
        
    
    def patch(self):
        '''
            更新
        '''
        
        return self.jsonify(error='')