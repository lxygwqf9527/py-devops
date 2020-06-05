# -*- coding:utf-8 -*-

from flask import request, g
from paramiko.ssh_exception import AuthenticationException

from api.config.Appsetting import AppSetting
from api.models import Host
from api.resource import APIView
from api.libs.ssh import SSH


class HostView(APIView):
    '''
        主机视图
    '''
    # url_prefix = '/hosts'

    def get(self):
        '''
            获取所有的zones和主机
        '''
        hosts = Host.query.filter(Host.deleted_at.is_(None))
        zones = [x['zone'] for x in hosts.order_by(Host.zone).with_entities(Host.zone).distinct()]
        return self.jsonify({'zones': zones, 'hosts': [x.to_dict() for x in hosts]})
    
    def post(self):
        '''
            添加主机
        '''
        id = request.values.pop('id', None)
        zone = request.values.pop('zone', None)
        name = request.values.pop('name',None)
        username = request.values.pop('username', None)
        password = request.values.pop('password', None)
        hostname = request.values.pop('hostname', None)
        port = request.values.pop('port', None)
        if valid_ssh(hostname, port, username, password) is False:
            return self.jsonify('auth fail')
        
        if id:
            Host.get_by(id=id, to_dict=False).update(request.values)
        else:
            request.values['created_by'] = g.user.id
            Host.create(**request.values)
        return self.jsonify(error='')

def valid_ssh(hostname, port, username, password):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')
    if password:
        cli = SSH(hostname, port, username, password=password)
        code, out = cli.exec_command('mkdir -p -m 700 ~/.ssh && \
                echo %r >> ~/.ssh/authorized_keys && \
                chmod 600 ~/.ssh/authorized_keys' % public_key)
        if code != 0:
            raise Exception(f'add public key error: {out!r}')
    else:
        cli = SSH(hostname, port, username, private_key)
    
    try:
        cli.ping()
    except AuthenticationException:
        return False
    return True