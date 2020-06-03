# -*- coding:utf-8 -*-

from flask import request

from api.config.Appsetting import AppSetting
from api.models import Host
from api.resource import APIView
from api.libs.ssh import SSH


class HostView(APIView):
    '''
        主机视图
    '''
    url_prefix = '/hosts'

    def get(self):
        '''
            获取所有的zones和主机
        '''
        hosts = Host.query.filter(Host.deleted_at.is_(None))
        print(hosts)
        zones = [x['zone'] for x in hosts.order_by(Host.zone).with_entities(Host.zone).distinct()]
        print(zones)
        return self.jsonify({'zones': zones, 'hosts': [x.to_dict() for x in hosts]})
    
    def post(self):
        '''
            添加主机
        '''
        zone = request.values['zone']
        username = request.values['username']
        password = request.values['password']
        hostname = request.values['hostname']
        port = request.values['port']
        if valid_ssh(username, port, username, password):
            pass

def valid_ssh(hostname, port, username, password):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')